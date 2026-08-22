from __future__ import annotations

import ast
import re
from pathlib import Path

PACKAGE = Path("src/qiskit_circuit_utils")
DOCS = Path("docs")


def format_annotation(node: ast.expr | None) -> str:
    if node is None:
        return ""
    return ast.unparse(node)


def format_arg(arg: ast.arg, default: ast.expr | None = None) -> str:
    result = arg.arg

    if arg.annotation is not None:
        result += f": {format_annotation(arg.annotation)}"

    if default is not None:
        result += f" = {ast.unparse(default)}"

    return result


def format_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    args = node.args
    parts: list[str] = []

    positional = [*args.posonlyargs, *args.args]
    defaults = [None] * (len(positional) - len(args.defaults)) + list(args.defaults)

    for i, (arg, default) in enumerate(zip(positional, defaults)):
        parts.append(format_arg(arg, default))

        if args.posonlyargs and i + 1 == len(args.posonlyargs):
            parts.append("/")

    if args.vararg is not None:
        parts.append(f"*{format_arg(args.vararg)}")
    elif args.kwonlyargs:
        parts.append("*")

    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        parts.append(format_arg(arg, default))

    if args.kwarg is not None:
        parts.append(f"**{format_arg(args.kwarg)}")

    return_annotation = format_annotation(node.returns)
    suffix = f" -> {return_annotation}" if return_annotation else ""

    return f"{node.name}({', '.join(parts)}){suffix}"


def parse_docstring(docstring: str | None) -> dict[str, object]:
    """Parse the project's Google-style function docstrings."""
    if not docstring:
        return {
            "description": "",
            "args": [],
            "raises": [],
        }

    lines = docstring.splitlines()

    description_lines: list[str] = []
    args: list[tuple[str, str]] = []
    raises: list[tuple[str, str]] = []

    section: str | None = None
    current_name: str | None = None
    current_text: list[str] = []

    def flush_entry() -> None:
        nonlocal current_name, current_text

        if current_name is None:
            return

        text = " ".join(part.strip() for part in current_text).strip()

        if section == "args":
            args.append((current_name, text))
        elif section == "raises":
            raises.append((current_name, text))

        current_name = None
        current_text = []

    for line in lines:
        stripped = line.strip()

        if stripped == "Args:":
            flush_entry()
            section = "args"
            continue

        if stripped == "Raises:":
            flush_entry()
            section = "raises"
            continue

        if re.match(r"^[A-Z][A-Za-z ]*:$", stripped):
            flush_entry()
            section = "other"
            continue

        if section is None:
            description_lines.append(line)
            continue

        if section in {"args", "raises"}:
            match = re.match(r"^(\w+):\s*(.*)$", stripped)

            if match:
                flush_entry()
                current_name = match.group(1)
                current_text = [match.group(2)]
            elif current_name is not None and stripped:
                current_text.append(stripped)

    flush_entry()

    description = "\n".join(description_lines).strip()

    return {
        "description": description,
        "args": args,
        "raises": raises,
    }


def format_description(description: str) -> str:
    """Preserve paragraphs while joining wrapped docstring lines."""
    if not description:
        return ""

    paragraphs = re.split(r"\n\s*\n", description)

    formatted: list[str] = []

    for paragraph in paragraphs:
        lines = [line.strip() for line in paragraph.splitlines()]
        formatted.append(" ".join(lines))

    return "\n\n".join(formatted)


def generate_function_docs(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> str:
    parsed = parse_docstring(ast.get_docstring(node))

    description = format_description(str(parsed["description"]))
    args = parsed["args"]
    raises = parsed["raises"]

    lines = [
        f"## `{node.name}`",
        "",
        "```python",
        format_signature(node),
        "```",
        "",
    ]

    if description:
        lines.extend([description, ""])

    if args:
        lines.extend(["### Parameters", ""])

        for name, text in args:
            lines.append(f"- `{name}` — {text}")

        lines.append("")

    if raises:
        lines.extend(["### Raises", ""])

        for exception, text in raises:
            lines.append(f"- `{exception}` — {text}")

        lines.append("")

    return "\n".join(lines)


def public_modules() -> list[Path]:
    return [
        path
        for path in sorted(PACKAGE.glob("*.py"))
        if not path.name.startswith("_")
        and path.name != "__init__.py"
    ]


def generate_module_docs(path: Path) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"))

    functions = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and not node.name.startswith("_")
    ]

    module_name = path.stem
    module_docstring = ast.get_docstring(tree)

    lines = [
        f"# `{module_name}`",
        "",
    ]

    if module_docstring:
        lines.extend(
            [
                format_description(module_docstring),
                "",
            ]
        )

    for function in functions:
        lines.append(generate_function_docs(function))

    return "\n".join(lines).rstrip() + "\n"


def generate_index(modules: list[Path]) -> str:
    lines = [
        "# API Reference",
        "",
        "The public API is organized into modules by functionality.",
        "",
    ]

    for path in modules:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        module_docstring = ast.get_docstring(tree)

        summary = ""
        if module_docstring:
            summary = format_description(module_docstring).split("\n\n", 1)[0]

        if summary:
            lines.append(
                f"- [`{path.stem}`]({path.stem}.md) — {summary}"
            )
        else:
            lines.append(f"- [`{path.stem}`]({path.stem}.md)")

    lines.append("")

    return "\n".join(lines)


def main() -> None:
    DOCS.mkdir(exist_ok=True)

    modules = public_modules()

    for path in modules:
        output = DOCS / f"{path.stem}.md"
        output.write_text(
            generate_module_docs(path),
            encoding="utf-8",
        )
        print(f"Generated {output}")

    index = DOCS / "README.md"
    index.write_text(
        generate_index(modules),
        encoding="utf-8",
    )
    print(f"Generated {index}")


if __name__ == "__main__":
    main()