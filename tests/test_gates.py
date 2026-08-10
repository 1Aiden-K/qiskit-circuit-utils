"""Tests for qiskit_circuit_utils.gates."""

import math

import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

from qiskit_circuit_utils import gates


def assert_operators_equivalent(
    actual: QuantumCircuit,
    expected: QuantumCircuit,
) -> None:
    """Assert that two circuits implement equivalent operators."""
    assert Operator(actual).equiv(Operator(expected))


# ---------------------------------------------------------------------------
# Single-qubit gates
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("gate_function", "qiskit_method"),
    [
        (gates.x_all, "x"),
        (gates.y_all, "y"),
        (gates.z_all, "z"),
        (gates.h_all, "h"),
        (gates.s_all, "s"),
        (gates.sdg_all, "sdg"),
        (gates.t_all, "t"),
        (gates.tdg_all, "tdg"),
        (gates.sx_all, "sx"),
        (gates.sxdg_all, "sxdg"),
    ],
)
def test_single_qubit_gate_all(
    gate_function,
    qiskit_method,
):
    circuit = QuantumCircuit(3)
    expected = QuantumCircuit(3)

    gate_function(
        circuit,
        circuit.qubits,
    )

    method = getattr(expected, qiskit_method)

    for qubit in expected.qubits:
        method(qubit)

    assert_operators_equivalent(circuit, expected)


# ---------------------------------------------------------------------------
# Integer qubit specifiers
# ---------------------------------------------------------------------------


def test_h_all_accepts_integer_specifiers():
    circuit = QuantumCircuit(3)
    expected = QuantumCircuit(3)

    gates.h_all(
        circuit,
        [0, 2],
    )

    expected.h(0)
    expected.h(2)

    assert_operators_equivalent(circuit, expected)


def test_h_all_accepts_qubit_objects():
    circuit = QuantumCircuit(3)
    expected = QuantumCircuit(3)

    gates.h_all(
        circuit,
        [
            circuit.qubits[0],
            circuit.qubits[2],
        ],
    )

    expected.h(0)
    expected.h(2)

    assert_operators_equivalent(circuit, expected)


# ---------------------------------------------------------------------------
# Rotation gates
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("gate_function", "qiskit_method"),
    [
        (gates.rx_all, "rx"),
        (gates.ry_all, "ry"),
        (gates.rz_all, "rz"),
        (gates.p_all, "p"),
    ],
)
@pytest.mark.parametrize(
    "theta",
    [
        0.0,
        math.pi / 4,
        math.pi / 2,
        math.pi,
        -math.pi / 3,
    ],
)
def test_rotation_gate_all(
    gate_function,
    qiskit_method,
    theta,
):
    circuit = QuantumCircuit(3)
    expected = QuantumCircuit(3)

    gate_function(
        circuit,
        circuit.qubits,
        theta,
    )

    method = getattr(expected, qiskit_method)

    for qubit in expected.qubits:
        method(theta, qubit)

    assert_operators_equivalent(circuit, expected)


# ---------------------------------------------------------------------------
# U gate
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("theta", "phi", "lam"),
    [
        (0.0, 0.0, 0.0),
        (math.pi / 2, 0.0, 0.0),
        (math.pi / 2, math.pi / 4, math.pi),
        (math.pi, math.pi / 2, -math.pi / 3),
    ],
)
def test_u_all(theta, phi, lam):
    circuit = QuantumCircuit(3)
    expected = QuantumCircuit(3)

    gates.u_all(
        circuit,
        circuit.qubits,
        theta,
        phi,
        lam,
    )

    for qubit in expected.qubits:
        expected.u(
            theta,
            phi,
            lam,
            qubit,
        )

    assert_operators_equivalent(circuit, expected)


# ---------------------------------------------------------------------------
# Controlled gates
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("gate_function", "qiskit_method"),
    [
        (gates.cx_pairs, "cx"),
        (gates.cy_pairs, "cy"),
        (gates.cz_pairs, "cz"),
        (gates.ch_pairs, "ch"),
    ],
)
def test_controlled_gate_pairs(
    gate_function,
    qiskit_method,
):
    circuit = QuantumCircuit(4)
    expected = QuantumCircuit(4)

    pairs = [
        (0, 1),
        (2, 3),
    ]

    gate_function(
        circuit,
        pairs,
    )

    method = getattr(expected, qiskit_method)

    for control, target in pairs:
        method(control, target)

    assert_operators_equivalent(circuit, expected)


# ---------------------------------------------------------------------------
# Controlled parameterized gates
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("gate_function", "qiskit_method"),
    [
        (gates.cp_pairs, "cp"),
        (gates.crx_pairs, "crx"),
        (gates.cry_pairs, "cry"),
        (gates.crz_pairs, "crz"),
    ],
)
@pytest.mark.parametrize(
    "theta",
    [
        math.pi / 4,
        math.pi / 2,
        math.pi,
        -math.pi / 3,
    ],
)
def test_controlled_rotation_pairs(
    gate_function,
    qiskit_method,
    theta,
):
    circuit = QuantumCircuit(4)
    expected = QuantumCircuit(4)

    pairs = [
        (0, 1),
        (2, 3),
    ]

    gate_function(
        circuit,
        pairs,
        theta,
    )

    method = getattr(expected, qiskit_method)

    for control, target in pairs:
        method(
            theta,
            control,
            target,
        )

    assert_operators_equivalent(circuit, expected)


# ---------------------------------------------------------------------------
# SWAP gates
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("gate_function", "qiskit_method"),
    [
        (gates.swap_pairs, "swap"),
        (gates.iswap_pairs, "iswap"),
    ],
)
def test_swap_pairs(
    gate_function,
    qiskit_method,
):
    circuit = QuantumCircuit(4)
    expected = QuantumCircuit(4)

    pairs = [
        (0, 1),
        (2, 3),
    ]

    gate_function(
        circuit,
        pairs,
    )

    method = getattr(expected, qiskit_method)

    for q0, q1 in pairs:
        method(q0, q1)

    assert_operators_equivalent(circuit, expected)


# ---------------------------------------------------------------------------
# Two-qubit rotation gates
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("gate_function", "qiskit_method"),
    [
        (gates.rxx_pairs, "rxx"),
        (gates.ryy_pairs, "ryy"),
        (gates.rzz_pairs, "rzz"),
        (gates.rzx_pairs, "rzx"),
    ],
)
@pytest.mark.parametrize(
    "theta",
    [
        math.pi / 4,
        math.pi / 2,
        math.pi,
        -math.pi / 3,
    ],
)
def test_two_qubit_rotation_pairs(
    gate_function,
    qiskit_method,
    theta,
):
    circuit = QuantumCircuit(4)
    expected = QuantumCircuit(4)

    pairs = [
        (0, 1),
        (2, 3),
    ]

    gate_function(
        circuit,
        pairs,
        theta,
    )

    method = getattr(expected, qiskit_method)

    for q0, q1 in pairs:
        method(
            theta,
            q0,
            q1,
        )

    assert_operators_equivalent(circuit, expected)


# ---------------------------------------------------------------------------
# Three-qubit gates
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("gate_function", "qiskit_method"),
    [
        (gates.ccx_triples, "ccx"),
        (gates.cswap_triples, "cswap"),
    ],
)
def test_three_qubit_gate_triples(
    gate_function,
    qiskit_method,
):
    circuit = QuantumCircuit(6)
    expected = QuantumCircuit(6)

    triples = [
        (0, 1, 2),
        (3, 4, 5),
    ]

    gate_function(
        circuit,
        triples,
    )

    method = getattr(expected, qiskit_method)

    for q0, q1, q2 in triples:
        method(q0, q1, q2)

    assert_operators_equivalent(circuit, expected)


# ---------------------------------------------------------------------------
# Iterable support
# ---------------------------------------------------------------------------


def test_h_all_accepts_generator():
    circuit = QuantumCircuit(3)
    expected = QuantumCircuit(3)

    qubits = (i for i in range(3))

    gates.h_all(
        circuit,
        qubits,
    )

    expected.h([0, 1, 2])

    assert_operators_equivalent(circuit, expected)


def test_cx_pairs_accepts_generator():
    circuit = QuantumCircuit(4)
    expected = QuantumCircuit(4)

    pairs = (
        pair
        for pair in [
            (0, 1),
            (2, 3),
        ]
    )

    gates.cx_pairs(
        circuit,
        pairs,
    )

    expected.cx(0, 1)
    expected.cx(2, 3)

    assert_operators_equivalent(circuit, expected)


# ---------------------------------------------------------------------------
# Empty collections
# ---------------------------------------------------------------------------


def test_h_all_accepts_empty_iterable():
    circuit = QuantumCircuit(2)

    gates.h_all(
        circuit,
        [],
    )

    expected = QuantumCircuit(2)

    assert_operators_equivalent(circuit, expected)


def test_cx_pairs_accepts_empty_iterable():
    circuit = QuantumCircuit(2)

    gates.cx_pairs(
        circuit,
        [],
    )

    expected = QuantumCircuit(2)

    assert_operators_equivalent(circuit, expected)