"""Observability module for distributed tracing, metrics, and logging.

This module implements comprehensive observability features including:
- Distributed tracing with OpenTelemetry
- Custom metrics exporters for ML workloads
- Advanced log aggregation and analysis
- Continuous performance profiling
- Performance bottleneck analysis

Reference: docs/OMNIMIND_COMPREHENSIVE_PENDENCIES_REPORT_20251119.md, Section 8
"""

from src.observability.distributed_tracing import (
    DistributedTracer,
    SpanContext,
    TraceConfig,
)
from src.observability.metrics_exporter import (
    CustomMetricsExporter,
    MLMetrics,
    MetricsConfig,
)
from src.observability.log_aggregator import (
    LogAggregator,
    LogAnalytics,
    LogConfig,
)
from src.observability.profiling_tools import (
    ContinuousProfiler,
    FlameGraphGenerator,
    ProfilingConfig,
)
from src.observability.opentelemetry_integration import (
    OpenTelemetryConfig,
    OpenTelemetryIntegration,
)
from src.observability.performance_analyzer import (
    PerformanceAnalyzer,
    PerformanceBottleneck,
    PerformanceReport,
)

__all__ = [
    # Distributed tracing
    "DistributedTracer",
    "SpanContext",
    "TraceConfig",
    # OpenTelemetry
    "OpenTelemetryConfig",
    "OpenTelemetryIntegration",
    # Metrics
    "CustomMetricsExporter",
    "MLMetrics",
    "MetricsConfig",
    # Logging
    "LogAggregator",
    "LogAnalytics",
    "LogConfig",
    # Profiling
    "ContinuousProfiler",
    "FlameGraphGenerator",
    "ProfilingConfig",
    # Performance Analysis
    "PerformanceAnalyzer",
    "PerformanceBottleneck",
    "PerformanceReport",
]
