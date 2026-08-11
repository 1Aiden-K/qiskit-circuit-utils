"""Utilities for quantum transforms."""

from collections.abc import Sequence
from math import pi

from qiskit import QuantumCircuit

from . import operation
from ._types import QubitSpecifier
from ._validation import require_distinct_qubits, require_min_qubits


def qft(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
    *,
    swaps: bool = True,
) -> None:
    """Apply the quantum Fourier transform.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits on which to apply the transform.
        swaps: Whether to reverse the qubit order using SWAP gates.

    Raises:
        ValueError: If no qubits are provided.
        ValueError: If duplicate qubits are specified.
    """
    require_min_qubits(qubits, 1)
    require_distinct_qubits(qubits)

    for index in reversed(range(len(qubits))):
        target = qubits[index]

        circuit.h(target)

        for offset, control in enumerate(
            reversed(qubits[:index]),
            start=1,
        ):
            circuit.cp(
                pi / (2**offset),
                control,
                target,
            )

    if swaps:
        operation.reverse(circuit, qubits)

def inverse_qft(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
    *,
    swaps: bool = True,
) -> None:
    """Apply the inverse quantum Fourier transform.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits on which to apply the inverse transform.
        swaps: Whether to reverse the qubit order using SWAP gates.

    Raises:
        ValueError: If no qubits are provided.
        ValueError: If duplicate qubits are specified.
    """
    require_min_qubits(qubits, 1)
    require_distinct_qubits(qubits)

    if swaps:
        operation.reverse(circuit, qubits)

    for index, target in enumerate(qubits):
        for offset, control in reversed(
            list(
                enumerate(
                    reversed(qubits[:index]),
                    start=1,
                )
            )
        ):
            circuit.cp(
                -pi / (2**offset),
                control,
                target,
            )

        circuit.h(target)