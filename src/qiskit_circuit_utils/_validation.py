"""Internal validation utilities."""

from collections.abc import Sequence
from typing import TypeVar

from ._types import ClbitSpecifier, QubitSpecifier

T = TypeVar("T")

def require_length(
    values: Sequence[T],
    count: int,
    *,
    name: str = "values",
) -> None:
    """Require a sequence to contain exactly ``count`` elements.

    Args:
        values: Sequence to validate.
        count: Required number of elements.
        name: Name used in the error message.

    Raises:
        ValueError: If the sequence does not have the required length.
    """
    if len(values) != count:
        raise ValueError(
            f"Expected exactly {count} {name}, got {len(values)}."
        )

def require_min_length(
    values: Sequence[T],
    minimum: int,
    *,
    name: str = "values",
) -> None:
    """Require a sequence to contain at least ``minimum`` elements.

    Args:
        values: Sequence to validate.
        minimum: Minimum number of elements.
        name: Name used in the error message.

    Raises:
        ValueError: If the sequence contains too few elements.
    """
    if len(values) < minimum:
        raise ValueError(
            f"Expected at least {minimum} {name}, got {len(values)}."
        )

def require_same_length(
    *sequences: Sequence[object],
    names: Sequence[str] | None = None,
) -> None:
    """Require all supplied sequences to have equal lengths.

    Args:
        sequences: Sequences to compare.
        names: Optional names used in the error message.

    Raises:
        ValueError: If the sequence lengths differ.
    """
    if len(sequences) < 2:
        return

    lengths = tuple(len(sequence) for sequence in sequences)

    if len(set(lengths)) == 1:
        return

    if names is not None:
        require_length(names, len(sequences), name="names")

        details = ", ".join(
            f"{name}={length}"
            for name, length in zip(names, lengths)
        )
    else:
        details = ", ".join(map(str, lengths))

    raise ValueError(
        f"Expected sequences of equal length, got {details}."
    )

def require_non_empty(
    values: Sequence[T],
    *,
    name: str = "values",
) -> None:
    """Require a sequence to contain at least one element.

    Args:
        values: Sequence to validate.
        name: Name used in the error message.

    Raises:
        ValueError: If the sequence is empty.
    """
    if not values:
        raise ValueError(f"Expected at least one {name}.")

def require_distinct(
    values: Sequence[T],
    *,
    name: str = "values",
) -> None:
    """Require all elements in a sequence to be distinct.

    Args:
        values: Sequence to validate.
        name: Name used in the error message.

    Raises:
        ValueError: If duplicate elements are present.
    """
    if len(set(values)) != len(values):
        raise ValueError(f"Expected distinct {name}.")

# Qubit validation

def require_qubits(
    qubits: Sequence[QubitSpecifier],
    count: int,
) -> None:
    """Require exactly ``count`` qubits."""
    require_length(qubits, count, name="qubits")

def require_min_qubits(
    qubits: Sequence[QubitSpecifier],
    minimum: int,
) -> None:
    """Require at least ``minimum`` qubits."""
    require_min_length(qubits, minimum, name="qubits")


def require_distinct_qubits(
    qubits: Sequence[QubitSpecifier],
) -> None:
    """Require all specified qubits to be distinct."""
    require_distinct(qubits, name="qubits")

# Classical-bit validation

def require_clbits(
    clbits: Sequence[ClbitSpecifier],
    count: int,
) -> None:
    """Require exactly ``count`` classical bits."""
    require_length(clbits, count, name="classical bits")

def require_distinct_clbits(
    clbits: Sequence[ClbitSpecifier],
) -> None:
    """Require all specified classical bits to be distinct."""
    require_distinct(clbits, name="classical bits")