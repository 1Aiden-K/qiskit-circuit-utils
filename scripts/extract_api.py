from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path("src/qiskit_circuit_utils")


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


for path in sorted(PACKAGE.glob("*.py")):
    if path.name.startswith("_"):
        continue

    tree = ast.parse(path.read_text())

    functions = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and not node.name.startswith("_")
    ]

    if not functions:
        continue

    print(f"\n## {path.name}\n")

    for function in functions:
        print(format_signature(function))

        docstring = ast.get_docstring(function)
        if docstring:
            summary = docstring.split("\n\n", 1)[0]
            print(f"    {summary}")

        print()