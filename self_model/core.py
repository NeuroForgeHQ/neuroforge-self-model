"""Drift-clean Self Model implementation for M1-M5.

The module is deliberately projection-only:
- it never mutates Runtime/Planner task lifecycle;
- it never becomes a capability authority;
- it never acts as a general knowledge base;
- it never executes or verifies actions;
- it consumes freshness classifications instead of calculating them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence


VALID_CONFIDENCE_MIN = 0.0
VALID_CONFIDENCE_MAX = 1.0

OPERATIONAL_OWNERS = {
    "current_task": "runtime",
    "session": "runtime",
    "active_module": "runtime",
    "active_process": "runtime",
    "current_subtask": "planner",
    "execution_state": "planner",
}

CAPABILITY_OWNERS = {
    "runtime",
    "tools",
    "voice",
    "vision",
    "desktop_context",
    "planner",
    "memory",
    "world_model",
    "temporal_awareness",
    "attention",
    "goals_drives",
    "autonomy",
    "self_recovery",
}

SELF_KNOWLEDGE_CATEGORIES = {
    "current_task",
    "current_subtask",
    "active_goal",
    "current_focus",
    "required_tool",
    "current_screen_state",
    "last_action_result",
    "capability",
    "limitation",
    "blocker",
    "permission",
}

KNOWLEDGE_STATES = {
    "known",
    "unknown",
    "uncertain",
    "stale",
    "conflicted",
    "not_observed",
}

FRESHNESS_STATES = {
    "fresh",
    "recent",
    "aging",
    "stale",
    "expired",
    "unknown",
}


def _validate_confidence(value: float) -> float:
    value = float(value)
    if not VALID_CONFIDENCE_MIN <= value <= VALID_CONFIDENCE_MAX:
        raise ValueError("confidence must be between 0.0 and 1.0")
    return value


def _require_text(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class SourceValue:
    """One owner-sourced self-state candidate.

    `freshness` is supplied by Temporal Awareness or another owner contract.
    Self Model does not compute it.
    """

    field: str
    value: Any
    owner: str
    source: str
    observed_at: str | None = None
    confidence: float = 1.0
    freshness: str = "unknown"

    def __post_init__(self) -> None:
        object.__setattr__(self, "field", _require_text("field", self.field))
        object.__setattr__(self, "owner", _require_text("owner", self.owner))
        object.__setattr__(self, "source", _require_text("source", self.source))
        object.__setattr__(self, "confidence", _validate_confidence(self.confidence))
        if self.freshness not in FRESHNESS_STATES:
            raise ValueError(f"unsupported freshness state: {self.freshness}")


@dataclass(frozen=True)
class OperationalProjection:
    fields: Mapping[str, SourceValue]
    missing_fields: tuple[str, ...] = ()

    def snapshot(self) -> dict[str, Any]:
        return {key: item.value for key, item in self.fields.items()}


class OperationalStateProjector:
    """M1: read-only projection of Runtime/Planner-owned operational state."""

    def project(
        self,
        *,
        runtime_state: Mapping[str, Any] | None = None,
        planner_state: Mapping[str, Any] | None = None,
    ) -> OperationalProjection:
        runtime_state = runtime_state or {}
        planner_state = planner_state or {}
        sources = {"runtime": runtime_state, "planner": planner_state}

        fields: dict[str, SourceValue] = {}
        missing: list[str] = []

        for field_name, owner in OPERATIONAL_OWNERS.items():
            owner_state = sources[owner]
            if field_name not in owner_state:
                missing.append(field_name)
                continue

            fields[field_name] = SourceValue(
                field=field_name,
                value=owner_state[field_name],
                owner=owner,
                source=f"{owner}.{field_name}",
                observed_at=owner_state.get("observed_at"),
                confidence=owner_state.get("confidence", 1.0),
                freshness=owner_state.get("freshness", "unknown"),
            )

        return OperationalProjection(fields=fields, missing_fields=tuple(missing))


@dataclass(frozen=True)
class CapabilityEvidence:
    capability: str
    state: str
    owner: str
    source: str
    confidence: float = 1.0
    permission_requirement: str | None = None
    blocker: str | None = None
    resource_limit: str | None = None
    observed_at: str | None = None
    freshness: str = "unknown"

    def __post_init__(self) -> None:
        object.__setattr__(self, "capability", _require_text("capability", self.capability))
        object.__setattr__(self, "state", _require_text("state", self.state))
        object.__setattr__(self, "owner", _require_text("owner", self.owner))
        object.__setattr__(self, "source", _require_text("source", self.source))
        object.__setattr__(self, "confidence", _validate_confidence(self.confidence))
        if self.owner not in CAPABILITY_OWNERS:
            raise ValueError(f"unrecognized capability owner: {self.owner}")
        if self.freshness not in FRESHNESS_STATES:
            raise ValueError(f"unsupported freshness state: {self.freshness}")


@dataclass(frozen=True)
class CapabilityProjection:
    capabilities: Mapping[str, tuple[CapabilityEvidence, ...]]

    def state_of(self, capability: str) -> str:
        evidence = self.capabilities.get(capability, ())
        if not evidence:
            return "unknown"
        states = {item.state for item in evidence}
        return next(iter(states)) if len(states) == 1 else "conflicted"


class CapabilityProjector:
    """M2: represent capability evidence without becoming capability authority."""

    def project(self, evidence: Iterable[CapabilityEvidence]) -> CapabilityProjection:
        grouped: dict[str, list[CapabilityEvidence]] = {}
        for item in evidence:
            grouped.setdefault(item.capability, []).append(item)

        frozen = {name: tuple(items) for name, items in grouped.items()}
        return CapabilityProjection(capabilities=frozen)


@dataclass(frozen=True)
class KnowledgeClaim:
    category: str
    key: str
    state: str
    owner: str
    source: str
    value: Any = None
    confidence: float = 1.0
    observed_at: str | None = None
    freshness: str = "unknown"

    def __post_init__(self) -> None:
        if self.category not in SELF_KNOWLEDGE_CATEGORIES:
            raise ValueError(
                f"category {self.category!r} is outside Self Model ownership"
            )
        object.__setattr__(self, "key", _require_text("key", self.key))
        object.__setattr__(self, "owner", _require_text("owner", self.owner))
        object.__setattr__(self, "source", _require_text("source", self.source))
        object.__setattr__(self, "confidence", _validate_confidence(self.confidence))
        if self.state not in KNOWLEDGE_STATES:
            raise ValueError(f"unsupported knowledge state: {self.state}")
        if self.freshness not in FRESHNESS_STATES:
            raise ValueError(f"unsupported freshness state: {self.freshness}")


@dataclass(frozen=True)
class KnowledgeProjection:
    claims: Mapping[str, KnowledgeClaim]

    def get(self, key: str) -> KnowledgeClaim | None:
        return self.claims.get(key)


class KnowledgeProjector:
    """M3: bounded self-relevant epistemic state, not general knowledge."""

    def project(self, claims: Iterable[KnowledgeClaim]) -> KnowledgeProjection:
        result: dict[str, KnowledgeClaim] = {}
        for claim in claims:
            previous = result.get(claim.key)
            if previous is None or claim.confidence > previous.confidence:
                result[claim.key] = claim
            elif previous.value != claim.value or previous.state != claim.state:
                result[claim.key] = KnowledgeClaim(
                    category=claim.category,
                    key=claim.key,
                    state="conflicted",
                    owner="self_model",
                    source=f"conflict:{previous.source}|{claim.source}",
                    value=None,
                    confidence=min(previous.confidence, claim.confidence),
                    freshness="unknown",
                )
        return KnowledgeProjection(claims=result)


@dataclass(frozen=True)
class ActionOutcome:
    action_id: str
    action: str
    owner: str
    source: str
    result: str | None = None
    verified: bool = False
    verified_by: str | None = None
    observed_at: str | None = None
    confidence: float = 1.0

    def __post_init__(self) -> None:
        object.__setattr__(self, "action_id", _require_text("action_id", self.action_id))
        object.__setattr__(self, "action", _require_text("action", self.action))
        object.__setattr__(self, "owner", _require_text("owner", self.owner))
        object.__setattr__(self, "source", _require_text("source", self.source))
        object.__setattr__(self, "confidence", _validate_confidence(self.confidence))
        if self.verified and not self.verified_by:
            raise ValueError("verified outcomes require verified_by provenance")

    @property
    def projected_result(self) -> str:
        if not self.verified:
            return "unverified"
        return self.result if self.result is not None else "verified_unknown"


@dataclass(frozen=True)
class ActionProjection:
    recent: tuple[ActionOutcome, ...]

    @property
    def last_action(self) -> ActionOutcome | None:
        return self.recent[-1] if self.recent else None


class ActionOutcomeProjector:
    """M4: bounded reflection of owner-verified outcomes."""

    def __init__(self, max_items: int = 8) -> None:
        if max_items < 1:
            raise ValueError("max_items must be >= 1")
        self._max_items = max_items

    def project(self, outcomes: Sequence[ActionOutcome]) -> ActionProjection:
        # Input order is owner-provided event order. Self Model does not create
        # or persist a separate historical event store.
        recent = tuple(outcomes[-self._max_items :])
        return ActionProjection(recent=recent)


@dataclass(frozen=True)
class ReconciliationOutcome:
    field: str
    status: str
    selected: SourceValue | None
    candidates: tuple[SourceValue, ...]
    refresh_requested: bool = False
    reasons: tuple[str, ...] = field(default_factory=tuple)


class SelfStateReconciler:
    """M5: conflict detection and freshness consumption.

    Freshness is never derived here. It is consumed from SourceValue.
    """

    def reconcile(
        self,
        field_name: str,
        candidates: Iterable[SourceValue],
        *,
        expected_owner: str | None = None,
    ) -> ReconciliationOutcome:
        field_name = _require_text("field_name", field_name)
        items = tuple(item for item in candidates if item.field == field_name)

        if not items:
            return ReconciliationOutcome(
                field=field_name,
                status="unknown",
                selected=None,
                candidates=(),
                refresh_requested=True,
                reasons=("no_evidence",),
            )

        live = tuple(
            item for item in items if item.freshness not in {"stale", "expired"}
        )
        if not live:
            return ReconciliationOutcome(
                field=field_name,
                status="stale",
                selected=None,
                candidates=items,
                refresh_requested=True,
                reasons=("all_evidence_stale_or_expired",),
            )

        distinct_values = {repr(item.value) for item in live}
        if len(distinct_values) > 1:
            selected = None
            reasons = ["conflicting_values"]
            if expected_owner:
                owner_candidates = [item for item in live if item.owner == expected_owner]
                if len(owner_candidates) == 1:
                    selected = owner_candidates[0]
                    reasons.append("expected_owner_candidate_available")
            return ReconciliationOutcome(
                field=field_name,
                status="conflicted",
                selected=selected,
                candidates=items,
                refresh_requested=True,
                reasons=tuple(reasons),
            )

        selected = max(live, key=lambda item: item.confidence)
        status = "known" if selected.freshness in {"fresh", "recent", "unknown"} else "aging"
        return ReconciliationOutcome(
            field=field_name,
            status=status,
            selected=selected,
            candidates=items,
            refresh_requested=False,
            reasons=("consistent_evidence",),
        )
