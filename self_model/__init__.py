"""NeuroForge Self Model.

Projection-only operational self-state. Owner repositories remain authoritative.
"""

from .core import (
    ActionOutcome,
    ActionOutcomeProjector,
    CapabilityEvidence,
    CapabilityProjection,
    CapabilityProjector,
    KnowledgeClaim,
    KnowledgeProjection,
    KnowledgeProjector,
    OperationalProjection,
    OperationalStateProjector,
    ReconciliationOutcome,
    SelfStateReconciler,
    SourceValue,
)

__all__ = [
    "ActionOutcome",
    "ActionOutcomeProjector",
    "CapabilityEvidence",
    "CapabilityProjection",
    "CapabilityProjector",
    "KnowledgeClaim",
    "KnowledgeProjection",
    "KnowledgeProjector",
    "OperationalProjection",
    "OperationalStateProjector",
    "ReconciliationOutcome",
    "SelfStateReconciler",
    "SourceValue",
]


from .integration import (
    ConsumerViews,
    GoalsAttentionIntegrator,
    IntegratedSelfState,
    RuntimeTemporalIntegrator,
    WorldMemoryIntegrator,
    merge_states,
)
from .acceptance import (
    AcceptanceResult,
    AcceptanceThresholds,
    RealPCAcceptanceHarness,
    RealPCEvidence,
)

__all__ += [
    "ConsumerViews",
    "GoalsAttentionIntegrator",
    "IntegratedSelfState",
    "RuntimeTemporalIntegrator",
    "WorldMemoryIntegrator",
    "merge_states",
    "AcceptanceResult",
    "AcceptanceThresholds",
    "RealPCAcceptanceHarness",
    "RealPCEvidence",
]
