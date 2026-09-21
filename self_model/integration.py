"""Owner-boundary integrations for Self Model M6-M9.

All integrations are projection-only. They consume owner state and expose
read-only Self Model views without taking ownership of lifecycle, temporal
calculation, goals, focus, memory, planning, permissions, risk, or actions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from .core import (
    CapabilityEvidence,
    CapabilityProjector,
    OperationalProjection,
    OperationalStateProjector,
    SourceValue,
)


def _mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return value if value is not None else {}


@dataclass(frozen=True)
class IntegratedSelfState:
    """Bounded coherent projection assembled from owner repositories."""

    fields: Mapping[str, SourceValue] = field(default_factory=dict)
    context: Mapping[str, Any] = field(default_factory=dict)
    source_trace: tuple[str, ...] = ()

    def values(self) -> dict[str, Any]:
        return {name: item.value for name, item in self.fields.items()}

    def owner_of(self, field_name: str) -> str | None:
        item = self.fields.get(field_name)
        return item.owner if item else None


class RuntimeTemporalIntegrator:
    """M6: Runtime operational state + Temporal Awareness metadata.

    Temporal Awareness remains the only freshness/duration owner. This class
    only applies owner-provided temporal metadata to projected fields.
    """

    def __init__(self) -> None:
        self._operational = OperationalStateProjector()

    def integrate(
        self,
        *,
        runtime_state: Mapping[str, Any] | None = None,
        planner_state: Mapping[str, Any] | None = None,
        temporal_state: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> IntegratedSelfState:
        projection: OperationalProjection = self._operational.project(
            runtime_state=runtime_state,
            planner_state=planner_state,
        )
        temporal_state = temporal_state or {}

        fields: dict[str, SourceValue] = {}
        trace: list[str] = []

        for name, item in projection.fields.items():
            temporal = temporal_state.get(name, {})
            freshness = temporal.get("freshness", item.freshness)
            observed_at = temporal.get("observed_at", item.observed_at)
            fields[name] = SourceValue(
                field=item.field,
                value=item.value,
                owner=item.owner,
                source=item.source,
                observed_at=observed_at,
                confidence=item.confidence,
                freshness=freshness,
            )
            trace.append(item.source)
            if temporal:
                trace.append(f"temporal_awareness.{name}")

        temporal_context = {
            name: {
                key: value
                for key, value in metadata.items()
                if key in {"age_seconds", "duration_seconds", "freshness", "observed_at"}
            }
            for name, metadata in temporal_state.items()
        }

        return IntegratedSelfState(
            fields=MappingProxyType(fields),
            context=MappingProxyType(
                {
                    "missing_operational_fields": projection.missing_fields,
                    "temporal": MappingProxyType(temporal_context),
                }
            ),
            source_trace=tuple(dict.fromkeys(trace)),
        )


class GoalsAttentionIntegrator:
    """M7: reflect Goals & Drives and Attention owner state."""

    def integrate(
        self,
        *,
        goals_state: Mapping[str, Any] | None = None,
        attention_state: Mapping[str, Any] | None = None,
    ) -> IntegratedSelfState:
        goals = _mapping(goals_state)
        attention = _mapping(attention_state)
        fields: dict[str, SourceValue] = {}
        trace: list[str] = []

        goal_fields = {
            "active_goal": "active_goal",
            "goal_blockers": "blockers",
            "goal_priority": "priority",
        }
        for self_field, owner_field in goal_fields.items():
            if owner_field in goals:
                fields[self_field] = SourceValue(
                    field=self_field,
                    value=goals[owner_field],
                    owner="goals_drives",
                    source=f"goals_drives.{owner_field}",
                    observed_at=goals.get("observed_at"),
                    confidence=goals.get("confidence", 1.0),
                    freshness=goals.get("freshness", "unknown"),
                )
                trace.append(f"goals_drives.{owner_field}")

        attention_fields = {
            "current_focus": "current_focus",
            "focus_reason": "focus_reason",
        }
        for self_field, owner_field in attention_fields.items():
            if owner_field in attention:
                fields[self_field] = SourceValue(
                    field=self_field,
                    value=attention[owner_field],
                    owner="attention",
                    source=f"attention.{owner_field}",
                    observed_at=attention.get("observed_at"),
                    confidence=attention.get("confidence", 1.0),
                    freshness=attention.get("freshness", "unknown"),
                )
                trace.append(f"attention.{owner_field}")

        return IntegratedSelfState(
            fields=MappingProxyType(fields),
            context=MappingProxyType({}),
            source_trace=tuple(trace),
        )


class WorldMemoryIntegrator:
    """M8: current environment relation + bounded historical context.

    World Model owns live environment state. Memory owns retained history.
    Self Model receives only a bounded projection of both.
    """

    def __init__(self, max_memory_items: int = 5) -> None:
        if max_memory_items < 0:
            raise ValueError("max_memory_items must be >= 0")
        self._max_memory_items = max_memory_items

    def integrate(
        self,
        *,
        world_state: Mapping[str, Any] | None = None,
        memory_items: Sequence[Mapping[str, Any]] | None = None,
    ) -> IntegratedSelfState:
        world = _mapping(world_state)
        memories = tuple(memory_items or ())
        fields: dict[str, SourceValue] = {}
        trace: list[str] = []

        if "self_relation" in world:
            fields["world_relation"] = SourceValue(
                field="world_relation",
                value=world["self_relation"],
                owner="world_model",
                source="world_model.self_relation",
                observed_at=world.get("observed_at"),
                confidence=world.get("confidence", 1.0),
                freshness=world.get("freshness", "unknown"),
            )
            trace.append("world_model.self_relation")

        bounded = memories[-self._max_memory_items :] if self._max_memory_items else ()
        selected_memories = tuple(
            {
                "memory_id": item.get("memory_id"),
                "summary": item.get("summary"),
                "source": item.get("source", "memory"),
                "relevance": item.get("relevance"),
            }
            for item in bounded
        )
        if selected_memories:
            trace.append("memory.selected_context")

        return IntegratedSelfState(
            fields=MappingProxyType(fields),
            context=MappingProxyType(
                {
                    "memory_context": selected_memories,
                    "memory_items_received": len(memories),
                    "memory_items_projected": len(selected_memories),
                }
            ),
            source_trace=tuple(trace),
        )


def merge_states(*states: IntegratedSelfState) -> IntegratedSelfState:
    """Merge projections without silently overwriting different owner values."""

    fields: dict[str, SourceValue] = {}
    context: dict[str, Any] = {}
    trace: list[str] = []

    for state in states:
        for name, item in state.fields.items():
            existing = fields.get(name)
            if existing is not None and (
                existing.value != item.value or existing.owner != item.owner
            ):
                raise ValueError(f"conflicting projections for field {name!r}")
            fields[name] = item
        context.update(state.context)
        trace.extend(state.source_trace)

    return IntegratedSelfState(
        fields=MappingProxyType(fields),
        context=MappingProxyType(context),
        source_trace=tuple(dict.fromkeys(trace)),
    )


class ConsumerViews:
    """M9: read-only Planner/Autonomy consumer views.

    No permission, risk, authorization or action decision is produced here.
    """

    FORBIDDEN_DECISION_KEYS = {
        "authorized",
        "authorization",
        "permission_decision",
        "risk_decision",
        "may_execute",
        "execute",
        "action_decision",
    }

    def planner_view(
        self,
        state: IntegratedSelfState,
        *,
        capability_evidence: Iterable[CapabilityEvidence] = (),
    ) -> Mapping[str, Any]:
        capabilities = CapabilityProjector().project(capability_evidence)
        view = {
            "self_state": state.values(),
            "capabilities": {
                name: capabilities.state_of(name)
                for name in capabilities.capabilities
            },
            "source_trace": state.source_trace,
        }
        return MappingProxyType(view)

    def autonomy_view(
        self,
        state: IntegratedSelfState,
        *,
        blockers: Sequence[str] = (),
        limitations: Sequence[str] = (),
    ) -> Mapping[str, Any]:
        view = {
            "self_state": state.values(),
            "blockers": tuple(blockers),
            "limitations": tuple(limitations),
            "source_trace": state.source_trace,
        }
        self._assert_no_decisions(view)
        return MappingProxyType(view)

    def _assert_no_decisions(self, view: Mapping[str, Any]) -> None:
        keys = set(view)
        forbidden = keys & self.FORBIDDEN_DECISION_KEYS
        if forbidden:
            raise ValueError(
                "Self Model consumer view attempted to own decisions: "
                + ", ".join(sorted(forbidden))
            )
