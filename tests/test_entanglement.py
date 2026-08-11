"""Tests for qiskit_circuit_utils.entanglement."""

import math

import pytest
from qiskit import QuantumCircuit
from qiskit.circuit.controlflow import IfElseOp
from qiskit.quantum_info import Statevector

from qiskit_circuit_utils import entanglement, preparation

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def assert_state_equivalent(
    circuit: QuantumCircuit,
    expected: Statevector | list[complex],
) -> None:
    """Assert that a circuit produces the expected state."""
    actual = Statevector.from_instruction(circuit)

    if not isinstance(expected, Statevector):
        expected = Statevector(expected)

    assert actual.equiv(expected)


def instruction_names(
    circuit: QuantumCircuit,
) -> list[str]:
    """Return the top-level instruction names in a circuit."""
    return [instruction.operation.name for instruction in circuit.data]


# ---------------------------------------------------------------------------
# Distribute
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("num_qubits", [2, 3, 4, 5])
def test_distribute_creates_ghz_state(num_qubits):
    circuit = QuantumCircuit(num_qubits)

    entanglement.distribute(
        circuit,
        circuit.qubits,
    )

    expected = [0j] * (2**num_qubits)
    expected[0] = 1 / math.sqrt(2)
    expected[-1] = 1 / math.sqrt(2)

    assert_state_equivalent(
        circuit,
        expected,
    )


def test_distribute_requires_two_qubits():
    circuit = QuantumCircuit(1)

    with pytest.raises(ValueError):
        entanglement.distribute(
            circuit,
            circuit.qubits,
        )


def test_distribute_accepts_integer_specifiers():
    circuit = QuantumCircuit(3)

    entanglement.distribute(
        circuit,
        [0, 1, 2],
    )

    expected = [
        1 / math.sqrt(2),
        0,
        0,
        0,
        0,
        0,
        0,
        1 / math.sqrt(2),
    ]

    assert_state_equivalent(
        circuit,
        expected,
    )


# ---------------------------------------------------------------------------
# Extend
# ---------------------------------------------------------------------------


def test_extend_ghz_state():
    circuit = QuantumCircuit(4)

    # Existing GHZ state across q0 and q1.
    preparation.bell_state(
        circuit,
        circuit.qubits[:2],
    )

    entanglement.extend(
        circuit,
        circuit.qubits[0],
        circuit.qubits[2:],
    )

    expected = [
        1 / math.sqrt(2),
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1 / math.sqrt(2),
    ]

    assert_state_equivalent(
        circuit,
        expected,
    )


def test_extend_accepts_integer_specifiers():
    circuit = QuantumCircuit(3)

    preparation.plus_state(
        circuit,
        [circuit.qubits[0]],
    )

    entanglement.extend(
        circuit,
        0,
        [1, 2],
    )

    expected = [
        1 / math.sqrt(2),
        0,
        0,
        0,
        0,
        0,
        0,
        1 / math.sqrt(2),
    ]

    assert_state_equivalent(
        circuit,
        expected,
    )


def test_extend_accepts_empty_targets():
    circuit = QuantumCircuit(1)

    preparation.plus_state(
        circuit,
        circuit.qubits,
    )

    expected = Statevector.from_instruction(circuit)

    entanglement.extend(
        circuit,
        circuit.qubits[0],
        [],
    )

    actual = Statevector.from_instruction(circuit)

    assert actual.equiv(expected)


# ---------------------------------------------------------------------------
# Connect
# ---------------------------------------------------------------------------


def test_connect_creates_bell_state():
    circuit = QuantumCircuit(2)

    preparation.plus_state(
        circuit,
        [circuit.qubits[0]],
    )

    entanglement.connect(
        circuit,
        circuit.qubits,
    )

    expected = [
        1 / math.sqrt(2),
        0,
        0,
        1 / math.sqrt(2),
    ]

    assert_state_equivalent(
        circuit,
        expected,
    )


def test_connect_requires_two_qubits():
    circuit = QuantumCircuit(3)

    with pytest.raises(ValueError):
        entanglement.connect(
            circuit,
            circuit.qubits,
        )


def test_connect_accepts_integer_specifiers():
    circuit = QuantumCircuit(2)

    circuit.h(0)

    entanglement.connect(
        circuit,
        [0, 1],
    )

    expected = [
        1 / math.sqrt(2),
        0,
        0,
        1 / math.sqrt(2),
    ]

    assert_state_equivalent(
        circuit,
        expected,
    )


# ---------------------------------------------------------------------------
# Disconnect
# ---------------------------------------------------------------------------


def test_disconnect_reverses_connect():
    circuit = QuantumCircuit(2)

    preparation.plus_state(
        circuit,
        [circuit.qubits[0]],
    )

    before = Statevector.from_instruction(circuit)

    entanglement.connect(
        circuit,
        circuit.qubits,
    )

    entanglement.disconnect(
        circuit,
        circuit.qubits,
    )

    after = Statevector.from_instruction(circuit)

    assert after.equiv(before)


def test_disconnect_bell_state():
    circuit = QuantumCircuit(2)

    preparation.bell_state(
        circuit,
        circuit.qubits,
    )

    entanglement.disconnect(
        circuit,
        circuit.qubits,
    )

    expected = Statevector(
        [
            1 / math.sqrt(2),
            1 / math.sqrt(2),
            0,
            0,
        ]
    )

    assert_state_equivalent(
        circuit,
        expected,
    )


def test_disconnect_requires_two_qubits():
    circuit = QuantumCircuit(3)

    with pytest.raises(ValueError):
        entanglement.disconnect(
            circuit,
            circuit.qubits,
        )


# ---------------------------------------------------------------------------
# Transfer
# ---------------------------------------------------------------------------


def test_transfer():
    circuit = QuantumCircuit(2)

    # Put q0 into |1>.
    circuit.x(0)

    entanglement.transfer(
        circuit,
        circuit.qubits,
    )

    # q0 = |0>, q1 = |1>.
    assert_state_equivalent(
        circuit,
        Statevector.from_label("10"),
    )


def test_transfer_arbitrary_state():
    circuit = QuantumCircuit(2)

    theta = 0.73
    phi = 1.21

    preparation.bloch_state(
        circuit,
        circuit.qubits[0],
        theta,
        phi,
    )

    source_state = Statevector(
        [
            math.cos(theta / 2),
            complex(
                math.cos(phi),
                math.sin(phi),
            )
            * math.sin(theta / 2),
        ]
    )

    entanglement.transfer(
        circuit,
        circuit.qubits,
    )

    # q0 becomes |0>; q1 receives the original q0 state.
    expected = source_state.tensor(Statevector.from_label("0"))

    assert_state_equivalent(
        circuit,
        expected,
    )


def test_transfer_requires_two_qubits():
    circuit = QuantumCircuit(3)

    with pytest.raises(ValueError):
        entanglement.transfer(
            circuit,
            circuit.qubits,
        )


# ---------------------------------------------------------------------------
# Teleportation
# ---------------------------------------------------------------------------


def test_teleport_instructions():
    circuit = QuantumCircuit(3, 2)

    entanglement.teleport(
        circuit,
        circuit.qubits,
        circuit.clbits,
    )

    names = instruction_names(circuit)

    # Bell-pair preparation.
    assert names[0:2] == [
        "h",
        "cx",
    ]

    # Bell-basis transformation + measurements.
    assert names[2:6] == [
        "cx",
        "h",
        "measure",
        "measure",
    ]

    # X and Z feed-forward corrections.
    assert isinstance(
        circuit.data[6].operation,
        IfElseOp,
    )

    assert isinstance(
        circuit.data[7].operation,
        IfElseOp,
    )


def test_teleport_corrections():
    circuit = QuantumCircuit(3, 2)

    entanglement.teleport(
        circuit,
        circuit.qubits,
        circuit.clbits,
    )

    x_correction = circuit.data[-2].operation
    z_correction = circuit.data[-1].operation

    phase_bit = circuit.clbits[0]
    parity_bit = circuit.clbits[1]

    assert isinstance(
        x_correction,
        IfElseOp,
    )
    assert isinstance(
        z_correction,
        IfElseOp,
    )

    assert x_correction.condition == (
        parity_bit,
        1,
    )

    assert z_correction.condition == (
        phase_bit,
        1,
    )

    assert x_correction.blocks[0].data[0].operation.name == "x"

    assert z_correction.blocks[0].data[0].operation.name == "z"


def test_teleport_requires_three_qubits():
    circuit = QuantumCircuit(2, 2)

    with pytest.raises(ValueError):
        entanglement.teleport(
            circuit,
            circuit.qubits,
            circuit.clbits,
        )


def test_teleport_requires_two_clbits():
    circuit = QuantumCircuit(3, 1)

    with pytest.raises(ValueError):
        entanglement.teleport(
            circuit,
            circuit.qubits,
            circuit.clbits,
        )


# ---------------------------------------------------------------------------
# Entanglement swapping
# ---------------------------------------------------------------------------


def test_swap_instructions():
    circuit = QuantumCircuit(3, 2)

    entanglement.swap(
        circuit,
        circuit.qubits,
        circuit.clbits,
    )

    names = instruction_names(circuit)

    assert names[:4] == [
        "cx",
        "h",
        "measure",
        "measure",
    ]

    assert isinstance(
        circuit.data[4].operation,
        IfElseOp,
    )

    assert isinstance(
        circuit.data[5].operation,
        IfElseOp,
    )


def test_swap_corrections():
    circuit = QuantumCircuit(3, 2)

    entanglement.swap(
        circuit,
        circuit.qubits,
        circuit.clbits,
    )

    x_correction = circuit.data[-2].operation
    z_correction = circuit.data[-1].operation

    phase_bit = circuit.clbits[0]
    parity_bit = circuit.clbits[1]

    assert x_correction.condition == (
        parity_bit,
        1,
    )

    assert z_correction.condition == (
        phase_bit,
        1,
    )

    assert x_correction.blocks[0].data[0].operation.name == "x"

    assert z_correction.blocks[0].data[0].operation.name == "z"


def test_swap_requires_three_qubits():
    circuit = QuantumCircuit(2, 2)

    with pytest.raises(ValueError):
        entanglement.swap(
            circuit,
            circuit.qubits,
            circuit.clbits,
        )


def test_swap_requires_two_clbits():
    circuit = QuantumCircuit(3, 1)

    with pytest.raises(ValueError):
        entanglement.swap(
            circuit,
            circuit.qubits,
            circuit.clbits,
        )


# ---------------------------------------------------------------------------
# Superdense coding
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("message", "encoding"),
    [
        ([False, False], []),
        ([False, True], ["x"]),
        ([True, False], ["z"]),
        ([True, True], ["x", "z"]),
    ],
)
def test_superdense_code_instructions(
    message,
    encoding,
):
    circuit = QuantumCircuit(2, 2)

    entanglement.superdense_code(
        circuit,
        circuit.qubits,
        circuit.clbits,
        message,
    )

    names = instruction_names(circuit)

    assert names == [
        "h",
        "cx",
        *encoding,
        "cx",
        "h",
        "measure",
        "measure",
    ]


@pytest.mark.parametrize(
    "message",
    [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
    ],
)
def test_superdense_code_decodes_message(message):
    circuit = QuantumCircuit(2, 2)

    entanglement.superdense_code(
        circuit,
        circuit.qubits,
        circuit.clbits,
        message,
    )

    transformed = circuit.remove_final_measurements(inplace=False)

    assert transformed is not None

    result = Statevector.from_instruction(transformed)

    phase_bit, parity_bit = message
    expected = Statevector.from_label(f"{int(parity_bit)}{int(phase_bit)}")

    assert result.equiv(expected)


def test_superdense_code_requires_two_qubits():
    circuit = QuantumCircuit(1, 2)

    with pytest.raises(ValueError):
        entanglement.superdense_code(
            circuit,
            circuit.qubits,
            circuit.clbits,
            (0, 0),
        )


def test_superdense_code_requires_distinct_qubits():
    circuit = QuantumCircuit(2, 2)

    with pytest.raises(ValueError):
        entanglement.superdense_code(
            circuit,
            [circuit.qubits[0], circuit.qubits[0]],
            circuit.clbits,
            (0, 0),
        )


def test_superdense_code_requires_two_clbits():
    circuit = QuantumCircuit(2, 1)

    with pytest.raises(ValueError):
        entanglement.superdense_code(
            circuit,
            circuit.qubits,
            circuit.clbits,
            (0, 0),
        )


def test_superdense_code_requires_distinct_clbits():
    circuit = QuantumCircuit(2, 2)

    with pytest.raises(ValueError):
        entanglement.superdense_code(
            circuit,
            circuit.qubits,
            [circuit.clbits[0], circuit.clbits[0]],
            (0, 0),
        )


@pytest.mark.parametrize(
    "message",
    [
        [],
        [0],
        [0, 0, 0],
    ],
)
def test_superdense_code_requires_two_message_bits(message):
    circuit = QuantumCircuit(2, 2)

    with pytest.raises(ValueError):
        entanglement.superdense_code(
            circuit,
            circuit.qubits,
            circuit.clbits,
            message,
        )
