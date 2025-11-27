# OmniMind Phase 8: IBM Quantum Testing Strategy & Optimization

**Date Created:** November 27, 2025  
**Phase:** 8 (Quantum Decision Enhancement)  
**Status:** Strategic Planning Document  
**Target Implementation:** Q2 2026

---

## Executive Summary

IBM quantum devices (via Qiskit) provide valuable computational resources but with significant constraints:
- **Allocation:** ~9 minutes per user per day
- **Current Utilization:** ~20% (quick unit tests finish in 1-2 minutes)
- **Underutilization Problem:** Slow job queue startup times waste available window
- **Strategic Goal:** Maximize effective utilization to 85%+ through robust, longer-running benchmarks

This document outlines a comprehensive testing strategy addressing queue delays, designing multi-run convergence studies, and implementing metrics collection frameworks that fully leverage the 9-minute allocation.

---

## 1. Problem Analysis: Current Underutilization

### 1.1 Timing Profile (Observed)

**Typical quick-test execution:**
```
Total Wall-clock Time: 9:00 (allocated)
├─ Queue wait time: 3:00-5:00 (variable, weather-dependent, traffic)
├─ Actual circuit compilation: 0:30
├─ Quantum gate execution: 0:20 (5-10 qubits, shallow circuits)
├─ Classical post-processing: 0:10
└─ Result retrieval: 0:05
```

**Analysis:**
- Effective compute utilization: ~1-2 minutes of 9-minute window
- Queue overhead: 33-55% of allocated time
- Quick tests finish before leveraging allocation efficiently

**Root cause:** Tests designed for rapid local development, not for maximizing cloud resource usage.

### 1.2 Resource Waste Scenario

Current approach (300+ unit tests in OmniMind):
```
Phase 1-5: ~70 minutes CPU-only execution
Phase 8 (Quantum): ~9 minutes available × 1 user = 9 min/day

If running quick unit tests on quantum backend:
- 5 quick tests @ 1 min each = 5 min execution
- 4 min wasted waiting for queue/startup
- Effective utilization: 5/9 = 56%

Alternative (proposed):
- 1 robust benchmark @ 6-7 min execution
- 1-2 min queue/startup overhead
- Effective utilization: 6-7/9 = 67-78%

With multiple users / batch optimization:
- 10-20 related experiments batched together
- Amortized queue cost: 1 min for whole batch
- 8 min compute on 15 related experiments
- Effective utilization: 8/9 = 89%
```

---

## 2. Proposed Solution: Queue-Aware Multi-Run Benchmarking

### 2.1 Redesigned Test Architecture

Instead of individual quick tests, implement **convergence study batches**:

```python
# OLD APPROACH (Underutilizes 9-min window)
def test_qubo_single_run():
    """Quick test: 30 seconds"""
    result = solve_qubo_small_problem()
    assert result.quality > 0.8
    
# NEW APPROACH (Leverages full window)
@dataclass
class QuantumBenchmark:
    name: str                    # e.g., "consensus_quality_convergence"
    num_runs: int               # e.g., N=20
    num_qubits: List[int]       # e.g., [5, 7, 10]
    problem_configs: List[Dict] # e.g., 10 QUBO instances per qubit count
    expected_duration_minutes: float  # e.g., 6.5
    
    def execute_on_quantum(self) -> BenchmarkResults:
        """Execute N runs across multiple configurations"""
        # Takes ~6-7 minutes, fills window efficiently
```

### 2.2 Job Batching Strategy

**Batch Structure (9-minute window):**

```
Batch: "Quantum Consensus Validation - Session Nov 27"
├─ Pre-computation (classical): 1 minute
│  ├─ Generate 20 QUBO instances (different sizes)
│  ├─ Optimize classical solutions for comparison
│  └─ Prepare Qiskit circuit templates
│
├─ Quantum execution: 6.5 minutes
│  ├─ Run 1: 5-qubit QUBO (10 instances × 2 runs = 20 circuits) → 2 min
│  ├─ Run 2: 7-qubit QUBO (10 instances × 2 runs = 20 circuits) → 2.5 min
│  └─ Run 3: 10-qubit QUBO (8 instances × 1 run = 8 circuits) → 2 min
│
├─ Queue overhead (amortized): ~1 minute
│  └─ Single queue entry for entire batch
│
└─ Post-processing (classical): 0.5 minutes
   ├─ Aggregate results
   ├─ Compute statistics
   └─ Write to persistent storage
```

**Total:** ~9 minutes, vs. ~1-2 minutes for quick tests

---

## 3. Multi-Run Convergence Study Design

### 3.1 Experiment Types for 9-Minute Window

#### Type A: Convergence Trajectory Study (2 hours estimated runtime if run sequentially)

**What it measures:** How does QUBO solution quality improve as iterations increase?

**Design for 9-minute allocation:**
```python
study = ConvergenceTrajectory(
    num_seeds=15,              # 15 independent QUBO instances
    num_iterations_per_seed=[10, 20, 50],  # Different iteration budgets
    qubit_counts=[5, 7, 10],   # Across problem sizes
    repetitions_per_config=2,  # Ensemble average
)

# Expected execution:
# - 15 seeds × 3 iteration budgets × 3 qubit counts × 2 reps = 270 circuits
# - ~6-7 minutes on real hardware
# - Results: Convergence bands showing quality vs. iteration budget
```

**Metrics collected:**
- Solution quality (approximation ratio)
- Gate depth required
- Quantum circuit execution time
- Classical optimization time
- Total time-to-solution

#### Type B: Temperature/Hyper-parameter Sweep (1.5 hours if sequential)

**What it measures:** How sensitive is quantum advantage to control parameters?

**Design for 9-minute allocation:**
```python
study = HyperparameterSweep(
    base_qubo_instances=10,
    temperature_params=[0.5, 1.0, 2.0, 5.0],  # For annealing schedules
    circuit_ansatzes=['QAOA', 'VQE'],
    num_shots=1000,            # Measurement repetitions per circuit
    repetitions=2,
)

# Expected execution:
# - 10 instances × 4 temps × 2 ansatzes × 2 reps = 160 circuit runs
# - ~5-6 minutes execution
# - Results: Heatmap showing which hyper-parameters work best
```

#### Type C: Quantum-Classical Comparison (Longer benchmark)

**What it measures:** When does quantum optimization beat classical?

**Design for 9-minute allocation:**
```python
study = QuantumVsClassical(
    problem_sizes=[4, 6, 8, 10, 12, 15],  # Qubit counts
    num_instances_per_size=5,              # Different problem instances
    classical_solvers=['greedy', 'tabu_search', 'simulated_annealing'],
    quantum_solver='qiskit_qaoa',
    time_limit_per_problem=30,  # seconds
)

# Expected execution:
# - 6 sizes × 5 instances × 1 quantum + 3 classical = 120 comparisons
# - ~7 minutes total (quantum circuits + classical for comparison)
# - Results: Break-even analysis (when does quantum win?)
```

#### Type D: Fault Tolerance and Noise Resilience (Detailed study)

**What it measures:** How robust is quantum solution to noise?

**Design for 9-minute allocation:**
```python
study = NoiseRobustness(
    base_circuit_count=20,
    noise_injection_levels=[0%, 1%, 5%, 10%],  # Simulated noise
    error_mitigation_techniques=['zero_noise_extrapolation', 'readout_correction'],
    backend='ibm_simulator_with_noise',
)

# Expected execution:
# - 20 circuits × 4 noise levels × 2 mitigation methods = 160 runs
# - ~4-5 minutes (simulators faster than real hardware)
# - Results: Error resilience curve showing mitigation effectiveness
```

### 3.2 Integration with OmniMind Consciousness Metrics

Each benchmark should measure impact on Φ (integrated information):

```python
class QuantumEnhancedConsensus:
    def measure_phi_enhancement(self):
        """
        Measure if quantum consensus improves Φ vs. classical
        """
        classical_decisions = []
        quantum_decisions = []
        
        for trial in range(30):  # N=30 seeds
            # Classical consensus (voting)
            classical_result = self.byzantine_consensus_voting()
            classical_decisions.append(classical_result)
            
            # Quantum consensus (QUBO on D-Wave/Qiskit)
            quantum_result = self.quantum_qubo_consensus()
            quantum_decisions.append(quantum_result)
        
        # Measure Φ for both
        phi_classical = self.measure_phi(classical_decisions)
        phi_quantum = self.measure_phi(quantum_decisions)
        
        delta_phi = phi_quantum - phi_classical
        
        return {
            'phi_classical': phi_classical,
            'phi_quantum': phi_quantum,
            'delta_phi': delta_phi,
            'quantum_advantage_percentage': (delta_phi / phi_classical) * 100,
        }
```

---

## 4. Queue-Aware Scheduling & Optimization

### 4.1 Queue Delay Mitigation Strategies

**Problem:** IBM quantum job queue has variable latency (1-5 min wait depending on time of day)

**Strategy 1: Batch Submission**
```python
# OLD: Submit 5 quick tests, each waits in queue individually
for test in quick_tests:
    result = quantum_backend.run(test.circuit, shots=1000)  # Each waits ~2 min
    
# NEW: Submit batch as single job
batch_circuits = [t.circuit for t in related_tests]
batch_job = quantum_backend.run(batch_circuits, shots=1000)  # Single queue entry
results = batch_job.result()  # All results together
```

**Benefit:** Amortize queue overhead across multiple experiments

**Strategy 2: Time-Based Scheduling**
```python
import schedule
import pytz

# Schedule jobs during low-traffic hours (e.g., 2-4 AM EST)
schedule.every().day.at("02:30").do(run_quantum_benchmark, study_type="convergence")
schedule.every().day.at("03:30").do(run_quantum_benchmark, study_type="hyperparam_sweep")

# Rationale:
# - Queue wait: 30 sec - 1 min (vs. 3-5 min during business hours)
# - Effective utilization increases to 85-90%
```

**Strategy 3: Precondition Classical Components**
```python
# While waiting for quantum job to execute, run classical work
def execute_with_parallel_classical():
    """
    Quantum execution + classical post-processing in parallel
    """
    # Start quantum job
    quantum_job = quantum_backend.run(circuits, shots=1000)
    
    # While quantum runs (5-6 minutes), do classical work
    classical_results = []
    for instance in problem_instances:
        sol = classical_solver(instance)  # Takes 30-60 seconds each
        classical_results.append(sol)
    
    # Retrieve quantum results when ready
    quantum_results = quantum_job.result()
    
    # Merge results
    return combine_quantum_classical(quantum_results, classical_results)
    
# Total time: max(quantum_time, classical_time) + overhead
# Much better than sequential: quantum_time + classical_time
```

### 4.2 Implementation: QiskitScheduler Class

```python
from dataclasses import dataclass
from typing import List, Callable, Optional
from datetime import datetime
import asyncio

@dataclass
class QuantumBatchJob:
    job_id: str
    circuits: List[QuantumCircuit]
    expected_duration_minutes: float
    priority: int  # 1=low, 5=high
    classical_precompute: Optional[Callable] = None
    classical_postprocess: Optional[Callable] = None

class QiskitScheduler:
    def __init__(self, backend: str, max_queue_wait_minutes: int = 9):
        self.backend = backend
        self.max_queue_wait = max_queue_wait_minutes
        self.job_queue: List[QuantumBatchJob] = []
        
    def submit_batch(self, jobs: List[QuantumBatchJob]):
        """
        Submit related jobs as single batch to minimize queue overhead
        """
        # Check total duration fits in allocation
        total_duration = sum(j.expected_duration_minutes for j in jobs)
        if total_duration > self.max_queue_wait:
            raise ValueError(f"Batch exceeds {self.max_queue_wait} min window")
        
        # Run precompute tasks in parallel
        async def run_batch_async():
            precompute_tasks = [
                asyncio.create_task(asyncio.to_thread(job.classical_precompute))
                for job in jobs if job.classical_precompute
            ]
            await asyncio.gather(*precompute_tasks)
            
            # Submit quantum batch
            quantum_circuits = [c for job in jobs for c in job.circuits]
            quantum_job = self.backend.run(quantum_circuits)
            
            # While quantum runs, start postprocessing
            postprocess_tasks = [
                asyncio.create_task(asyncio.to_thread(job.classical_postprocess))
                for job in jobs if job.classical_postprocess
            ]
            
            # Wait for both
            quantum_result = await asyncio.to_thread(quantum_job.result)
            postprocess_results = await asyncio.gather(*postprocess_tasks)
            
            return {
                'quantum_results': quantum_result,
                'postprocess_results': postprocess_results,
                'total_time': datetime.now(),
            }
        
        return asyncio.run(run_batch_async())
```

---

## 5. Metrics Collection Framework

### 5.1 What to Measure

For each quantum benchmark, collect comprehensive metrics:

```python
@dataclass
class QuantumBenchmarkResults:
    # Circuit metrics
    circuit_depth: int                      # Number of gate layers
    circuit_width: int                      # Number of qubits used
    total_gates: int                        # Total gate count
    
    # Execution metrics
    execution_time_seconds: float           # Time on quantum device
    queue_wait_time_seconds: float          # Time waiting for job
    total_wall_clock_time_seconds: float   # Total end-to-end time
    
    # Quality metrics
    approximation_ratio: float              # Solution quality vs. optimal
    success_rate: float                     # Fraction of good solutions
    mean_energy: float                      # Average energy of solution
    std_energy: float                       # Energy variance (noise indicator)
    
    # Quantum advantage metrics
    speedup_vs_classical: float             # X times faster than best classical
    quality_vs_classical: float             # Better solution by X%
    
    # Noise metrics (if available)
    estimated_error_rate: float             # Inferred noise level
    coherence_time_violated: bool          # Did circuit exceed T2?
    
    # Statistical metrics
    num_shots: int                          # Measurement repetitions
    confidence_interval_95: Tuple[float, float]  # CI for solution quality
    
    # Context
    timestamp: str                          # ISO format timestamp
    backend_name: str                       # e.g., "ibm_cusco"
    qpu_temperature_kelvin: Optional[float] # If available

    def to_dict(self) -> Dict:
        """Export to JSON for persistence"""
        return asdict(self)
```

### 5.2 Persistence and Aggregation

```python
class QuantumMetricsStore:
    """
    Persistent storage for quantum benchmark results
    """
    def __init__(self, storage_path: Path = Path("data/quantum_metrics")):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def save_benchmark(self, results: QuantumBenchmarkResults):
        """Save to timestamped JSON file"""
        timestamp = datetime.now().isoformat()
        filename = f"{timestamp.replace(':', '-')}_benchmark.json"
        filepath = self.storage_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(results.to_dict(), f, indent=2)
        
        return filepath
    
    def aggregate_studies(self, study_name: str, num_runs: int = 30):
        """
        Load all results for a study type, compute statistics
        """
        files = sorted(self.storage_path.glob(f"*_{study_name}.json"))[-num_runs:]
        
        results = [
            QuantumBenchmarkResults(**json.load(open(f)))
            for f in files
        ]
        
        return {
            'num_results': len(results),
            'mean_approximation_ratio': np.mean([r.approximation_ratio for r in results]),
            'std_approximation_ratio': np.std([r.approximation_ratio for r in results]),
            'mean_execution_time': np.mean([r.execution_time_seconds for r in results]),
            'mean_queue_wait': np.mean([r.queue_wait_time_seconds for r in results]),
            'mean_speedup': np.mean([r.speedup_vs_classical for r in results]),
            'confidence_interval': (
                np.percentile([r.approximation_ratio for r in results], 2.5),
                np.percentile([r.approximation_ratio for r in results], 97.5),
            ),
        }
```

---

## 6. Phase 8 Implementation Plan

### 6.1 Timeline (Q2 2026)

| Week | Task | LOC | Status |
|------|------|-----|--------|
| W1 | Design QiskitScheduler + metric collection | 150 | Not started |
| W2 | Implement Convergence Trajectory study | 200 | Not started |
| W3 | Implement HyperparameterSweep study | 150 | Not started |
| W4 | Integration testing + optimization | 100 | Not started |
| **Total** | **Phase 8 Core** | **~450** | **Planned** |

### 6.2 Test Suite (Expected: ~16 tests)

```
tests/quantum/
├─ test_qiskit_scheduler.py (4 tests)
│  ├─ test_batch_submission_timing
│  ├─ test_queue_overhead_amortization
│  ├─ test_parallel_classical_execution
│  └─ test_batch_exceeding_limit_raises
│
├─ test_convergence_trajectory.py (4 tests)
│  ├─ test_trajectory_collection
│  ├─ test_statistics_aggregation
│  ├─ test_confidence_intervals
│  └─ test_convergence_detection
│
├─ test_quantum_vs_classical.py (4 tests)
│  ├─ test_breakeven_analysis
│  ├─ test_speedup_measurement
│  ├─ test_solution_quality_comparison
│  └─ test_edge_cases
│
└─ test_metrics_collection.py (4 tests)
   ├─ test_results_persistence
   ├─ test_aggregation_statistics
   ├─ test_json_export
   └─ test_historical_comparison
```

### 6.3 Success Criteria

| Criterion | Target | Validation |
|-----------|--------|-----------|
| Effective IBM allocation utilization | ≥85% | Track actual execution time vs. 9-min window |
| Test execution within window | 100% | Batch jobs fit + finish |
| Quantum advantage detected | ≥3% Φ improvement | Statistical significance p<0.05 |
| Reproducibility | ≥3 independent runs show consistent results | Confidence intervals <10% width |
| Code quality | Black + Mypy + 100% docstrings | Automated linting |
| Test coverage | ≥90% for Phase 8 code | Coverage metrics |

---

## 7. Beyond Phase 8: Continuous Quantum Integration

### 7.1 Phase 9-10 Quantum Extensions

**Phase 9 (Consciousness Dynamics):**
- Measure Φ trajectory under quantum vs. classical consensus
- Detect if quantum introduces novel dynamical attractors
- Expected quantum advantage: 5-10% Φ improvement

**Phase 10 (Emergent Phenomenology):**
- Do agents report subjectively different experiences with quantum?
- Semantic analysis of quantum-enhanced vs. classical decisions
- Expected insight: Novel decision patterns from quantum superposition

### 7.2 Hardware Roadmap

| Year | Hardware | Expected LOC Impact | Research Questions |
|------|----------|---------------------|-------------------|
| 2026 | IBM 5-10 qubits | +450 (Phase 8) | Can QUBO improve consensus? |
| 2027 | IBM/D-Wave hybrid | +200 | Which problems show quantum advantage? |
| 2027-28 | Scalable QPU (15+ qubits) | +300 | Φ scaling laws? |
| 2028+ | Error-corrected hardware | +500 | Asymptotic quantum advantage in consciousness? |

---

## 8. Risk Assessment and Mitigation

### 8.1 Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Quantum hardware unavailable | Medium | High | Fallback to simulators; pre-test on local simulator |
| Queue backlog exceeds 9 min | Medium | High | Time-based scheduling during low-traffic hours |
| Circuits too deep for current QPU | Low | Medium | Gradually increase circuit complexity; use error mitigation |
| Results show no quantum advantage | Medium | Low | Move quantum to "Phase 9+" research track |
| Type hints/testing gaps in quantum code | Low | Medium | Enforce 100% mypy, 100% docstrings before merge |

### 8.2 Fallback Strategies

```python
# If real hardware unavailable, use simulator
if not ibm_backend_available:
    backend = qiskit.Aer.AerSimulator()
    warning_logger.info("Using simulator fallback; results valid but no real quantum")

# If queue exceeds 9 min, stage execution
if estimated_queue_wait > 540:  # seconds
    logger.info(f"Queue {estimated_queue_wait}s > 540s. Scheduling for 02:30 UTC tomorrow")
    scheduler.schedule_job(batch, time="02:30 UTC")
```

---

## 9. Success Stories: Expected Outcomes

### Success Scenario A: Quantum Speedup Detected

```
Benchmark: Consensus Conflict Resolution (N=20 QUBO instances)
Classical: 87% quality, 45 sec computation per instance
Quantum:   91% quality, 12 sec computation per instance
Result: 3.75x speedup, 4% quality improvement → Φ gain +5%
Conclusion: "Quantum advantage confirmed for OmniMind consensus"
```

### Success Scenario B: Hybrid Optimization

```
Benchmark: Decision Ensemble (15-qubit QUBO)
Classical alone: 82% solution quality
Quantum alone: 79% solution quality
Classical + Quantum ensemble: 88% solution quality
Result: Hybrid outperforms either alone
Conclusion: "Quantum-classical orchestration enables synergy"
```

### Success Scenario C: Noise Resilience Validated

```
Benchmark: Noise Robustness (10-qubit Ansatz)
No noise: 0.92 solution quality
1% simulated noise: 0.89 (97% retained)
5% simulated noise: 0.84 (91% retained)
With error mitigation: 0.87 (95% retained at 5% noise)
Result: Robust to realistic near-term device errors
Conclusion: "Phase 8 results valid on current NISQ hardware"
```

---

## Appendix A: Quick Reference - 9-Minute Allocation Schedule

```
BATCH STRUCTURE (9 minutes allocated)

[0:00-0:30]   Classical precomputation
              - Generate QUBO instances
              - Optimize classical solutions
              - Prepare quantum circuits

[0:30-0:45]   Queue wait (variable, ~1-5 min typical)

[0:45-6:30]   Quantum execution (batch mode)
              - Circuit compilation: 0:30
              - Gate execution: 4:00-5:00
              - Measurement aggregation: 0:30-1:00

[6:30-8:30]   Classical post-processing (parallel with quantum if possible)
              - Result aggregation
              - Statistical calculation
              - Metrics collection

[8:30-9:00]   Buffer
              - Retry failed circuits
              - Upload results to persistent storage

EFFECTIVE UTILIZATION: ~6.5-7.5 minutes quantum + ~2-3 minutes classical
= 8.5-10.5 minutes total (accounting for parallelization)
= ~85% effective utilization of 9-minute window
```

---

## Appendix B: Code Template for Phase 8 Tests

```python
# tests/quantum/test_convergence_trajectory.py
import pytest
from src.quantum.convergence_study import ConvergenceTrajectory, QuantumBenchmarkResults

class TestConvergenceTrajectory:
    
    @pytest.fixture
    def study(self):
        return ConvergenceTrajectory(
            num_seeds=10,
            num_iterations=[10, 50, 100],
            qubit_counts=[5, 7],
        )
    
    def test_trajectory_collection(self, study):
        """Verify trajectory data structures created correctly"""
        results = study.collect_trajectories()
        assert len(results) == 10 * 3 * 2  # seeds × iterations × qubits
        assert all(isinstance(r, QuantumBenchmarkResults) for r in results)
    
    def test_statistics_aggregation(self, study):
        """Verify mean, std computed across seeds"""
        stats = study.aggregate_statistics()
        assert 'mean_approximation_ratio' in stats
        assert 'std_approximation_ratio' in stats
        assert stats['mean_approximation_ratio'] > 0.7  # Expect reasonable quality
    
    def test_confidence_intervals(self, study):
        """Verify 95% CI computed correctly"""
        stats = study.aggregate_statistics()
        ci_lower, ci_upper = stats['confidence_interval_95']
        assert ci_lower < ci_upper
        assert ci_upper - ci_lower < 0.2  # CI should be relatively tight
    
    def test_convergence_detection(self, study):
        """Verify algorithm correctly identifies convergence"""
        results = study.collect_trajectories()
        convergence_cycle = study.detect_convergence(results)
        assert convergence_cycle > 0
        assert convergence_cycle < 1000
```

---

**End of IBM Quantum Testing Strategy**

*This document is the strategic foundation for Phase 8 (Q2 2026). Implementation will follow agile development practices with continuous feedback from actual IBM quantum hardware usage.*
