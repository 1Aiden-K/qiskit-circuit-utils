"""Utilities for classically controlled quantum corrections."""

from collections.abc import Sequence

from qiskit import QuantumCircuit

from ._types import ClbitSpecifier, QubitSpecifier
from ._validation import require_same_length


def x_if(
    circuit: QuantumCircuit,
    target: QubitSpecifier,
    control_bit: ClbitSpecifier,
) -> None:
    """Apply a classically controlled X correction.

    Applies an X gate to ``target`` when ``control_bit`` is 1.

    Args:
        circuit: Circuit to modify.
        target: Qubit receiving the correction.
        control_bit: Classical bit controlling the correction.
    """
    with circuit.if_test((control_bit, 1)):
        circuit.x(target)


def z_if(
    circuit: QuantumCircuit,
    target: QubitSpecifier,
    control_bit: ClbitSpecifier,
) -> None:
    """Apply a classically controlled Z correction.

    Applies a Z gate to ``target`` when ``control_bit`` is 1.

    Args:
        circuit: Circuit to modify.
        target: Qubit receiving the correction.
        control_bit: Classical bit controlling the correction.
    """
    with circuit.if_test((control_bit, 1)):
        circuit.z(target)


def pauli(
    circuit: QuantumCircuit,
    target: QubitSpecifier,
    x_bit: ClbitSpecifier,
    z_bit: ClbitSpecifier,
) -> None:
    """Apply classically controlled Pauli X and Z corrections.

    This is the standard correction used by quantum teleportation
    and entanglement-swapping protocols.

    Args:
        circuit: Circuit to modify.
        target: Qubit receiving the corrections.
        x_bit: Classical bit controlling the X correction.
        z_bit: Classical bit controlling the Z correction.
    """
    x_if(circuit, target, x_bit)
    z_if(circuit, target, z_bit)


def x_if_all(
    circuit: QuantumCircuit,
    targets: Sequence[QubitSpecifier],
    control_bits: Sequence[ClbitSpecifier],
) -> None:
    """Apply controlled X corrections to corresponding qubits.

    Args:
        circuit: Circuit to modify.
        targets: Qubits receiving the corrections.
        control_bits: Classical bits controlling the corrections.

    Raises:
        ValueError: If the numbers of targets and control bits differ.
    """
    require_same_length(
        targets,
        control_bits,
        names=("targets", "classical bits"),
    )

    for target, control_bit in zip(targets, control_bits):
        x_if(circuit, target, control_bit)


def z_if_all(
    circuit: QuantumCircuit,
    targets: Sequence[QubitSpecifier],
    control_bits: Sequence[ClbitSpecifier],
) -> None:
    """Apply controlled Z corrections to corresponding qubits.

    Args:
        circuit: Circuit to modify.
        targets: Qubits receiving the corrections.
        control_bits: Classical bits controlling the corrections.

    Raises:
        ValueError: If the numbers of targets and control bits differ.
    """
    require_same_length(
        targets,
        control_bits,
        names=("targets", "classical bits"),
    )

    for target, control_bit in zip(targets, control_bits):
        z_if(circuit, target, control_bit)


def pauli_all(
    circuit: QuantumCircuit,
    targets: Sequence[QubitSpecifier],
    x_bits: Sequence[ClbitSpecifier],
    z_bits: Sequence[ClbitSpecifier],
) -> None:
    """Apply Pauli corrections to corresponding target qubits.

    Args:
        circuit: Circuit to modify.
        targets: Qubits receiving the corrections.
        x_bits: Classical bits controlling X corrections.
        z_bits: Classical bits controlling Z corrections.

    Raises:
        ValueError: If the input sequences have different lengths.
    """
    require_same_length(
        targets,
        x_bits,
        z_bits,
        names=("targets", "X bits", "Z bits"),
    )

    for target, x_bit, z_bit in zip(targets, x_bits, z_bits):
        pauli(
            circuit,
            target,
            x_bit=x_bit,
            z_bit=z_bit,
        )
