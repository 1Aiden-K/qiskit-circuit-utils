"""Utilities for preparing states across qubits."""

from collections.abc import Sequence
from itertools import pairwise

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import random_statevector

from ._types import (
    BellState,
    Eigenvalue,
    QubitSpecifier,
    StatevectorLike,
)
from ._validation import (
    require_choice,
    require_distinct_qubits,
    require_length,
    require_min_qubits,
    require_non_empty,
    require_qubits,
    require_same_length,
)


def bell_state(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
    state: BellState = "phi+",
) -> None:
    """Prepare two qubits in one of the four Bell states.

    The qubits are assumed to initially be in the |00> state.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to prepare. Exactly two distinct qubits are required.
        state: Bell state to prepare. One of:
            - "phi+": (|00> + |11>) / sqrt(2)
            - "phi-": (|00> - |11>) / sqrt(2)
            - "psi+": (|01> + |10>) / sqrt(2)
            - "psi-": (|01> - |10>) / sqrt(2)

    Raises:
        ValueError: If exactly two distinct qubits are not specified.
        ValueError: If an unsupported Bell state is specified.
    """
    require_qubits(qubits, 2)
    require_distinct_qubits(qubits)
    require_choice(
        state,
        ("phi+", "phi-", "psi+", "psi-"),
        name="state",
    )

    q0, q1 = qubits

    circuit.h(q0)
    circuit.cx(q0, q1)

    if state == "phi-":
        circuit.z(q0)
    elif state == "psi+":
        circuit.x(q1)
    elif state == "psi-":
        circuit.x(q1)
        circuit.z(q0)


def ghz_state(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
) -> None:
    """Prepare the specified qubits in a GHZ state.

    The qubits are assumed to initially be in the |0> state.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to prepare. At least two distinct qubits are required.

    Raises:
        ValueError: If fewer than two qubits are specified.
        ValueError: If duplicate qubits are specified.
    """
    require_min_qubits(qubits, 2)
    require_distinct_qubits(qubits)

    circuit.h(qubits[0])

    for control, target in pairwise(qubits):
        circuit.cx(control, target)


def w_state(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
) -> None:
    """Prepare the specified qubits in a W state.

    The W state is an equal superposition of all computational basis
    states containing exactly one excitation.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits on which to prepare the W state. At least two
            distinct qubits are required.

    Raises:
        ValueError: If fewer than two qubits are provided.
        ValueError: If duplicate qubits are specified.
    """
    require_min_qubits(qubits, 2)
    require_distinct_qubits(qubits)

    num_qubits = len(qubits)

    state = np.zeros(2**num_qubits, dtype=complex)

    for qubit in range(num_qubits):
        state[1 << qubit] = 1 / np.sqrt(num_qubits)

    circuit.initialize(state.tolist(), qubits)


def zero_state(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
) -> None:
    """Prepare the specified qubits in the |0> state.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to prepare.

    Raises:
        ValueError: If duplicate qubits are specified.
    """
    require_distinct_qubits(qubits)

    circuit.reset(qubits)


def one_state(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
) -> None:
    """Prepare the specified qubits in the |1> state.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to prepare.

    Raises:
        ValueError: If duplicate qubits are specified.
    """
    require_distinct_qubits(qubits)

    circuit.reset(qubits)
    circuit.x(qubits)


def plus_state(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
) -> None:
    """Prepare the specified qubits in the |+> state.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to prepare.

    Raises:
        ValueError: If duplicate qubits are specified.
    """
    require_distinct_qubits(qubits)

    circuit.reset(qubits)
    circuit.h(qubits)


def minus_state(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
) -> None:
    """Prepare the specified qubits in the |-> state.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to prepare.

    Raises:
        ValueError: If duplicate qubits are specified.
    """
    require_distinct_qubits(qubits)

    circuit.reset(qubits)
    circuit.x(qubits)
    circuit.h(qubits)


def basis_state(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
    state: str,
) -> None:
    """Prepare a computational basis state.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to prepare.
        state: Bit string describing the state, such as "101".
            Bits correspond positionally to ``qubits``: ``state[i]``
            specifies the state of ``qubits[i]``.

    Raises:
        ValueError: If the bit string length does not match the number
            of qubits or contains characters other than "0" and "1".
        ValueError: If duplicate qubits are specified.
    """
    require_distinct_qubits(qubits)

    require_same_length(
        state,
        qubits,
        names=("state", "qubits"),
    )

    if any(bit not in "01" for bit in state):
        raise ValueError("State must contain only '0' and '1'.")

    circuit.reset(qubits)

    for qubit, bit in zip(qubits, state):
        if bit == "1":
            circuit.x(qubit)


def uniform_superposition(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
) -> None:
    """Prepare a uniform superposition over the specified qubits.

    The qubits are assumed to initially be in the |0> state.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to place into uniform superposition.

    Raises:
        ValueError: If duplicate qubits are specified.
    """
    require_distinct_qubits(qubits)

    circuit.h(qubits)


def statevector(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
    statevector: StatevectorLike,
) -> None:
    """Prepare an arbitrary statevector on the specified qubits.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits on which to prepare the state.
        statevector: Statevector amplitudes.

    Raises:
        ValueError: If the statevector dimension does not match the
            number of qubits.
        ValueError: If duplicate qubits are specified.
    """
    require_distinct_qubits(qubits)

    require_length(
        statevector,
        2 ** len(qubits),
        name="statevector",
    )

    circuit.initialize(list(statevector), qubits)


def product_state(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
    states: Sequence[Sequence[complex]],
) -> None:
    """Prepare a product of arbitrary single-qubit states.

    Each single-qubit state is specified as [alpha, beta], representing
    alpha|0> + beta|1>.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to prepare.
        states: Single-qubit statevectors corresponding to each qubit.

    Raises:
        ValueError: If the number of states does not match the number
            of qubits.
        ValueError: If duplicate qubits are specified.
        ValueError: If any single-qubit state does not contain exactly two amplitudes.
    """
    require_distinct_qubits(qubits)

    require_same_length(
        states,
        qubits,
        names=("states", "qubits"),
    )

    for state in states:
        require_length(
            state,
            2,
            name="single-qubit statevector amplitudes",
        )

    for qubit, state in zip(qubits, states):
        circuit.initialize(state, [qubit])


def random_state(
    circuit: QuantumCircuit,
    qubits: Sequence[QubitSpecifier],
    seed: int | None = None,
) -> None:
    """Prepare a random pure state on the specified qubits.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits on which to prepare the state.
        seed: Optional random seed for reproducibility.

    Raises:
        ValueError: If no qubits are specified.
        ValueError: If duplicate qubits are specified.
    """
    require_non_empty(qubits, name="qubits")
    require_distinct_qubits(qubits)

    state = random_statevector(2 ** len(qubits), seed=seed)
    circuit.initialize(state, qubits)


def x_eigenstate(
    circuit: QuantumCircuit,
    qubit: QubitSpecifier,
    eigenvalue: Eigenvalue = 1,
) -> None:
    """Prepare an eigenstate of the Pauli-X operator.

    Args:
        circuit: Circuit to modify.
        qubit: Qubit to prepare.
        eigenvalue: Desired eigenvalue, either +1 or -1.

    Raises:
        ValueError: If eigenvalue is not +1 or -1.
    """
    require_choice(
        eigenvalue,
        (1, -1),
        name="eigenvalue",
    )

    circuit.reset(qubit)

    if eigenvalue == -1:
        circuit.x(qubit)

    circuit.h(qubit)


def y_eigenstate(
    circuit: QuantumCircuit,
    qubit: QubitSpecifier,
    eigenvalue: Eigenvalue = 1,
) -> None:
    """Prepare an eigenstate of the Pauli-Y operator.

    Args:
        circuit: Circuit to modify.
        qubit: Qubit to prepare.
        eigenvalue: Desired eigenvalue, either +1 or -1.

    Raises:
        ValueError: If eigenvalue is not +1 or -1.
    """
    require_choice(
        eigenvalue,
        (1, -1),
        name="eigenvalue",
    )

    circuit.reset(qubit)
    circuit.h(qubit)

    if eigenvalue == 1:
        circuit.s(qubit)
    else:
        circuit.sdg(qubit)


def z_eigenstate(
    circuit: QuantumCircuit,
    qubit: QubitSpecifier,
    eigenvalue: Eigenvalue = 1,
) -> None:
    """Prepare an eigenstate of the Pauli-Z operator.

    Args:
        circuit: Circuit to modify.
        qubit: Qubit to prepare.
        eigenvalue: Desired eigenvalue, either +1 or -1.

    Raises:
        ValueError: If eigenvalue is not +1 or -1.
    """
    require_choice(
        eigenvalue,
        (1, -1),
        name="eigenvalue",
    )

    circuit.reset(qubit)

    if eigenvalue == -1:
        circuit.x(qubit)


def bloch_state(
    circuit: QuantumCircuit,
    qubit: QubitSpecifier,
    theta: float,
    phi: float,
) -> None:
    """Prepare a single-qubit state using Bloch-sphere angles.

    Prepares, up to global phase, the state

        cos(theta / 2)|0> + exp(i * phi) sin(theta / 2)|1>.

    Args:
        circuit: Circuit to modify.
        qubit: Qubit to prepare.
        theta: Polar angle in radians.
        phi: Azimuthal angle in radians.
    """
    circuit.reset(qubit)
    circuit.ry(theta, qubit)
    circuit.rz(phi, qubit)
