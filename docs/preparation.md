# `preparation`

Utilities for preparing states across qubits.

## `bell_state`

```python
bell_state(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier], state: BellState = 'phi+') -> None
```

Prepare two qubits in one of the four Bell states.

The qubits are assumed to initially be in the |00> state.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits to prepare. Exactly two distinct qubits are required.
- `state` — Bell state to prepare. One of: - "phi+": (|00> + |11>) / sqrt(2) - "phi-": (|00> - |11>) / sqrt(2) - "psi+": (|01> + |10>) / sqrt(2) - "psi-": (|01> - |10>) / sqrt(2)

### Raises

- `ValueError` — If exactly two distinct qubits are not specified.
- `ValueError` — If an unsupported Bell state is specified.

## `ghz_state`

```python
ghz_state(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier]) -> None
```

Prepare the specified qubits in a GHZ state.

The qubits are assumed to initially be in the |0> state.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits to prepare. At least two distinct qubits are required.

### Raises

- `ValueError` — If fewer than two qubits are specified.
- `ValueError` — If duplicate qubits are specified.

## `w_state`

```python
w_state(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier]) -> None
```

Prepare the specified qubits in a W state.

The W state is an equal superposition of all computational basis states containing exactly one excitation.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits on which to prepare the W state. At least two distinct qubits are required.

### Raises

- `ValueError` — If fewer than two qubits are provided.
- `ValueError` — If duplicate qubits are specified.

## `zero_state`

```python
zero_state(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier]) -> None
```

Prepare the specified qubits in the |0> state.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits to prepare.

### Raises

- `ValueError` — If duplicate qubits are specified.

## `one_state`

```python
one_state(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier]) -> None
```

Prepare the specified qubits in the |1> state.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits to prepare.

### Raises

- `ValueError` — If duplicate qubits are specified.

## `plus_state`

```python
plus_state(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier]) -> None
```

Prepare the specified qubits in the |+> state.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits to prepare.

### Raises

- `ValueError` — If duplicate qubits are specified.

## `minus_state`

```python
minus_state(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier]) -> None
```

Prepare the specified qubits in the |-> state.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits to prepare.

### Raises

- `ValueError` — If duplicate qubits are specified.

## `basis_state`

```python
basis_state(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier], state: str) -> None
```

Prepare a computational basis state.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits to prepare.
- `state` — Bit string describing the state, such as "101". Bits correspond positionally to ``qubits``: ``state[i]`` specifies the state of ``qubits[i]``.

### Raises

- `ValueError` — If the bit string length does not match the number of qubits or contains characters other than "0" and "1".
- `ValueError` — If duplicate qubits are specified.

## `uniform_superposition`

```python
uniform_superposition(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier]) -> None
```

Prepare a uniform superposition over the specified qubits.

The qubits are assumed to initially be in the |0> state.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits to place into uniform superposition.

### Raises

- `ValueError` — If duplicate qubits are specified.

## `statevector`

```python
statevector(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier], statevector: StatevectorLike) -> None
```

Prepare an arbitrary statevector on the specified qubits.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits on which to prepare the state.
- `statevector` — Statevector amplitudes.

### Raises

- `ValueError` — If the statevector dimension does not match the number of qubits.
- `ValueError` — If duplicate qubits are specified.

## `product_state`

```python
product_state(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier], states: Sequence[Sequence[complex]]) -> None
```

Prepare a product of arbitrary single-qubit states.

Each single-qubit state is specified as [alpha, beta], representing alpha|0> + beta|1>.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits to prepare.
- `states` — Single-qubit statevectors corresponding to each qubit.

### Raises

- `ValueError` — If the number of states does not match the number of qubits.
- `ValueError` — If duplicate qubits are specified.
- `ValueError` — If any single-qubit state does not contain exactly two amplitudes.

## `random_state`

```python
random_state(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier], seed: int | None = None) -> None
```

Prepare a random pure state on the specified qubits.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits on which to prepare the state.
- `seed` — Optional random seed for reproducibility.

### Raises

- `ValueError` — If no qubits are specified.
- `ValueError` — If duplicate qubits are specified.

## `x_eigenstate`

```python
x_eigenstate(circuit: QuantumCircuit, qubit: QubitSpecifier, eigenvalue: Eigenvalue = 1) -> None
```

Prepare an eigenstate of the Pauli-X operator.

### Parameters

- `circuit` — Circuit to modify.
- `qubit` — Qubit to prepare.
- `eigenvalue` — Desired eigenvalue, either +1 or -1.

### Raises

- `ValueError` — If eigenvalue is not +1 or -1.

## `y_eigenstate`

```python
y_eigenstate(circuit: QuantumCircuit, qubit: QubitSpecifier, eigenvalue: Eigenvalue = 1) -> None
```

Prepare an eigenstate of the Pauli-Y operator.

### Parameters

- `circuit` — Circuit to modify.
- `qubit` — Qubit to prepare.
- `eigenvalue` — Desired eigenvalue, either +1 or -1.

### Raises

- `ValueError` — If eigenvalue is not +1 or -1.

## `z_eigenstate`

```python
z_eigenstate(circuit: QuantumCircuit, qubit: QubitSpecifier, eigenvalue: Eigenvalue = 1) -> None
```

Prepare an eigenstate of the Pauli-Z operator.

### Parameters

- `circuit` — Circuit to modify.
- `qubit` — Qubit to prepare.
- `eigenvalue` — Desired eigenvalue, either +1 or -1.

### Raises

- `ValueError` — If eigenvalue is not +1 or -1.

## `bloch_state`

```python
bloch_state(circuit: QuantumCircuit, qubit: QubitSpecifier, theta: float, phi: float) -> None
```

Prepare a single-qubit state using Bloch-sphere angles.

Prepares, up to global phase, the state

cos(theta / 2)|0> + exp(i * phi) sin(theta / 2)|1>.

### Parameters

- `circuit` — Circuit to modify.
- `qubit` — Qubit to prepare.
- `theta` — Polar angle in radians.
- `phi` — Azimuthal angle in radians.
