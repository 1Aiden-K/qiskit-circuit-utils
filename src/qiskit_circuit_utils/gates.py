"""Utilities for applying gates across collections of qubits."""

from collections.abc import Iterable

from qiskit import QuantumCircuit

from ._types import (
    QubitPair,
    QubitSpecifier,
    QubitTriple,
)

# Pauli gates

def x_all(
    circuit: QuantumCircuit,
    qubits: Iterable[QubitSpecifier],
) -> None:
    """Apply an X gate to each qubit."""
    qubits = list(qubits)

    if qubits:
        circuit.x(qubits)

def y_all(
    circuit: QuantumCircuit,
    qubits: Iterable[QubitSpecifier],
) -> None:
    """Apply a Y gate to each qubit."""
    qubits = list(qubits)

    if qubits:
        circuit.y(qubits)

def z_all(
    circuit: QuantumCircuit,
    qubits: Iterable[QubitSpecifier],
) -> None:
    """Apply a Z gate to each qubit."""
    qubits = list(qubits)

    if qubits:
        circuit.z(qubits)

# Hadamard

def h_all(
    circuit: QuantumCircuit,
    qubits: Iterable[QubitSpecifier],
) -> None:
    """Apply a Hadamard gate to each qubit."""
    qubits = list(qubits)

    if qubits:
        circuit.h(qubits)

# Phase gates

def s_all(
    circuit: QuantumCircuit,
    qubits: Iterable[QubitSpecifier],
) -> None:
    """Apply an S gate to each qubit."""
    qubits = list(qubits)

    if qubits:
        circuit.s(qubits)

def sdg_all(
    circuit: QuantumCircuit,
    qubits: Iterable[QubitSpecifier],
) -> None:
    """Apply an S-dagger gate to each qubit."""
    qubits = list(qubits)

    if qubits:
        circuit.sdg(qubits)

def t_all(
    circuit: QuantumCircuit,
    qubits: Iterable[QubitSpecifier],
) -> None:
    """Apply a T gate to each qubit."""
    qubits = list(qubits)

    if qubits:
        circuit.t(qubits)

def tdg_all(
    circuit: QuantumCircuit,
    qubits: Iterable[QubitSpecifier],
) -> None:
    """Apply a T-dagger gate to each qubit."""
    qubits = list(qubits)

    if qubits:
        circuit.tdg(qubits)

# Square-root X

def sx_all(
    circuit: QuantumCircuit,
    qubits: Iterable[QubitSpecifier],
) -> None:
    """Apply an SX gate to each qubit."""
    qubits = list(qubits)

    if qubits:
        circuit.sx(qubits)

def sxdg_all(
    circuit: QuantumCircuit,
    qubits: Iterable[QubitSpecifier],
) -> None:
    """Apply an SX-dagger gate to each qubit."""
    qubits = list(qubits)

    if qubits:
        circuit.sxdg(qubits)

# Rotation gates

def rx_all(
    circuit: QuantumCircuit,
    qubits: Iterable[QubitSpecifier],
    theta: float,
) -> None:
    """Apply RX(theta) to each qubit."""
    qubits = list(qubits)

    if qubits:
        circuit.rx(theta, qubits)

def ry_all(
    circuit: QuantumCircuit,
    qubits: Iterable[QubitSpecifier],
    theta: float,
) -> None:
    """Apply RY(theta) to each qubit."""
    qubits = list(qubits)

    if qubits:
        circuit.ry(theta, qubits)

def rz_all(
    circuit: QuantumCircuit,
    qubits: Iterable[QubitSpecifier],
    theta: float,
) -> None:
    """Apply RZ(theta) to each qubit."""
    qubits = list(qubits)

    if qubits:
        circuit.rz(theta, qubits)

def p_all(
    circuit: QuantumCircuit,
    qubits: Iterable[QubitSpecifier],
    theta: float,
) -> None:
    """Apply a phase gate P(theta) to each qubit."""
    qubits = list(qubits)

    if qubits:
        circuit.p(theta, qubits)


# General single-qubit gates

def u_all(
    circuit: QuantumCircuit,
    qubits: Iterable[QubitSpecifier],
    theta: float,
    phi: float,
    lam: float,
) -> None:
    """Apply U(theta, phi, lambda) to each qubit."""
    qubits = list(qubits)

    if qubits:
        circuit.u(theta, phi, lam, qubits)

# Controlled gates

def cx_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[QubitPair],
) -> None:
    """Apply CX to each (control, target) pair."""
    for control, target in pairs:
        circuit.cx(control, target)

def cy_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[QubitPair],
) -> None:
    """Apply CY to each (control, target) pair."""
    for control, target in pairs:
        circuit.cy(control, target)

def cz_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[QubitPair],
) -> None:
    """Apply CZ to each (control, target) pair."""
    for control, target in pairs:
        circuit.cz(control, target)

def ch_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[QubitPair],
) -> None:
    """Apply controlled-H to each (control, target) pair."""
    for control, target in pairs:
        circuit.ch(control, target)

def cp_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[QubitPair],
    theta: float,
) -> None:
    """Apply CP(theta) to each (control, target) pair."""
    for control, target in pairs:
        circuit.cp(theta, control, target)

def crx_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[QubitPair],
    theta: float,
) -> None:
    """Apply CRX(theta) to each (control, target) pair."""
    for control, target in pairs:
        circuit.crx(theta, control, target)

def cry_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[QubitPair],
    theta: float,
) -> None:
    """Apply CRY(theta) to each (control, target) pair."""
    for control, target in pairs:
        circuit.cry(theta, control, target)

def crz_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[QubitPair],
    theta: float,
) -> None:
    """Apply CRZ(theta) to each (control, target) pair."""
    for control, target in pairs:
        circuit.crz(theta, control, target)

# Two-qubit gates

def swap_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[QubitPair],
) -> None:
    """Apply SWAP to each pair of qubits."""
    for q0, q1 in pairs:
        circuit.swap(q0, q1)

def iswap_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[QubitPair],
) -> None:
    """Apply iSWAP to each pair of qubits."""
    for q0, q1 in pairs:
        circuit.iswap(q0, q1)

def rxx_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[QubitPair],
    theta: float,
) -> None:
    """Apply RXX(theta) to each pair of qubits."""
    for q0, q1 in pairs:
        circuit.rxx(theta, q0, q1)

def ryy_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[QubitPair],
    theta: float,
) -> None:
    """Apply RYY(theta) to each pair of qubits."""
    for q0, q1 in pairs:
        circuit.ryy(theta, q0, q1)

def rzz_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[QubitPair],
    theta: float,
) -> None:
    """Apply RZZ(theta) to each pair of qubits."""
    for q0, q1 in pairs:
        circuit.rzz(theta, q0, q1)

def rzx_pairs(
    circuit: QuantumCircuit,
    pairs: Iterable[QubitPair],
    theta: float,
) -> None:
    """Apply RZX(theta) to each pair of qubits."""
    for q0, q1 in pairs:
        circuit.rzx(theta, q0, q1)

# Three-qubit gates

def ccx_triples(
    circuit: QuantumCircuit,
    triples: Iterable[QubitTriple],
) -> None:
    """Apply CCX to each (control_0, control_1, target) triple."""
    for control_0, control_1, target in triples:
        circuit.ccx(control_0, control_1, target)

def cswap_triples(
    circuit: QuantumCircuit,
    triples: Iterable[QubitTriple],
) -> None:
    """Apply controlled-SWAP to each (control, q0, q1) triple."""
    for control, q0, q1 in triples:
        circuit.cswap(control, q0, q1)