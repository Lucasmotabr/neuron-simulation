# Neuron Activity Simulation

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A high-performance neuron activity simulation program with both standard and optimized implementations, designed for accuracy, performance, and easy verification.

## Features

- **Standard Implementation**: Faithful to problem specifications, ideal for small-scale data and verification
- **Fast Implementation**: Processes only active neurons, optimized for sparse graphs and large-scale cases
- **Verification Mode**: Compares outputs and execution times between standard and fast versions
- **Benchmark Mode**: Performance testing with large-scale randomly generated networks

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Development History](#development-history)
- [Performance](#performance)
- [Examples](#examples)
- [Contributing](#contributing)

## Installation

```bash
git clone https://github.com/Lucasmotabr/neuron-simulation.git
cd neuron-simulation
```

No additional dependencies required - uses Python standard library only.

## Usage

### Basic Commands

#### Standard Implementation
```bash
python3 q1.py --stdin < input_file.txt
```

#### Fast Implementation
```bash
python3 q1.py --stdin-fast < input_file.txt
```

#### Verification Mode
```bash
python3 q1.py --verify-stdin < input_file.txt
```

#### Benchmark Mode
```bash
python3 q1.py --bench-demo
```

### Input Format

The input file should follow this format:
```
M N
state_1 state_2 ... state_M
threshold_1 threshold_2 ... threshold_M
[connection_data]
```

Where:
- `M`: Number of neurons
- `N`: Number of simulation steps
- `state_i`: Initial state of neuron i (0 or 1)
- `threshold_i`: Activation threshold for neuron i
- `connection_data`: Network connectivity information

## Development History

### Phase 1: Basic Implementation
- Implemented standard neuron simulation following problem specifications
- Process M neurons over N steps with signal transmission and state updates
- Verified correctness with small-scale test cases

### Phase 2: File Input Support
- Added `--stdin` option for flexible input handling
- Support for piped text files and direct file input
- Maintained backward compatibility

### Phase 3: Performance Optimization
- Identified performance bottleneck with N up to 10^6 steps
- Implemented `fast` mode utilizing inactive neuron properties
- Achieved significant speedup for sparse networks

### Phase 4: Verification System
- Added `--verify-stdin` for output validation
- Real-time comparison of standard vs. fast implementations
- Performance benchmarking capabilities

### Phase 5: Comprehensive Benchmarking
- Implemented `--bench-demo` for large-scale testing
- Automated generation of random network topologies
- Quantified performance improvements

## Performance

The fast implementation shows significant improvements, especially for large sparse networks:

| Test Case | Neurons | Edges | Steps | Standard | Fast | Improvement |
|-----------|---------|-------|-------|----------|------|-------------|
| Small     | 1,000   | 3,000 | 100   | 0.15s    | 0.12s| 20%         |
| Medium    | 20,000  | 60,000| 500   | 6.36s    | 5.03s| 21%         |
| Large     | 200,000 | 600,000| 1,500| 158.15s  | 124.71s| 21%       |

## Examples

### Example 1: Basic Usage
```bash
$ python3 q1.py --stdin < input_q1_case1.txt
1 0 1 1 0 1 1 1 1
```

### Example 2: Verification Mode
```bash
$ python3 q1.py --verify-stdin < input_q1_case2.txt
BASE : 0 0 0 1 0 0 1 0 0 0 1 0 1 0
FAST : 0 0 0 1 0 0 1 0 0 0 1 0 1 0
MATCH: True
time  baseline=0.036705s  fast=0.031777s
```

### Example 3: Benchmark Mode
```bash
$ python3 q1.py --bench-demo
[Bench] M=200000, edges=600000, steps=1500
baseline: 158.145s
fast    : 124.714s
```

## Architecture

### Core Components

- **Standard Simulator**: Direct implementation of neuron update rules
- **Fast Simulator**: Optimized version tracking only active neurons
- **Verification Engine**: Automated testing and performance comparison
- **Benchmark Generator**: Creates test cases with configurable parameters

### Key Optimizations

1. **Active Neuron Tracking**: Only processes neurons that can affect the network state
2. **Sparse Graph Handling**: Efficient representation for networks with low connectivity
3. **Memory Management**: Reduced memory footprint for large-scale simulations

## Testing

Run the verification suite:
```bash
# Test with provided examples
python3 q1.py --verify-stdin < test_cases/case1.txt
python3 q1.py --verify-stdin < test_cases/case2.txt

# Run performance benchmarks
python3 q1.py --bench-demo
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original problem specification from competitive programming contest
- Optimization techniques inspired by sparse matrix algorithms
- Performance testing methodology based on scientific computing best practices

---

Built for high-performance neural network simulation