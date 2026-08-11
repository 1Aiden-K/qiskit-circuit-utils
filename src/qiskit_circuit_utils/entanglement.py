"""Utilities for entanglement protocols and distribution."""

from collections.abc import Sequence

from qiskit import QuantumCircuit

from . import correction, measurement, preparation
from ._types import ClbitSpecifier, QubitSpecifier, BinaryValue
from ._validation import (
    require_clbits,
    require_distinct_clbits,
    require_distinct_qubits,
    require_min_qubits,
    require_qubits,
    require_choice,
    require_length,
)


def swap(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
    clbits: Sequence[ClbitSpecifier],
) -> None:
    """Perform entanglement swapping.

    The qubits must be ordered as ``[alice, ancillary, bob]``, where
    a remote qubit is already entangled with ``alice`` and
    ``ancillary`` is already entangled with ``bob``.

    The classical bits must be ordered as
    ``[phase_bit, parity_bit]``.

    Args:
        circuit: Circuit to modify.
        qubits: Alice, ancillary, and Bob qubits, in that order.
        clbits: Phase and parity measurement bits, in that order.

    Raises:
        ValueError: If exactly three distinct qubits and two distinct
            classical bits are not provided.
    """
    require_qubits(qubits, 3)
    require_clbits(clbits, 2)
    require_distinct_qubits(qubits)
    require_distinct_clbits(clbits)

    alice, ancillary, bob = qubits
    phase_bit, parity_bit = clbits

    measurement.bell_basis(
        circuit,
        [alice, ancillary],
        clbits,
    )

    correction.pauli(
        circuit,
        bob,
        x_bit=parity_bit,
        z_bit=phase_bit,
    )


def teleport(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
    clbits: Sequence[ClbitSpecifier],
) -> None:
    """Teleport a single-qubit state.

    The qubits must be ordered as ``[source, ancillary, target]``.
    ``ancillary`` and ``target`` are assumed to initially be in |0>.

    The classical bits must be ordered as
    ``[phase_bit, parity_bit]``.

    Args:
        circuit: Circuit to modify.
        qubits: Source, ancillary, and target qubits, in that order.
        clbits: Phase and parity measurement bits, in that order.

    Raises:
        ValueError: If exactly three distinct qubits and two distinct
            classical bits are not provided.
    """
    require_qubits(qubits, 3)
    require_clbits(clbits, 2)
    require_distinct_qubits(qubits)
    require_distinct_clbits(clbits)

    source, ancillary, target = qubits
    phase_bit, parity_bit = clbits

    preparation.bell_state(
        circuit,
        [ancillary, target],
    )

    measurement.bell_basis(
        circuit,
        [source, ancillary],
        clbits,
    )

    correction.pauli(
        circuit,
        target,
        x_bit=parity_bit,
        z_bit=phase_bit,
    )


def distribute(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
) -> None:
    """Prepare GHZ-style entanglement across the specified qubits.

    The qubits are assumed to initially be in |0>. The first qubit
    acts as the source and is entangled with every remaining qubit.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits across which to distribute entanglement.

    Raises:
        ValueError: If fewer than two qubits are provided.
        ValueError: If duplicate qubits are specified.
    """
    require_min_qubits(qubits, 2)
    require_distinct_qubits(qubits)

    source, *targets = qubits

    circuit.h(source)

    for target in targets:
        circuit.cx(source, target)


def extend(
    circuit: QuantumCircuit,
    source: QubitSpecifier,
    targets: Sequence[QubitSpecifier],
) -> None:
    """Extend GHZ-style entanglement to additional qubits.

    ``source`` is assumed to already belong to the entangled state.
    Each target is assumed to initially be in |0>.

    Args:
        circuit: Circuit to modify.
        source: Qubit already belonging to the entangled state.
        targets: Qubits to add to the entangled state.
    """
    for target in targets:
        circuit.cx(source, target)


def connect(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
) -> None:
    """Correlate two qubits using a CNOT.

    The qubits must be ordered as ``[source, target]``. The target
    is assumed to initially be in |0>.

    For a source in alpha|0> + beta|1>, the resulting state is
    alpha|00> + beta|11>.

    Args:
        circuit: Circuit to modify.
        qubits: Source and target qubits, in that order.

    Raises:
        ValueError: If exactly two qubits are not provided.
    """
    require_qubits(qubits, 2)

    source, target = qubits
    circuit.cx(source, target)


def disconnect(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
) -> None:
    """Reverse a compatible ``connect`` operation.

    The qubits must be ordered as ``[source, target]``.

    This disentangles the qubits only when their state has the
    structure produced by ``connect``.

    Args:
        circuit: Circuit to modify.
        qubits: Source and target qubits, in that order.

    Raises:
        ValueError: If exactly two qubits are not provided.
    """
    require_qubits(qubits, 2)

    source, target = qubits
    circuit.cx(source, target)


def transfer(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
) -> None:
    """Exchange the states of two qubits using SWAP.

    Unlike teleportation, this operation is fully unitary and
    requires no measurement or classical communication.

    The qubits must be ordered as ``[source, target]``.

    Args:
        circuit: Circuit to modify.
        qubits: Source and target qubits, in that order.

    Raises:
        ValueError: If exactly two qubits are not provided.
    """
    require_qubits(qubits, 2)

    source, target = qubits
    circuit.swap(source, target)


def superdense_code(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
    clbits: Sequence[ClbitSpecifier],
    message: tuple[BinaryValue, BinaryValue],
) -> None:
    """Transmit two classical bits using superdense coding.

    The qubits must be ordered as ``[alice, bob]``. Both qubits are
    assumed to initially be in |0>.

    The message must be ordered as ``[phase_bit, parity_bit]``.
    The classical bits receive the decoded message in the same order.

    Args:
        circuit: Circuit to modify.
        qubits: Alice and Bob qubits, in that order.
        clbits: Classical bits for the decoded message.
        message: Phase and parity bits to transmit, in that order.

    Raises:
        ValueError: If exactly two distinct qubits and two distinct
            classical bits are not provided.
        ValueError: If exactly two message bits are not provided.
    """
    require_qubits(qubits, 2)
    require_clbits(clbits, 2)
    require_distinct_qubits(qubits)
    require_distinct_clbits(clbits)
    require_length(message, 2, name="message bits")

    for bit in message:
        require_choice(bit, (0, 1), name="message bit")

    alice, bob = qubits
    phase_bit, parity_bit = message

    preparation.bell_state(
        circuit,
        [alice, bob],
    )

    if parity_bit:
        circuit.x(alice)

    if phase_bit:
        circuit.z(alice)

    measurement.bell_basis(
        circuit,
        [alice, bob],
        clbits,
    )