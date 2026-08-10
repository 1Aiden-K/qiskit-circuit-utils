"""Utilities for preparing states across qubits."""

import math
from collections.abc import Sequence
from typing import Literal

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Qubit
from qiskit.quantum_info import random_statevector

BellState = Literal["phi+", "phi-", "psi+", "psi-"]

def bell_state(
    circuit: QuantumCircuit,
    qubits: Sequence[Qubit],
    state: BellState = "phi+",
) -> None:
    """Prepare two qubits in one of the four Bell states.

        The qubits are assumed to initially be in the |00> state.

        Args:
            circuit: Circuit to modify.
            qubits: Qubits to prepare. Exactly two qubits are required.
            state: Bell state to prepare. One of:
                - "phi+": (|00> + |11>) / sqrt(2)
                - "phi-": (|00> - |11>) / sqrt(2)
                - "psi+": (|01> + |10>) / sqrt(2)
                - "psi-": (|01> - |10>) / sqrt(2)

        Raises:
            ValueError: If an unsupported Bell state is specified.
            ValueError: If more or less than two qubits are specified.
    """
    if len(qubits) != 2:
        raise ValueError(
            f"Bell state requires exactly 2 qubits, got {len(qubits)}."
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
    elif state != "phi+":
        raise ValueError(f"Unsupported Bell state: {state!r}")

def ghz_state(
    circuit: QuantumCircuit,
    qubits: Sequence[Qubit],
) -> None:
    """Prepare the specified qubits in a GHZ state.

    The qubits are assumed to initially be in the |0> state.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to prepare. At least two qubits are required.

    Raises:
        ValueError: If fewer than two qubits are specified.
    """
    if len(qubits) < 2:
        raise ValueError(
            f"GHZ state requires at least 2 qubits, got {len(qubits)}."
        )

    circuit.h(qubits[0])

    for control, target in zip(qubits, qubits[1:]):
        circuit.cx(control, target)

def w_state(
    circuit: QuantumCircuit,
    qubits: Sequence[Qubit],
) -> None:
    """Prepare the specified qubits in a W state.

    The qubits are assumed to initially be in the |0> state.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to prepare. At least two qubits are required.

    Raises:
        ValueError: If fewer than two qubits are specified.
    """
    if len(qubits) < 2:
        raise ValueError(
            f"W state requires at least 2 qubits, got {len(qubits)}."
        )

    n = len(qubits)

    circuit.x(qubits[0])

    for i in range(n - 1):
        theta = 2 * math.acos(1 / math.sqrt(n - i))

        circuit.ry(-theta, qubits[i + 1])
        circuit.cz(qubits[i], qubits[i + 1])
        circuit.ry(theta, qubits[i + 1])

        circuit.cx(qubits[i + 1], qubits[i])

    circuit.x(qubits[-1])

def zero_state(
    circuit: QuantumCircuit,
    qubits: Sequence[Qubit],
) -> None:
    """Prepare the specified qubits in the |0> state.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to prepare.
    """
    circuit.reset(qubits)

def one_state(
    circuit: QuantumCircuit,
    qubits: Sequence[Qubit],
) -> None:
    """Prepare the specified qubits in the |1> state.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to prepare.
    """
    circuit.reset(qubits)
    circuit.x(qubits)

def plus_state(
    circuit: QuantumCircuit,
    qubits: Sequence[Qubit],
) -> None:
    """Prepare the specified qubits in the |+> state.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to prepare.
    """
    circuit.reset(qubits)
    circuit.h(qubits)

def minus_state(
    circuit: QuantumCircuit,
    qubits: Sequence[Qubit],
) -> None:
    """Prepare the specified qubits in the |-> state.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to prepare.
    """
    circuit.reset(qubits)
    circuit.x(qubits)
    circuit.h(qubits)

def basis_state(
    circuit: QuantumCircuit,
    qubits: Sequence[Qubit],
    state: str,
) -> None:
    """Prepare a computational basis state.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to prepare.
        state: Bit string describing the state, such as "101".

    Raises:
        ValueError: If the bit string length does not match the number
            of qubits or contains characters other than "0" and "1".
    """
    if len(state) != len(qubits):
        raise ValueError(
            f"State requires {len(state)} qubits, got {len(qubits)}."
        )

    if any(bit not in "01" for bit in state):
        raise ValueError("State must contain only '0' and '1'.")

    circuit.reset(qubits)

    for qubit, bit in zip(qubits, state):
        if bit == "1":
            circuit.x(qubit)

def uniform_superposition(
    circuit: QuantumCircuit,
    qubits: Sequence[Qubit],
) -> None:
    """Prepare a uniform superposition over the specified qubits.

    The qubits are assumed to initially be in the |0> state.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits to place into uniform superposition.
    """
    circuit.h(qubits)

def statevector(
    circuit: QuantumCircuit,
    qubits: Sequence[Qubit],
    statevector: Sequence[complex],
) -> None:
    """Prepare an arbitrary statevector on the specified qubits.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits on which to prepare the state.
        statevector: Statevector amplitudes.

    Raises:
        ValueError: If the statevector dimension does not match the
            number of qubits.
    """
    expected_size = 2 ** len(qubits)

    if len(statevector) != expected_size:
        raise ValueError(
            f"Statevector must contain {expected_size} amplitudes, "
            f"got {len(statevector)}."
        )

    circuit.initialize(statevector, qubits)

def product_state(
    circuit: QuantumCircuit,
    qubits: Sequence[Qubit],
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
            of qubits or a state does not contain exactly two amplitudes.
    """
    if len(states) != len(qubits):
        raise ValueError(
            f"Expected {len(qubits)} states, got {len(states)}."
        )

    for qubit, state in zip(qubits, states):
        if len(state) != 2:
            raise ValueError(
                "Each single-qubit state must contain exactly 2 amplitudes."
            )

        circuit.initialize(state, [qubit])

def random_state(
    circuit: QuantumCircuit,
    qubits: Sequence[Qubit],
    seed: int | None = None,
) -> None:
    """Prepare a random pure state on the specified qubits.

    Args:
        circuit: Circuit to modify.
        qubits: Qubits on which to prepare the state.
        seed: Optional random seed for reproducibility.
    """
    if not qubits:
        raise ValueError("At least one qubit is required.")

    state = random_statevector(2 ** len(qubits), seed=seed)

    circuit.initialize(state.data, qubits)

def x_eigenstate(
    circuit: QuantumCircuit,
    qubit: Qubit,
    eigenvalue: Literal[1, -1] = 1,
) -> None:
    """Prepare an eigenstate of the Pauli-X operator.

    Args:
        circuit: Circuit to modify.
        qubit: Qubit to prepare.
        eigenvalue: Desired eigenvalue, either +1 or -1.

    Raises:
        ValueError: If eigenvalue is not +1 or -1.
    """
    if eigenvalue not in (1, -1):
        raise ValueError("Eigenvalue must be +1 or -1.")

    circuit.reset(qubit)

    if eigenvalue == -1:
        circuit.x(qubit)

    circuit.h(qubit)

def y_eigenstate(
    circuit: QuantumCircuit,
    qubit: Qubit,
    eigenvalue: Literal[1, -1] = 1,
) -> None:
    """Prepare an eigenstate of the Pauli-Y operator.

    Args:
        circuit: Circuit to modify.
        qubit: Qubit to prepare.
        eigenvalue: Desired eigenvalue, either +1 or -1.

    Raises:
        ValueError: If eigenvalue is not +1 or -1.
    """
    if eigenvalue not in (1, -1):
        raise ValueError("Eigenvalue must be +1 or -1.")

    circuit.reset(qubit)
    circuit.h(qubit)

    if eigenvalue == 1:
        circuit.s(qubit)
    else:
        circuit.sdg(qubit)

def z_eigenstate(
    circuit: QuantumCircuit,
    qubit: Qubit,
    eigenvalue: Literal[1, -1] = 1,
) -> None:
    """Prepare an eigenstate of the Pauli-Z operator.

    Args:
        circuit: Circuit to modify.
        qubit: Qubit to prepare.
        eigenvalue: Desired eigenvalue, either +1 or -1.

    Raises:
        ValueError: If eigenvalue is not +1 or -1.
    """
    if eigenvalue not in (1, -1):
        raise ValueError("Eigenvalue must be +1 or -1.")

    circuit.reset(qubit)

    if eigenvalue == -1:
        circuit.x(qubit)

def bloch_state(
    circuit: QuantumCircuit,
    qubit: Qubit,
    theta: float,
    phi: float,
) -> None:
    """Prepare a single-qubit state using Bloch-sphere angles.

    Prepares the state

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