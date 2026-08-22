# `correction`

Utilities for classically controlled quantum corrections.

## `x_if`

```python
x_if(circuit: QuantumCircuit, target: QubitSpecifier, control_bit: ClbitSpecifier) -> None
```

Apply a classically controlled X correction.

Applies an X gate to ``target`` when ``control_bit`` is 1.

### Parameters

- `circuit` — Circuit to modify.
- `target` — Qubit receiving the correction.
- `control_bit` — Classical bit controlling the correction.

## `z_if`

```python
z_if(circuit: QuantumCircuit, target: QubitSpecifier, control_bit: ClbitSpecifier) -> None
```

Apply a classically controlled Z correction.

Applies a Z gate to ``target`` when ``control_bit`` is 1.

### Parameters

- `circuit` — Circuit to modify.
- `target` — Qubit receiving the correction.
- `control_bit` — Classical bit controlling the correction.

## `pauli`

```python
pauli(circuit: QuantumCircuit, target: QubitSpecifier, x_bit: ClbitSpecifier, z_bit: ClbitSpecifier) -> None
```

Apply classically controlled Pauli X and Z corrections.

This is the standard correction used by quantum teleportation and entanglement-swapping protocols.

### Parameters

- `circuit` — Circuit to modify.
- `target` — Qubit receiving the corrections.
- `x_bit` — Classical bit controlling the X correction.
- `z_bit` — Classical bit controlling the Z correction.

## `x_if_all`

```python
x_if_all(circuit: QuantumCircuit, targets: Sequence[QubitSpecifier], control_bits: Sequence[ClbitSpecifier]) -> None
```

Apply controlled X corrections to corresponding qubits.

### Parameters

- `circuit` — Circuit to modify.
- `targets` — Qubits receiving the corrections.
- `control_bits` — Classical bits controlling the corrections.

### Raises

- `ValueError` — If the numbers of targets and control bits differ.

## `z_if_all`

```python
z_if_all(circuit: QuantumCircuit, targets: Sequence[QubitSpecifier], control_bits: Sequence[ClbitSpecifier]) -> None
```

Apply controlled Z corrections to corresponding qubits.

### Parameters

- `circuit` — Circuit to modify.
- `targets` — Qubits receiving the corrections.
- `control_bits` — Classical bits controlling the corrections.

### Raises

- `ValueError` — If the numbers of targets and control bits differ.

## `pauli_all`

```python
pauli_all(circuit: QuantumCircuit, targets: Sequence[QubitSpecifier], x_bits: Sequence[ClbitSpecifier], z_bits: Sequence[ClbitSpecifier]) -> None
```

Apply Pauli corrections to corresponding target qubits.

### Parameters

- `circuit` — Circuit to modify.
- `targets` — Qubits receiving the corrections.
- `x_bits` — Classical bits controlling X corrections.
- `z_bits` — Classical bits controlling Z corrections.

### Raises

- `ValueError` — If the input sequences have different lengths.
