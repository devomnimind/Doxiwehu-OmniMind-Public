import numpy as np
import pytest

from src.consciousness.topological_phi import PhiCalculator, SimplicialComplex


def _build_simple_complex() -> SimplicialComplex:
    complex_ = SimplicialComplex()
    complex_.add_simplex((0,))
    complex_.add_simplex((1,))
    complex_.add_simplex((0, 1))
    return complex_


@pytest.mark.asyncio
async def test_topological_hybrid_validation_runs() -> None:
    complex_ = _build_simple_complex()
    calc = PhiCalculator(complex_)

    # Pequena matriz de estados artificiais
    states = np.random.randn(4, 4)

    result = await calc.calculate_with_quantum_validation(states)

    assert "phi_classical" in result
    assert "phi_quantum" in result
    assert "fidelity" in result
    assert "phi_topological" in result
    assert 0.0 <= result["phi_topological"] <= 1.0
