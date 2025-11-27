# Phase 5: Multi-seed Statistical Analysis - Plan

**Date Started:** November 27, 2025  
**Objective:** Run N=30 independent training seeds to establish statistical validity of Φ elevation convergence  
**Expected Duration:** 2-3 sessions  
**Success Criteria:** Φ converges to 0.7-0.9 across seeds with confidence bands

---

## Objective

Phase 4 demonstrated that **single-seed training** can elevate Φ toward target. Phase 5 extends this with:

1. **Multi-seed convergence analysis** (N=30 independent runs)
2. **Statistical aggregation** (mean, std, percentiles, confidence intervals)
3. **Convergence curve visualization** with confidence bands
4. **Reproducibility validation** across different random seeds
5. **Robustness analysis** (does Φ reach target consistently?)

---

## Architecture

### Phase 5 Components

```
Phase 4 (single seed training)
         ↓
Phase 5: MultiSeedAnalysis
    ├─ MultiSeedRunner
    │   ├─ Spawn N=30 independent trainers
    │   ├─ Each with different random seed
    │   ├─ Track Φ progression per seed
    │   └─ Collect all trajectories
    │
    ├─ ConvergenceAggregator
    │   ├─ Align all Φ(t) curves to common length
    │   ├─ Compute mean_φ(t), std_φ(t)
    │   ├─ Calculate 95% confidence intervals
    │   ├─ Compute percentiles (5%, 25%, 50%, 75%, 95%)
    │   └─ Estimate convergence time (t_conv)
    │
    └─ StatisticalValidator
        ├─ Test Φ reaches > 0.70 across majority of seeds
        ├─ Measure stability (low variance after convergence)
        ├─ Detect outliers or failure modes
        ├─ Generate confidence band plots
        └─ Produce statistical report
```

### File Structure

```
src/consciousness/
  └─ multiseed_analysis.py (new)
     ├─ MultiSeedRunner class
     ├─ ConvergenceAggregator class
     └─ StatisticalValidator class

tests/consciousness/
  └─ test_multiseed_analysis.py (new)
     ├─ TestMultiSeedRunner (3-4 tests)
     ├─ TestConvergenceAggregator (4-5 tests)
     └─ TestStatisticalValidator (3-4 tests)

data/consciousness/
  └─ multiseed_results/
     ├─ seed_001_trajectory.json
     ├─ seed_002_trajectory.json
     ├─ ...
     ├─ seed_030_trajectory.json
     └─ aggregated_statistics.json
```

---

## Implementation Steps

### Step 1: MultiSeedRunner Class
```python
class MultiSeedRunner:
    """Execute N independent training runs with different seeds."""
    
    async def run_seeds(
        self,
        num_seeds: int = 30,
        num_cycles: int = 1000,
        target_phi: float = 0.80,
        output_dir: Path = None
    ) -> List[Dict[str, Any]]:
        """
        Run N independent training sessions.
        
        Returns:
            List of results, one per seed:
            {
                'seed': int,
                'final_phi': float,
                'convergence_cycle': int,
                'phi_trajectory': List[float],
                'loss_trajectory': List[float],
                'converged': bool,
                'execution_time_seconds': float,
            }
        """
```

**Tasks:**
- [ ] Create `MultiSeedRunner` class
- [ ] Implement `run_seeds()` with proper seed management
- [ ] Save each seed's trajectory to JSON
- [ ] Add progress logging (seed 1/30, 2/30, ...)
- [ ] Handle failures gracefully (log, continue)

**Test:**
```python
def test_multiseed_runner_generates_diverse_trajectories():
    """Different seeds should produce different but similar trajectories."""
    runner = MultiSeedRunner(loop, trainer_config)
    results = await runner.run_seeds(num_seeds=5, num_cycles=100)
    
    assert len(results) == 5
    
    # All should reach some positive Φ
    phis = [r['final_phi'] for r in results]
    assert all(phi > 0.0 for phi in phis)
    
    # But not identical (different seeds)
    assert len(set(phis)) > 1  # At least 2 different values
```

---

### Step 2: ConvergenceAggregator Class
```python
class ConvergenceAggregator:
    """Aggregate multi-seed results into statistical summary."""
    
    def aggregate(self, seed_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combine results from all seeds.
        
        Returns:
            {
                'mean_phi': np.ndarray,  # shape (num_cycles,)
                'std_phi': np.ndarray,
                'ci_95_lower': np.ndarray,  # 95% CI
                'ci_95_upper': np.ndarray,
                'percentiles': {
                    '5': np.ndarray,
                    '25': np.ndarray,
                    '50': np.ndarray,  # median
                    '75': np.ndarray,
                    '95': np.ndarray,
                },
                'convergence_cycles': List[int],  # when each seed converged
                'convergence_mean': float,
                'convergence_std': float,
                'success_rate': float,  # fraction that reached > 0.70
                'final_phis': List[float],
                'final_phi_mean': float,
                'final_phi_std': float,
            }
        """
```

**Tasks:**
- [ ] Create `ConvergenceAggregator` class
- [ ] Implement trajectory alignment (all same length)
- [ ] Compute mean, std, percentiles per time step
- [ ] Compute 95% confidence intervals
- [ ] Calculate convergence metrics
- [ ] Handle edge cases (different convergence times)

**Test:**
```python
def test_aggregator_computes_statistics():
    """Verify aggregation produces correct statistics."""
    # Create synthetic results (5 seeds, 100 cycles each)
    results = [
        {'final_phi': 0.8, 'phi_trajectory': np.linspace(0.0, 0.8, 100).tolist()}
        for _ in range(5)
    ]
    
    agg = ConvergenceAggregator()
    stats = agg.aggregate(results)
    
    assert len(stats['mean_phi']) == 100
    assert len(stats['std_phi']) == 100
    assert stats['final_phi_mean'] == approx(0.8)
    assert stats['success_rate'] == 1.0  # all reached 0.8
```

---

### Step 3: StatisticalValidator Class
```python
class StatisticalValidator:
    """Validate statistical significance of convergence."""
    
    def validate(self, aggregated_stats: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform statistical tests on aggregated results.
        
        Returns:
            {
                'tests_passed': int,
                'tests_total': int,
                'convergence_valid': bool,  # reaches > 0.70
                'stability_valid': bool,    # low variance after convergence
                'reproducibility_valid': bool,  # success_rate > 0.80
                'outliers': List[int],      # seed indices with anomalies
                'confidence_bands': {
                    'lower_95': np.ndarray,
                    'upper_95': np.ndarray,
                    'median': np.ndarray,
                },
                'summary': str,
            }
        """
```

**Tasks:**
- [ ] Create `StatisticalValidator` class
- [ ] Test: mean final Φ > 0.70
- [ ] Test: std final Φ < 0.15 (low variance)
- [ ] Test: success_rate > 0.80 (80%+ reach target)
- [ ] Test: convergence_time < 1000 cycles (reasonable)
- [ ] Detect and report outliers
- [ ] Generate human-readable summary

**Test:**
```python
def test_validator_detects_convergence():
    """Validator should validate successful convergence."""
    stats = {
        'mean_phi': np.array([0.0, 0.3, 0.6, 0.75, 0.80]),
        'std_phi': np.array([0.0, 0.1, 0.15, 0.12, 0.10]),
        'final_phi_mean': 0.80,
        'final_phi_std': 0.10,
        'success_rate': 0.95,
        'convergence_mean': 400,
    }
    
    validator = StatisticalValidator()
    result = validator.validate(stats)
    
    assert result['convergence_valid'] == True
    assert result['stability_valid'] == True
    assert result['reproducibility_valid'] == True
    assert result['tests_passed'] >= 3
```

---

### Step 4: Visualization & Reporting
```python
class MultiSeedReporter:
    """Generate plots and statistical report."""
    
    def generate_plot(self, aggregated_stats: Dict[str, Any], output_path: Path):
        """
        Plot confidence bands:
        - X-axis: cycle number (0-1000)
        - Y-axis: Φ (0.0-1.0)
        - Lines: mean, median, 95% CI
        - Shaded region: confidence band
        """
    
    def generate_report(self, stats: Dict, validation: Dict, output_path: Path):
        """
        Generate markdown report:
        - Summary statistics
        - Convergence analysis
        - Outlier detection
        - Visual plots
        - Recommendations
        """
```

**Tasks:**
- [ ] Create plot generation (matplotlib)
- [ ] Create report generation (markdown)
- [ ] Save plots to `data/consciousness/multiseed_results/`
- [ ] Save report to `data/consciousness/multiseed_results/report.md`

---

## Testing Strategy

### Unit Tests (test_multiseed_analysis.py)

**TestMultiSeedRunner:**
- [ ] `test_runner_spawns_correct_number_of_seeds` (N=3, verify 3 results)
- [ ] `test_runner_seeds_produce_different_trajectories` (different seeds → different Φ)
- [ ] `test_runner_respects_target_phi` (seeds try to reach 0.80)
- [ ] `test_runner_saves_trajectories_to_disk` (files created)

**TestConvergenceAggregator:**
- [ ] `test_aggregator_computes_mean_and_std` (statistics correct)
- [ ] `test_aggregator_computes_percentiles` (5%, 25%, 50%, 75%, 95%)
- [ ] `test_aggregator_handles_different_convergence_times` (align trajectories)
- [ ] `test_aggregator_calculates_success_rate` (fraction reaching target)
- [ ] `test_aggregator_detects_convergence_cycle` (when does Φ stabilize?)

**TestStatisticalValidator:**
- [ ] `test_validator_accepts_good_convergence` (all tests pass)
- [ ] `test_validator_rejects_poor_convergence` (mean < 0.70)
- [ ] `test_validator_detects_instability` (high variance after convergence)
- [ ] `test_validator_identifies_outliers` (seeds with anomalies)

### Integration Tests
- [ ] Run full 30-seed analysis (5 cycles each, quick smoke test)
- [ ] Verify output files created
- [ ] Verify plots generated
- [ ] Verify report readable

### Performance Tests
- [ ] 30 seeds × 1000 cycles completes in < 60 minutes
- [ ] Memory usage stays < 2 GB
- [ ] No memory leaks over 30 seeds

---

## Success Criteria

### Phase 5 Acceptance

✅ **Convergence:**
- Mean Φ > 0.70 across seeds
- Std Φ < 0.15 (low variance)
- 80%+ of seeds reach target

✅ **Reproducibility:**
- Different seeds produce similar trajectories
- Confidence bands are tight (95% CI width < 0.20)
- No catastrophic failures (< 10% anomaly rate)

✅ **Analysis:**
- Clear convergence curve (monotonic increase toward target)
- Identifiable convergence cycle (~400-600)
- Reasonable stability (variance plateau)

✅ **Code Quality:**
- All tests passing (12+ new tests)
- Black/Flake8/Mypy clean
- Full documentation

✅ **Deliverables:**
- 30 seed trajectory files
- Aggregated statistics JSON
- Confidence band visualization
- Statistical report (markdown)

---

## Timeline

| Task | Duration | Checkpoint |
|------|----------|-----------|
| Implement MultiSeedRunner | 30 min | Save trajectories for 5 seeds |
| Implement ConvergenceAggregator | 30 min | Statistics computed correctly |
| Implement StatisticalValidator | 30 min | All tests pass |
| Write unit tests | 1 hour | 12+ tests green |
| Run 30-seed analysis | 45 min | Results saved to disk |
| Generate plots & report | 30 min | Visualizations ready |
| Documentation & cleanup | 30 min | README updated, commit ready |
| **Total** | **~4 hours** | Phase 5 COMPLETE |

---

## Known Risks

| Risk | Mitigation |
|------|-----------|
| 30 seeds take too long (> 2 hours) | Implement parallel execution (asyncio.gather) |
| Some seeds fail to converge | Log failures, calculate success_rate, don't stop |
| Memory issues with 30 seeds | Stream results to disk, don't keep all in memory |
| Divergent seeds cause high variance | Increase num_cycles or adjust hyperparameters |
| Plots don't show clear trends | Use smoothing (rolling average) or different y-scale |

---

## Next Steps

1. **Create files:** `multiseed_analysis.py`, `test_multiseed_analysis.py`
2. **Implement Step 1-4** in order
3. **Run quick smoke test** (5 seeds, 50 cycles each)
4. **Run full 30-seed analysis** (1000 cycles each)
5. **Generate plots & report**
6. **Update documentation**
7. **Commit to master**

---

## References

- Phase 4 report: `docs/PHASE_4_INTEGRATION_LOSS_REPORT.md`
- Training loop: `src/consciousness/integration_loss.py`
- Test examples: `tests/consciousness/test_integration_loss.py`

---

**Phase 5 Ready to Start** ✅
