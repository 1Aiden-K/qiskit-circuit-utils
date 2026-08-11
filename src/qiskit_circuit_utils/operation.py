"""Utilities for multi-qubit operations."""

from collections.abc import Sequence

from qiskit import QuantumCircuit

from ._types import QubitSpecifier
from ._validation import require_distinct_qubits


def reverse(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
) -> None:
    """Reverse the order of the specified qubits using SWAP gates.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits whose states to reverse.

    Raises:
        ValueError: If duplicate qubits are specified.
    """
    require_distinct_qubits(qubits)

    for source, target in zip(
        qubits[: len(qubits) // 2],
        reversed(qubits[(len(qubits) + 1) // 2 :]),
        strict=True,
    ):
        circuit.swap(source, target)