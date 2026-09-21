"""M10 real-PC acceptance harness.

This harness is intentionally fail-closed. It can validate evidence, but it
cannot manufacture real Windows evidence. CI is not required by this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .integration import IntegratedSelfState


@dataclass(frozen=True)
class AcceptanceThresholds:
    min_duration_seconds: float
    max_avg_cpu_percent: float
    max_peak_memory_mb: float

    def __post_init__(self) -> None:
        if self.min_duration_seconds <= 0:
            raise ValueError("min_duration_seconds must be > 0")
        if self.max_avg_cpu_percent <= 0:
            raise ValueError("max_avg_cpu_percent must be > 0")
        if self.max_peak_memory_mb <= 0:
            raise ValueError("max_peak_memory_mb must be > 0")


@dataclass(frozen=True)
class RealPCEvidence:
    platform: str
    real_owner_sources: bool
    duration_seconds: float
    avg_cpu_percent: float
    peak_memory_mb: float
    stale_scenario_passed: bool
    conflict_scenario_passed: bool
    stop_on_missing_owner_evidence: bool


@dataclass(frozen=True)
class AcceptanceResult:
    passed: bool
    reasons: tuple[str, ...]


class RealPCAcceptanceHarness:
    """Validate M10 evidence without treating simulated/CI data as real-PC PASS."""

    def evaluate(
        self,
        *,
        snapshots: Iterable[IntegratedSelfState],
        evidence: RealPCEvidence,
        thresholds: AcceptanceThresholds,
    ) -> AcceptanceResult:
        snapshots = tuple(snapshots)
        reasons: list[str] = []

        if evidence.platform.lower() != "windows":
            reasons.append("real_windows_required")
        if not evidence.real_owner_sources:
            reasons.append("real_owner_sources_required")
        if not snapshots:
            reasons.append("continuous_snapshots_required")
        if evidence.duration_seconds < thresholds.min_duration_seconds:
            reasons.append("long_session_duration_not_met")
        if evidence.avg_cpu_percent > thresholds.max_avg_cpu_percent:
            reasons.append("cpu_budget_exceeded")
        if evidence.peak_memory_mb > thresholds.max_peak_memory_mb:
            reasons.append("memory_budget_exceeded")
        if not evidence.stale_scenario_passed:
            reasons.append("stale_state_scenario_failed")
        if not evidence.conflict_scenario_passed:
            reasons.append("conflict_scenario_failed")
        if not evidence.stop_on_missing_owner_evidence:
            reasons.append("fail_closed_owner_evidence_missing")

        for snapshot in snapshots:
            if not snapshot.source_trace:
                reasons.append("source_trace_missing")
                break
            for item in snapshot.fields.values():
                if not item.owner or not item.source:
                    reasons.append("untraceable_self_state_field")
                    break

        return AcceptanceResult(passed=not reasons, reasons=tuple(dict.fromkeys(reasons)))
