# `transform`

Utilities for quantum transforms.

## `qft`

```python
qft(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier], *, swaps: bool = True) -> None
```

Apply the quantum Fourier transform.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits on which to apply the transform.
- `swaps` — Whether to reverse the qubit order using SWAP gates.

### Raises

- `ValueError` — If no qubits are provided.
- `ValueError` — If duplicate qubits are specified.

## `inverse_qft`

```python
inverse_qft(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier], *, swaps: bool = True) -> None
```

Apply the inverse quantum Fourier transform.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits on which to apply the inverse transform.
- `swaps` — Whether to reverse the qubit order using SWAP gates.

### Raises

- `ValueError` — If no qubits are provided.
- `ValueError` — If duplicate qubits are specified.
