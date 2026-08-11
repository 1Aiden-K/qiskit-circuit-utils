"""Tests for qiskit_circuit_utils.measurement."""

import math

import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from qiskit_circuit_utils import measurement, preparation


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def instruction_names(
    circuit: QuantumCircuit,
) -> list[str]:
    """Return the instruction names in a circuit."""
    return [
        instruction.operation.name
        for instruction in circuit.data
    ]


# ---------------------------------------------------------------------------
# Z-basis measurement
# ---------------------------------------------------------------------------


def test_z():
    circuit = QuantumCircuit(1, 1)

    measurement.z(
        circuit,
        circuit.qubits[0],
        circuit.clbits[0],
    )

    assert instruction_names(circuit) == [
        "measure",
    ]


def test_z_accepts_integer_specifiers():
    circuit = QuantumCircuit(1, 1)

    measurement.z(
        circuit,
        0,
        0,
    )

    assert instruction_names(circuit) == [
        "measure",
    ]


# ---------------------------------------------------------------------------
# X-basis measurement
# ---------------------------------------------------------------------------


def test_x():
    circuit = QuantumCircuit(1, 1)

    measurement.x(
        circuit,
        circuit.qubits[0],
        circuit.clbits[0],
    )

    assert instruction_names(circuit) == [
        "h",
        "measure",
    ]


def test_x_accepts_integer_specifiers():
    circuit = QuantumCircuit(1, 1)

    measurement.x(
        circuit,
        0,
        0,
    )

    assert instruction_names(circuit) == [
        "h",
        "measure",
    ]


# ---------------------------------------------------------------------------
# Y-basis measurement
# ---------------------------------------------------------------------------


def test_y():
    circuit = QuantumCircuit(1, 1)

    measurement.y(
        circuit,
        circuit.qubits[0],
        circuit.clbits[0],
    )

    assert instruction_names(circuit) == [
        "sdg",
        "h",
        "measure",
    ]


def test_y_accepts_integer_specifiers():
    circuit = QuantumCircuit(1, 1)

    measurement.y(
        circuit,
        0,
        0,
    )

    assert instruction_names(circuit) == [
        "sdg",
        "h",
        "measure",
    ]


# ---------------------------------------------------------------------------
# Bulk measurements
# ---------------------------------------------------------------------------


def test_z_all():
    circuit = QuantumCircuit(3, 3)

    measurement.z_all(
        circuit,
        circuit.qubits,
        circuit.clbits,
    )

    assert instruction_names(circuit) == [
        "measure",
        "measure",
        "measure",
    ]


def test_x_all():
    circuit = QuantumCircuit(3, 3)

    measurement.x_all(
        circuit,
        circuit.qubits,
        circuit.clbits,
    )

    assert instruction_names(circuit) == [
        "h",
        "h",
        "h",
        "measure",
        "measure",
        "measure",
    ]


def test_y_all():
    circuit = QuantumCircuit(3, 3)

    measurement.y_all(
        circuit,
        circuit.qubits,
        circuit.clbits,
    )

    assert instruction_names(circuit) == [
        "sdg",
        "sdg",
        "sdg",
        "h",
        "h",
        "h",
        "measure",
        "measure",
        "measure",
    ]


@pytest.mark.parametrize(
    "function",
    [
        measurement.x_all,
        measurement.y_all,
        measurement.z_all,
    ],
)
def test_all_rejects_mismatched_lengths(function):
    circuit = QuantumCircuit(3, 2)

    with pytest.raises(ValueError):
        function(
            circuit,
            circuit.qubits,
            circuit.clbits,
        )


# ---------------------------------------------------------------------------
# Arbitrary Pauli measurement
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("basis", "expected"),
    [
        ("X", ["h", "measure"]),
        ("Y", ["sdg", "h", "measure"]),
        ("Z", ["measure"]),
    ],
)
def test_pauli(basis, expected):
    circuit = QuantumCircuit(1, 1)

    measurement.pauli(
        circuit,
        0,
        0,
        basis,
    )

    assert instruction_names(circuit) == expected


@pytest.mark.parametrize(
    ("basis", "expected"),
    [
        ("x", ["h", "measure"]),
        ("y", ["sdg", "h", "measure"]),
        ("z", ["measure"]),
    ],
)
def test_pauli_accepts_lowercase(basis, expected):
    circuit = QuantumCircuit(1, 1)

    measurement.pauli(
        circuit,
        0,
        0,
        basis,
    )

    assert instruction_names(circuit) == expected


@pytest.mark.parametrize(
    "basis",
    [
        "",
        "A",
        "XX",
    ],
)
def test_pauli_rejects_invalid_basis(basis):
    circuit = QuantumCircuit(1, 1)

    with pytest.raises(ValueError):
        measurement.pauli(
            circuit,
            0,
            0,
            basis,
        )


# ---------------------------------------------------------------------------
# Pair-based measurement
# ---------------------------------------------------------------------------


def test_z_pairs():
    circuit = QuantumCircuit(3, 3)

    measurement.z_pairs(
        circuit,
        [
            (0, 2),
            (2, 0),
        ],
    )

    assert instruction_names(circuit) == [
        "measure",
        "measure",
    ]


def test_x_pairs():
    circuit = QuantumCircuit(3, 3)

    measurement.x_pairs(
        circuit,
        [
            (0, 2),
            (2, 0),
        ],
    )

    assert instruction_names(circuit) == [
        "h",
        "measure",
        "h",
        "measure",
    ]


def test_y_pairs():
    circuit = QuantumCircuit(3, 3)

    measurement.y_pairs(
        circuit,
        [
            (0, 2),
            (2, 0),
        ],
    )

    assert instruction_names(circuit) == [
        "sdg",
        "h",
        "measure",
        "sdg",
        "h",
        "measure",
    ]


# ---------------------------------------------------------------------------
# Measurement mappings
# ---------------------------------------------------------------------------


def test_z_maps_correct_qubit_to_clbit():
    circuit = QuantumCircuit(3, 3)

    measurement.z(
        circuit,
        circuit.qubits[2],
        circuit.clbits[1],
    )

    instruction = circuit.data[-1]

    assert instruction.qubits == (
        circuit.qubits[2],
    )

    assert instruction.clbits == (
        circuit.clbits[1],
    )


def test_z_all_preserves_mapping_order():
    circuit = QuantumCircuit(3, 3)

    measurement.z_all(
        circuit,
        [
            circuit.qubits[2],
            circuit.qubits[0],
        ],
        [
            circuit.clbits[0],
            circuit.clbits[2],
        ],
    )

    measurements = [
        instruction
        for instruction in circuit.data
        if instruction.operation.name == "measure"
    ]

    assert measurements[0].qubits == (
        circuit.qubits[2],
    )
    assert measurements[0].clbits == (
        circuit.clbits[0],
    )

    assert measurements[1].qubits == (
        circuit.qubits[0],
    )
    assert measurements[1].clbits == (
        circuit.clbits[2],
    )


# ---------------------------------------------------------------------------
# Bell-basis measurement
# ---------------------------------------------------------------------------


def test_bell_basis_instructions():
    circuit = QuantumCircuit(2, 2)

    measurement.bell_basis(
        circuit,
        circuit.qubits,
        circuit.clbits,
    )

    assert instruction_names(circuit) == [
        "cx",
        "h",
        "measure",
        "measure",
    ]


def test_bell_basis_requires_two_qubits():
    circuit = QuantumCircuit(3, 2)

    with pytest.raises(ValueError):
        measurement.bell_basis(
            circuit,
            circuit.qubits,
            circuit.clbits,
        )


def test_bell_basis_requires_two_clbits():
    circuit = QuantumCircuit(2, 3)

    with pytest.raises(ValueError):
        measurement.bell_basis(
            circuit,
            circuit.qubits,
            circuit.clbits,
        )


@pytest.mark.parametrize(
    ("bell_state", "expected"),
    [
        ("phi+", "00"),
        ("phi-", "01"),
        ("psi+", "10"),
        ("psi-", "11"),
    ],
)
def test_bell_basis_transform(
    bell_state,
    expected,
):
    circuit = QuantumCircuit(2, 2)

    preparation.bell_state(
        circuit,
        circuit.qubits,
        state=bell_state,
    )

    measurement.bell_basis(
        circuit,
        circuit.qubits,
        circuit.clbits,
    )

    # Remove final measurements so Statevector can inspect the
    # Bell-to-computational-basis transformation.
    transformed = circuit.remove_final_measurements(
        inplace=False
    )

    actual = Statevector.from_instruction(transformed)

    assert actual.equiv(
        Statevector.from_label(expected)
    )