"""Tests for qiskit_circuit_utils.preparation."""

import math

import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from qiskit_circuit_utils import preparation


def assert_state_equivalent(
    circuit: QuantumCircuit,
    expected: Statevector | list[complex],
) -> None:
    """Assert that a circuit produces the expected state."""
    actual = Statevector.from_instruction(circuit)

    if not isinstance(expected, Statevector):
        expected = Statevector(expected)

    assert actual.equiv(expected)


# ---------------------------------------------------------------------------
# Bell states
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("bell_state", "expected"),
    [
        ("phi+", [1, 0, 0, 1]),
        ("phi-", [1, 0, 0, -1]),
        ("psi+", [0, 1, 1, 0]),
        ("psi-", [0, 1, -1, 0]),
    ],
)
def test_bell_state(bell_state, expected):
    circuit = QuantumCircuit(2)

    preparation.bell_state(
        circuit,
        circuit.qubits,
        state=bell_state,
    )

    expected = [
        amplitude / math.sqrt(2)
        for amplitude in expected
    ]

    assert_state_equivalent(circuit, expected)


def test_bell_state_requires_two_qubits():
    circuit = QuantumCircuit(3)

    with pytest.raises(ValueError):
        preparation.bell_state(
            circuit,
            circuit.qubits,
        )


# ---------------------------------------------------------------------------
# GHZ state
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("num_qubits", [2, 3, 4, 5])
def test_ghz_state(num_qubits):
    circuit = QuantumCircuit(num_qubits)

    preparation.ghz_state(
        circuit,
        circuit.qubits,
    )

    expected = np.zeros(2**num_qubits, dtype=complex)
    expected[0] = 1 / math.sqrt(2)
    expected[-1] = 1 / math.sqrt(2)

    assert_state_equivalent(circuit, expected)


def test_ghz_state_requires_two_qubits():
    circuit = QuantumCircuit(1)

    with pytest.raises(ValueError):
        preparation.ghz_state(
            circuit,
            circuit.qubits,
        )


# ---------------------------------------------------------------------------
# W state
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("num_qubits", [2, 3, 4])
def test_w_state(num_qubits):
    circuit = QuantumCircuit(num_qubits)

    preparation.w_state(
        circuit,
        circuit.qubits,
    )

    actual = Statevector.from_instruction(circuit)

    expected = np.zeros(2**num_qubits, dtype=complex)

    for qubit in range(num_qubits):
        expected[1 << qubit] = 1 / math.sqrt(num_qubits)

    assert actual.equiv(Statevector(expected))


def test_w_state_requires_two_qubits():
    circuit = QuantumCircuit(1)

    with pytest.raises(ValueError):
        preparation.w_state(
            circuit,
            circuit.qubits,
        )


# ---------------------------------------------------------------------------
# Basic states
# ---------------------------------------------------------------------------


def test_zero_state():
    circuit = QuantumCircuit(3)

    # Start somewhere other than |000>.
    circuit.x(circuit.qubits)

    preparation.zero_state(
        circuit,
        circuit.qubits,
    )

    assert_state_equivalent(
        circuit,
        Statevector.from_label("000"),
    )


def test_one_state():
    circuit = QuantumCircuit(3)

    preparation.one_state(
        circuit,
        circuit.qubits,
    )

    assert_state_equivalent(
        circuit,
        Statevector.from_label("111"),
    )


def test_plus_state():
    circuit = QuantumCircuit(1)

    preparation.plus_state(
        circuit,
        circuit.qubits,
    )

    assert_state_equivalent(
        circuit,
        [
            1 / math.sqrt(2),
            1 / math.sqrt(2),
        ],
    )


def test_minus_state():
    circuit = QuantumCircuit(1)

    preparation.minus_state(
        circuit,
        circuit.qubits,
    )

    assert_state_equivalent(
        circuit,
        [
            1 / math.sqrt(2),
            -1 / math.sqrt(2),
        ],
    )


# ---------------------------------------------------------------------------
# Computational basis states
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "state",
    [
        "000",
        "001",
        "010",
        "011",
        "100",
        "101",
        "110",
        "111",
    ],
)
def test_basis_state(state):
    circuit = QuantumCircuit(3)

    preparation.basis_state(
        circuit,
        circuit.qubits,
        state,
    )

    # preparation.basis_state maps the string left-to-right onto
    # q0, q1, q2, while Qiskit displays basis labels as q2 q1 q0.
    expected = Statevector.from_label(state[::-1])

    assert_state_equivalent(circuit, expected)


def test_basis_state_rejects_wrong_length():
    circuit = QuantumCircuit(3)

    with pytest.raises(ValueError):
        preparation.basis_state(
            circuit,
            circuit.qubits,
            "10",
        )


@pytest.mark.parametrize(
    "state",
    [
        "10A",
        "12",
        "abc",
    ],
)
def test_basis_state_rejects_invalid_bits(state):
    circuit = QuantumCircuit(len(state))

    with pytest.raises(ValueError):
        preparation.basis_state(
            circuit,
            circuit.qubits,
            state,
        )


# ---------------------------------------------------------------------------
# Uniform superposition
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("num_qubits", [1, 2, 3, 4])
def test_uniform_superposition(num_qubits):
    circuit = QuantumCircuit(num_qubits)

    preparation.uniform_superposition(
        circuit,
        circuit.qubits,
    )

    amplitude = 1 / math.sqrt(2**num_qubits)

    expected = [
        amplitude
        for _ in range(2**num_qubits)
    ]

    assert_state_equivalent(circuit, expected)


# ---------------------------------------------------------------------------
# Arbitrary statevector
# ---------------------------------------------------------------------------


def test_statevector():
    circuit = QuantumCircuit(2)

    expected = np.array(
        [
            1 / math.sqrt(3),
            1j / math.sqrt(3),
            0,
            1 / math.sqrt(3),
        ],
        dtype=complex,
    )

    preparation.statevector(
        circuit,
        circuit.qubits,
        expected,
    )

    assert_state_equivalent(circuit, expected)


def test_statevector_rejects_wrong_dimension():
    circuit = QuantumCircuit(2)

    with pytest.raises(ValueError):
        preparation.statevector(
            circuit,
            circuit.qubits,
            [1, 0],
        )


# ---------------------------------------------------------------------------
# Product states
# ---------------------------------------------------------------------------


def test_product_state():
    circuit = QuantumCircuit(2)

    plus = [
        1 / math.sqrt(2),
        1 / math.sqrt(2),
    ]

    one = [0, 1]

    preparation.product_state(
        circuit,
        circuit.qubits,
        [plus, one],
    )
    
    # Qiskit's tensor ordering means q1 is the left-hand factor.
    expected = Statevector(one).tensor(
        Statevector(plus)
    )

    assert_state_equivalent(circuit, expected)


def test_product_state_rejects_wrong_number_of_states():
    circuit = QuantumCircuit(2)

    with pytest.raises(ValueError):
        preparation.product_state(
            circuit,
            circuit.qubits,
            [[1, 0]],
        )


def test_product_state_rejects_invalid_single_qubit_state():
    circuit = QuantumCircuit(1)

    with pytest.raises(ValueError):
        preparation.product_state(
            circuit,
            circuit.qubits,
            [[1, 0, 0]],
        )


# ---------------------------------------------------------------------------
# Random states
# ---------------------------------------------------------------------------


def test_random_state():
    circuit = QuantumCircuit(3)

    preparation.random_state(
        circuit,
        circuit.qubits,
        seed=42,
    )

    state = Statevector.from_instruction(circuit)

    assert len(state.data) == 8
    assert np.isclose(
        np.linalg.norm(state.data),
        1.0,
    )


def test_random_state_is_reproducible():
    circuit_a = QuantumCircuit(2)
    circuit_b = QuantumCircuit(2)

    preparation.random_state(
        circuit_a,
        circuit_a.qubits,
        seed=42,
    )

    preparation.random_state(
        circuit_b,
        circuit_b.qubits,
        seed=42,
    )

    state_a = Statevector.from_instruction(circuit_a)
    state_b = Statevector.from_instruction(circuit_b)

    assert state_a.equiv(state_b)


# ---------------------------------------------------------------------------
# Pauli eigenstates
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("eigenvalue", "expected"),
    [
        (
            1,
            [
                1 / math.sqrt(2),
                1 / math.sqrt(2),
            ],
        ),
        (
            -1,
            [
                1 / math.sqrt(2),
                -1 / math.sqrt(2),
            ],
        ),
    ],
)
def test_x_eigenstate(eigenvalue, expected):
    circuit = QuantumCircuit(1)

    preparation.x_eigenstate(
        circuit,
        circuit.qubits[0],
        eigenvalue,
    )

    assert_state_equivalent(circuit, expected)


@pytest.mark.parametrize(
    ("eigenvalue", "expected"),
    [
        (
            1,
            [
                1 / math.sqrt(2),
                1j / math.sqrt(2),
            ],
        ),
        (
            -1,
            [
                1 / math.sqrt(2),
                -1j / math.sqrt(2),
            ],
        ),
    ],
)
def test_y_eigenstate(eigenvalue, expected):
    circuit = QuantumCircuit(1)

    preparation.y_eigenstate(
        circuit,
        circuit.qubits[0],
        eigenvalue,
    )

    assert_state_equivalent(circuit, expected)


@pytest.mark.parametrize(
    ("eigenvalue", "expected"),
    [
        (1, [1, 0]),
        (-1, [0, 1]),
    ],
)
def test_z_eigenstate(eigenvalue, expected):
    circuit = QuantumCircuit(1)

    preparation.z_eigenstate(
        circuit,
        circuit.qubits[0],
        eigenvalue,
    )

    assert_state_equivalent(circuit, expected)


@pytest.mark.parametrize(
    "function",
    [
        preparation.x_eigenstate,
        preparation.y_eigenstate,
        preparation.z_eigenstate,
    ],
)
def test_eigenstate_rejects_invalid_eigenvalue(function):
    circuit = QuantumCircuit(1)

    with pytest.raises(ValueError):
        function(
            circuit,
            circuit.qubits[0],
            0,
        )


# ---------------------------------------------------------------------------
# Bloch states
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("theta", "phi"),
    [
        (0, 0),
        (math.pi, 0),
        (math.pi / 2, 0),
        (math.pi / 2, math.pi),
        (math.pi / 2, math.pi / 2),
        (math.pi / 3, math.pi / 4),
    ],
)
def test_bloch_state(theta, phi):
    circuit = QuantumCircuit(1)

    preparation.bloch_state(
        circuit,
        circuit.qubits[0],
        theta,
        phi,
    )

    expected = Statevector(
        [
            math.cos(theta / 2),
            np.exp(1j * phi) * math.sin(theta / 2),
        ]
    )

    assert_state_equivalent(circuit, expected)