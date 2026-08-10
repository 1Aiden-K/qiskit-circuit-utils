"""Utilities for adding non-basic measurements to quantum circuits."""

from collections.abc import Iterable, Sequence

from qiskit import QuantumCircuit

from ._types import (
    ClbitSpecifier,
    MeasurementPair,
    PauliBasis,
    QubitSpecifier,
)
from ._validation import require_clbits, require_qubits, require_same_length

# Computational / Z-basis measurement

def z(
    circuit: QuantumCircuit,
    qubit: QubitSpecifier,
    clbit: ClbitSpecifier,
) -> None:
    """Measure a qubit in the Z basis.

    Maps:
        |0> -> 0
        |1> -> 1
    """
    circuit.measure(qubit, clbit)

def z_all(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
    clbits: Sequence[ClbitSpecifier],
) -> None:
    """Measure each qubit in the Z basis."""
    require_same_length(
        qubits,
        clbits,
        names=("qubits", "classical bits"),
    )

    circuit.measure(qubits, clbits)

# X-basis measurement

def x(
    circuit: QuantumCircuit,
    qubit: QubitSpecifier,
    clbit: ClbitSpecifier,
) -> None:
    """Measure a qubit in the X basis.

    Maps:
        |+> -> 0
        |-> -> 1
    """
    circuit.h(qubit)
    circuit.measure(qubit, clbit)

def x_all(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
    clbits: Sequence[ClbitSpecifier],
) -> None:
    """Measure each qubit in the X basis."""
    require_same_length(
        qubits,
        clbits,
        names=("qubits", "classical bits"),
    )

    circuit.h(qubits)
    circuit.measure(qubits, clbits)

# Y-basis measurement

def y(
    circuit: QuantumCircuit,
    qubit: QubitSpecifier,
    clbit: ClbitSpecifier,
) -> None:
    """Measure a qubit in the Y basis.

    Maps:
        |+i> -> 0
        |-i> -> 1
    """
    circuit.sdg(qubit)
    circuit.h(qubit)
    circuit.measure(qubit, clbit)

def y_all(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
    clbits: Sequence[ClbitSpecifier],
) -> None:
    """Measure each qubit in the Y basis."""
    require_same_length(
        qubits,
        clbits,
        names=("qubits", "classical bits"),
    )

    circuit.sdg(qubits)
    circuit.h(qubits)
    circuit.measure(qubits, clbits)

# Arbitrary Pauli-basis measurement

def pauli(
    circuit: QuantumCircuit,
    qubit: QubitSpecifier,
    clbit: ClbitSpecifier,
    basis: PauliBasis = "Z",
) -> None:
    """Measure a qubit in a Pauli basis.

    Args:
        circuit: Circuit to modify.
        qubit: Qubit to measure.
        clbit: Classical bit receiving the result.
        basis: Measurement basis: "X", "Y", or "Z".

    Raises:
        ValueError: If the basis is unsupported.
    """
    basis = basis.upper()

    if basis == "X":
        x(circuit, qubit, clbit)
    elif basis == "Y":
        y(circuit, qubit, clbit)
    elif basis == "Z":
        z(circuit, qubit, clbit)
    else:
        raise ValueError(
            f"Unsupported Pauli basis: {basis!r}. "
            "Expected 'X', 'Y', or 'Z'."
        )

# Bell basis measurement

def bell_basis(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
    clbits: Sequence[ClbitSpecifier],
) -> None:
    """Measure two qubits in the Bell basis.

    Performs the inverse of Bell-state preparation followed by
    measurement in the computational basis.

    The measurement outcomes correspond to:

        00 -> |Phi+>
        01 -> |Psi+>
        10 -> |Phi->
        11 -> |Psi->

    Args:
        circuit: Circuit to modify.
        qubits: Two qubits to measure.
        clbits: Two classical bits receiving the measurement results.

    Raises:
        ValueError: If exactly two qubits and classical bits are not provided.
    """
    require_qubits(qubits, 2)
    require_clbits(clbits, 2)

    q0, q1 = qubits

    circuit.cx(q0, q1)
    circuit.h(q0)
    circuit.measure(qubits, clbits)

# Pair-based measurement

def z_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[MeasurementPair],
) -> None:
    """Measure each (qubit, classical-bit) pair in the Z basis."""
    for qubit, clbit in pairs:
        z(circuit, qubit, clbit)


def x_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[MeasurementPair],
) -> None:
    """Measure each (qubit, classical-bit) pair in the X basis."""
    for qubit, clbit in pairs:
        x(circuit, qubit, clbit)


def y_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[MeasurementPair],
) -> None:
    """Measure each (qubit, classical-bit) pair in the Y basis."""
    for qubit, clbit in pairs:
        y(circuit, qubit, clbit)

# Measure entire circuit

def all(
    circuit: QuantumCircuit,
) -> None:
    """Measure all qubits.

    Classical bits are added to the circuit automatically by Qiskit.
    """
    circuit.measure_all()