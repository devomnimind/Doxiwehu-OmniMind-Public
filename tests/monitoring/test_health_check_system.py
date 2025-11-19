"""Tests for advanced health check system."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.backend.monitoring.health_check_system import (
    DependencyType,
    HealthCheckResult,
    HealthCheckSystem,
    HealthStatus,
    HealthThresholds,
)


@pytest.fixture
def health_system():
    """Create health check system for testing."""
    return HealthCheckSystem(check_interval_seconds=1)


@pytest.fixture
def custom_thresholds():
    """Create custom thresholds for testing."""
    return HealthThresholds(
        response_time_warning_ms=500.0,
        response_time_critical_ms=2000.0,
        cpu_usage_warning=70.0,
        cpu_usage_critical=90.0,
        memory_usage_warning=75.0,
        memory_usage_critical=90.0,
    )


class TestHealthCheckResult:
    """Test HealthCheckResult dataclass."""

    def test_result_creation(self):
        """Test creating a health check result."""
        result = HealthCheckResult(
            name="test_check",
            dependency_type=DependencyType.DATABASE,
            status=HealthStatus.HEALTHY,
            response_time_ms=50.0,
            details={"connection": "active"},
        )

        assert result.name == "test_check"
        assert result.dependency_type == DependencyType.DATABASE
        assert result.status == HealthStatus.HEALTHY
        assert result.response_time_ms == 50.0
        assert result.details["connection"] == "active"
        assert result.error is None
        assert not result.threshold_breached


class TestHealthCheckSystem:
    """Test HealthCheckSystem class."""

    def test_initialization(self, custom_thresholds):
        """Test system initialization."""
        system = HealthCheckSystem(
            thresholds=custom_thresholds,
            check_interval_seconds=30,
        )

        assert system.thresholds.cpu_usage_warning == 70.0
        assert system.check_interval == 30
        assert not system._running

    @pytest.mark.asyncio
    async def test_check_database(self, health_system):
        """Test database health check."""
        result = await health_system.check_database()

        assert result.name == "database"
        assert result.dependency_type == DependencyType.DATABASE
        assert isinstance(result.status, HealthStatus)
        assert result.response_time_ms >= 0

    @pytest.mark.asyncio
    async def test_run_all_checks(self, health_system):
        """Test running all health checks."""
        results = await health_system.run_all_checks()

        assert len(results) >= 6
        assert "database" in results
        assert "redis" in results
        assert "gpu" in results

    def test_get_overall_status_healthy(self, health_system):
        """Test overall status when all checks are healthy."""
        results = {
            "db": HealthCheckResult(
                name="db",
                dependency_type=DependencyType.DATABASE,
                status=HealthStatus.HEALTHY,
                response_time_ms=50.0,
            ),
        }

        status = health_system.get_overall_status(results)
        assert status == HealthStatus.HEALTHY

    def test_get_health_trends_insufficient_data(self, health_system):
        """Test trends with insufficient data."""
        trends = health_system.get_health_trends("nonexistent")

        assert trends["trend"] == "unknown"
        assert trends["prediction"] == "insufficient_data"

    @pytest.mark.asyncio
    async def test_monitoring_lifecycle(self, health_system):
        """Test starting and stopping monitoring."""
        assert not health_system._running

        await health_system.start_monitoring()
        assert health_system._running

        await asyncio.sleep(0.1)

        await health_system.stop_monitoring()
        assert not health_system._running
