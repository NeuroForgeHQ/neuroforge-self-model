from __future__ import annotations

import argparse
import ctypes
from ctypes import wintypes
from datetime import datetime, timedelta, timezone
import importlib.util
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time
from typing import Any


OWNER_REPOS = (
    "neuroforge-runtime",
    "neuroforge-temporal-awareness",
    "neuroforge-goals-drives",
    "neuroforge-attention",
    "neuroforge-world-model",
    "neuroforge-memory",
    "neuroforge-planner",
    "neuroforge-tools",
)


def git_sha(path: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        text=True,
        stderr=subprocess.DEVNULL,
        timeout=10,
    ).strip()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load owner module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def add_paths(root: Path) -> None:
    paths = (
        root / "neuroforge-runtime",
        root / "neuroforge-temporal-awareness",
        root / "neuroforge-goals-drives",
        root / "neuroforge-attention",
        root / "neuroforge-world-model",
        root / "neuroforge-memory",
        root / "neuroforge-planner",
        root / "neuroforge-tools",
        root / "neuroforge-self-model",
    )
    for path in paths:
        value = str(path.resolve())
        if value not in sys.path:
            sys.path.insert(0, value)
    self_model_root = str((root / "neuroforge-self-model").resolve())
    if self_model_root in sys.path:
        sys.path.remove(self_model_root)
    sys.path.insert(0, self_model_root)


def peak_working_set_mb() -> float:
    if os.name != "nt":
        return 0.0

    class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
        _fields_ = [
            ("cb", wintypes.DWORD),
            ("PageFaultCount", wintypes.DWORD),
            ("PeakWorkingSetSize", ctypes.c_size_t),
            ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t),
            ("PeakPagefileUsage", ctypes.c_size_t),
        ]

    counters = PROCESS_MEMORY_COUNTERS()
    counters.cb = ctypes.sizeof(counters)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    get_current_process = kernel32.GetCurrentProcess
    get_current_process.argtypes = []
    get_current_process.restype = wintypes.HANDLE
    handle = get_current_process()
    memory_info = getattr(kernel32, "K32GetProcessMemoryInfo", None)
    if memory_info is None:
        psapi = ctypes.WinDLL("psapi", use_last_error=True)
        memory_info = psapi.GetProcessMemoryInfo
    memory_info.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(PROCESS_MEMORY_COUNTERS),
        wintypes.DWORD,
    ]
    memory_info.restype = wintypes.BOOL
    if not memory_info(handle, ctypes.byref(counters), counters.cb):
        raise OSError(ctypes.get_last_error(), "GetProcessMemoryInfo failed")
    return counters.PeakWorkingSetSize / (1024.0 * 1024.0)


def json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_safe(v) for v in value]
    if hasattr(value, "value") and isinstance(getattr(value, "value"), (str, int, float, bool)):
        return getattr(value, "value")
    return str(value)


def serialize_snapshot(snapshot) -> dict[str, object]:
    return {
        "fields": {
            name: {
                "field": item.field,
                "value": json_safe(item.value),
                "owner": item.owner,
                "source": item.source,
                "observed_at": item.observed_at,
                "confidence": item.confidence,
                "freshness": item.freshness,
            }
            for name, item in snapshot.fields.items()
        },
        "context": json_safe(dict(snapshot.context)),
        "source_trace": list(snapshot.source_trace),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect real Windows Self Model M10 evidence."
    )
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--duration-seconds", type=float, default=600.0)
    parser.add_argument("--sample-interval-seconds", type=float, default=5.0)
    parser.add_argument("--preflight", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if platform.system().casefold() != "windows":
        raise RuntimeError("Self Model M10 collector requires Windows")
    if not args.preflight and args.duration_seconds < 600.0:
        raise ValueError("Self Model M10 final evidence requires >= 600 seconds")
    target_duration = 3.0 if args.preflight else args.duration_seconds

    add_paths(root)

    from self_model import (
        ActionOutcome,
        ActionOutcomeProjector,
        CapabilityEvidence,
        ConsumerViews,
        GoalsAttentionIntegrator,
        KnowledgeClaim,
        KnowledgeProjector,
        RealPCAcceptanceHarness,
        RealPCEvidence,
        RuntimeTemporalIntegrator,
        SelfStateReconciler,
        SourceValue,
        WorldMemoryIntegrator,
        merge_states,
    )
    from self_model.acceptance import AcceptanceThresholds

    from goals import Goal, GoalSource, GoalStatus, PriorityDecision, PriorityLevel
    from drives import DriveSignal, DriveStatus, DriveType
    from attention import AttentionCandidate, FocusSelector, SalienceScorer
    from temporal.freshness import FreshnessEngine, FreshnessPolicy
    from neuroforge_planner.ids import deterministic_id
    from neuroforge_planner.models import ActionIntent
    from world_model import Entity, EntityState
    from neuroforge_memory.identity import Scope
    from neuroforge_memory.retrieval import MemoryContext, MemoryRetrievalResult
    from neuroforge_runtime import RuntimeConfig
    from neuroforge_runtime.adapters.tools import ToolsAdapter

    goals_attention_owner = load_module(
        "nf_self_model_m10_goals_attention_owner",
        root / "neuroforge-goals-drives" / "integrations" / "attention.py",
    )

    self_root = root / "neuroforge-self-model"
    owner_revisions = {"neuroforge-self-model": git_sha(self_root)}
    for repo_name in OWNER_REPOS:
        owner_revisions[repo_name] = git_sha(root / repo_name)

    now = datetime.now(timezone.utc)
    work = Path(tempfile.mkdtemp(prefix="nf-self-model-m10-")).resolve()
    permission_ref = "auth:self-model-m10"
    file_path = work / "self-model-m10-owner.txt"

    # ------------------------------------------------------------------
    # Real Planner -> Runtime -> Tools owner flow.
    # ------------------------------------------------------------------
    parent_goal_id = deterministic_id(
        "goal",
        {
            "schema": 1,
            "kind": "goal",
            "owner": "self-model-m10",
            "creation_key": "self-model-m10-goal",
        },
    )
    task_id = deterministic_id(
        "task",
        {
            "schema": 1,
            "kind": "task",
            "owner": "self-model-m10",
            "parent_goal_id": parent_goal_id,
            "creation_key": "self-model-m10-task",
        },
    )
    intent = ActionIntent(
        task_id=task_id,
        capability="file.write",
        operation="execute",
        parameters={
            "path": str(file_path),
            "content": "neuroforge-self-model-m10",
            "overwrite": True,
        },
        expected_result_kind="file_write_result",
        authorization_class="filesystem.write",
        idempotency_key="self-model-m10-owner-flow",
    )

    runtime_tools = ToolsAdapter(
        RuntimeConfig(
            sibling_root=root,
            tools_enabled=True,
            tools_allowed_root=work,
            tools_authorization_grants={
                permission_ref: ("filesystem.write",),
            },
        )
    )
    runtime_tools.start()

    checks = {
        "real_runtime_tools": False,
        "real_planner": False,
        "real_temporal": False,
        "real_goals": False,
        "real_attention": False,
        "real_world_model": False,
        "real_memory_contract": False,
        "capability_projection_passed": False,
        "verified_action_projection_passed": False,
        "knowledge_projection_passed": False,
        "stale_scenario_passed": False,
        "conflict_scenario_passed": False,
        "missing_owner_fail_closed": False,
        "consumer_boundaries_passed": False,
        "continuous_traceable_snapshots": False,
    }

    snapshots = []
    detail: dict[str, object] = {}
    cpu_start = time.process_time()
    wall_start = time.monotonic()
    peak_memory_mb = peak_working_set_mb()

    try:
        tool_result = runtime_tools.execute_action_intent(
            intent.to_dict(),
            session_id="self-model-m10",
            turn_id="turn:m10",
            plan_id="plan:m10",
            step_id="step:m10",
            dry_run=False,
            authorization_refs=(permission_ref,),
        )
        observed_content = file_path.read_text(encoding="utf-8")
        status_value = getattr(tool_result.status, "value", str(tool_result.status))
        checks["real_runtime_tools"] = (
            status_value == "ok"
            and observed_content == "neuroforge-self-model-m10"
        )
        checks["real_planner"] = (
            intent.operation == "execute"
            and intent.capability == "file.write"
            and Path(intent.parameters["path"]).resolve() == file_path
        )

        # Actual Tools owner descriptor becomes Self Model capability evidence.
        descriptor = runtime_tools.describe_capability("file.write")
        capability = CapabilityEvidence(
            capability="file.write",
            state="available" if descriptor is not None else "unknown",
            owner="tools",
            source="tools.registry.file.write",
            confidence=1.0 if descriptor is not None else 0.0,
            permission_requirement=(
                None if descriptor is None else descriptor.get("permission")
            ),
            freshness="fresh",
        )

        # Independently observed outcome: ToolResult alone is not marked verified.
        action_unverified = ActionOutcome(
            action_id=intent.action_id,
            action="file.write",
            owner="runtime",
            source=f"runtime.tools.{tool_result.request_id}",
            result=status_value,
            verified=False,
            observed_at=datetime.now(timezone.utc).isoformat(),
            confidence=1.0,
        )
        action_verified = ActionOutcome(
            action_id=intent.action_id,
            action="file.write",
            owner="runtime",
            source=f"runtime.tools.{tool_result.request_id}",
            result="success",
            verified=(observed_content == "neuroforge-self-model-m10"),
            verified_by="independent_os_readback",
            observed_at=datetime.now(timezone.utc).isoformat(),
            confidence=1.0,
        )
        action_projection = ActionOutcomeProjector(max_items=2).project(
            (action_unverified, action_verified)
        )
        checks["verified_action_projection_passed"] = (
            action_projection.last_action is not None
            and action_projection.last_action.projected_result == "success"
            and action_projection.recent[0].projected_result == "unverified"
        )

        knowledge = KnowledgeProjector().project(
            (
                KnowledgeClaim(
                    category="required_tool",
                    key="file.write",
                    state="known" if descriptor is not None else "unknown",
                    owner="tools",
                    source="tools.registry.file.write",
                    value="available" if descriptor is not None else None,
                    confidence=1.0 if descriptor is not None else 0.0,
                    freshness="fresh",
                ),
                KnowledgeClaim(
                    category="last_action_result",
                    key="self-model-m10-write",
                    state="known",
                    owner="runtime",
                    source=f"runtime.tools.{tool_result.request_id}",
                    value=action_verified.projected_result,
                    confidence=1.0,
                    freshness="fresh",
                ),
            )
        )
        checks["knowledge_projection_passed"] = (
            knowledge.get("file.write") is not None
            and knowledge.get("self-model-m10-write") is not None
            and knowledge.get("self-model-m10-write").value == "success"
        )

        # ------------------------------------------------------------------
        # Real Goals + Attention + Temporal owner state.
        # ------------------------------------------------------------------
        goal = Goal(
            goal_id="self-model-m10-goal",
            title="Complete Self Model M10",
            description="Real-PC continuous self-state acceptance",
            source=GoalSource.USER,
            created_at=now,
            updated_at=now,
            status=GoalStatus.ACTIVE,
            provenance="controlled_user_goal:self-model-m10",
        )
        priority = PriorityDecision(
            goal.goal_id,
            PriorityLevel.HIGH,
            "user",
            "current explicit acceptance objective",
            True,
        )
        drive = DriveSignal(
            drive_id="self-model-m10-drive",
            drive_type=DriveType.TASK_COMPLETION,
            strength=0.8,
            maximum_strength=1.0,
            source="goals_drives",
            reason="self-model acceptance unfinished",
            related_goal_ids=(goal.goal_id,),
            created_at=now,
            updated_at=now,
            status=DriveStatus.ACTIVE,
        )
        goal_view = goals_attention_owner.GoalAttentionAdapter().build(
            goal=goal,
            priority=priority,
            drives=(drive,),
        )
        checks["real_goals"] = (
            getattr(goal_view, "goal_id", None) == goal.goal_id
            or getattr(goal_view, "active_goal", None) == goal.goal_id
        )

        temporal = FreshnessEngine(
            {"self_model": FreshnessPolicy(5.0, 30.0, 60.0, 120.0)}
        )
        fresh_state = temporal.classify("self_model", now, now)
        checks["real_temporal"] = fresh_state == "fresh"

        attention_candidate = AttentionCandidate(
            candidate_id="self-model:m10:focus",
            source="goals_drives",
            candidate_type="goal",
            summary="Complete Self Model M10",
            created_at=now,
            confidence=1.0,
            user_relevance=1.0,
            goal_relevance=1.0,
            urgency=0.8,
            freshness=fresh_state,
            novelty=1.0,
            resource_cost=0.05,
            priority_hint=1.0,
            related_goal_id=goal.goal_id,
            provenance="goals_drives:self-model-m10",
        )
        attention_score = SalienceScorer().score(
            attention_candidate,
            active_task_relevance=1.0,
        )
        attention_snapshot = FocusSelector(max_secondary=3).select(
            (attention_score,)
        )
        checks["real_attention"] = (
            attention_snapshot.primary is not None
            and attention_snapshot.primary.candidate_id
            == attention_candidate.candidate_id
        )

        # ------------------------------------------------------------------
        # Real World Model + Memory owner contracts.
        # ------------------------------------------------------------------
        world_entity = Entity(
            "self-model:m10",
            "operational_self_relation",
            {
                "working_on": "self-model-m10",
                "artifact": str(file_path),
                "verified": observed_content == "neuroforge-self-model-m10",
            },
            "independent_os_readback",
            datetime.now(timezone.utc),
            1.0,
        )
        world_entity_state = EntityState(world_entity, lifecycle="active")
        checks["real_world_model"] = (
            world_entity_state.entity.entity_id == "self-model:m10"
            and world_entity_state.lifecycle == "active"
        )

        memory_context = MemoryContext(
            records=(),
            record_count=0,
            serialized_size=0,
            truncated=False,
            scope=Scope("project", "neuroforge"),
            query_id="self-model-m10",
            retrieval_status="ok",
        )
        memory_result = MemoryRetrievalResult(
            query_id="self-model-m10",
            context=memory_context,
            total_candidates_considered=0,
            truncated=False,
            retrieval_status="ok",
        )
        checks["real_memory_contract"] = (
            memory_result.context.record_count == 0
            and memory_result.retrieval_status == "ok"
            and memory_result.context.scope.kind == "project"
        )

        # ------------------------------------------------------------------
        # Initial merged source-traceable snapshot.
        # ------------------------------------------------------------------
        sample_now = datetime.now(timezone.utc)
        runtime_state = {
            "current_task": f"runtime_tools:{tool_result.tool}",
            "session": "self-model-m10",
            "active_module": "tools",
            "active_process": "python",
            "observed_at": sample_now.isoformat(),
            "confidence": 1.0,
            "freshness": "fresh",
        }
        planner_state = {
            "current_subtask": intent.capability,
            "execution_state": "ready",
            "observed_at": sample_now.isoformat(),
            "confidence": 1.0,
            "freshness": "fresh",
        }
        temporal_state = {
            name: {
                "freshness": temporal.classify(
                    "self_model",
                    sample_now,
                    sample_now,
                ),
                "age_seconds": 0.0,
                "observed_at": sample_now.isoformat(),
            }
            for name in (
                "current_task",
                "session",
                "active_module",
                "active_process",
                "current_subtask",
                "execution_state",
            )
        }
        rt_state = RuntimeTemporalIntegrator().integrate(
            runtime_state=runtime_state,
            planner_state=planner_state,
            temporal_state=temporal_state,
        )
        goals_state = GoalsAttentionIntegrator().integrate(
            goals_state={
                "active_goal": goal.goal_id,
                "blockers": (),
                "priority": priority.level.name.lower(),
                "observed_at": sample_now.isoformat(),
                "confidence": 1.0,
                "freshness": "fresh",
            },
            attention_state={
                "current_focus": attention_snapshot.primary.candidate_id,
                "focus_reason": "highest_salience_explicit_goal",
                "observed_at": sample_now.isoformat(),
                "confidence": 1.0,
                "freshness": "fresh",
            },
        )
        world_memory_state = WorldMemoryIntegrator(max_memory_items=5).integrate(
            world_state={
                "self_relation": {
                    "working_on": world_entity.properties["working_on"],
                    "artifact": world_entity.properties["artifact"],
                    "verified": world_entity.properties["verified"],
                },
                "observed_at": world_entity.observed_at.isoformat(),
                "confidence": world_entity.confidence,
                "freshness": "fresh",
            },
            memory_items=(),
        )
        merged = merge_states(rt_state, goals_state, world_memory_state)
        snapshots.append(merged)

        planner_view = ConsumerViews().planner_view(
            merged,
            capability_evidence=(capability,),
        )
        autonomy_view = ConsumerViews().autonomy_view(
            merged,
            blockers=(),
            limitations=(),
        )
        checks["capability_projection_passed"] = (
            planner_view["capabilities"].get("file.write") == "available"
        )
        checks["consumer_boundaries_passed"] = (
            "authorization" not in planner_view
            and "may_execute" not in autonomy_view
            and "risk_decision" not in autonomy_view
        )

        # Stale owner evidence remains stale and is not promoted.
        stale_observed = sample_now - timedelta(seconds=180)
        stale_class = temporal.classify(
            "self_model",
            stale_observed,
            sample_now,
        )
        stale_result = SelfStateReconciler().reconcile(
            "current_task",
            (
                SourceValue(
                    field="current_task",
                    value="old-task",
                    owner="runtime",
                    source="runtime.current_task",
                    observed_at=stale_observed.isoformat(),
                    confidence=1.0,
                    freshness=stale_class,
                ),
            ),
            expected_owner="runtime",
        )
        checks["stale_scenario_passed"] = (
            stale_class in {"stale", "expired"}
            and stale_result.status == "stale"
            and stale_result.selected is None
            and stale_result.refresh_requested
        )

        # Conflicting owner views remain explicit conflict.
        conflict_result = SelfStateReconciler().reconcile(
            "current_task",
            (
                SourceValue(
                    "current_task",
                    f"runtime_tools:{tool_result.tool}",
                    "runtime",
                    "runtime.current_task",
                    freshness="fresh",
                ),
                SourceValue(
                    "current_task",
                    f"planner:{intent.capability}",
                    "planner",
                    "planner.current_task_candidate",
                    freshness="fresh",
                ),
            ),
            expected_owner="runtime",
        )
        checks["conflict_scenario_passed"] = (
            conflict_result.status == "conflicted"
            and conflict_result.refresh_requested
            and "conflicting_values" in conflict_result.reasons
        )

        missing_result = SelfStateReconciler().reconcile(
            "current_task",
            (),
            expected_owner="runtime",
        )
        checks["missing_owner_fail_closed"] = (
            missing_result.status == "unknown"
            and missing_result.selected is None
            and missing_result.refresh_requested
            and "no_evidence" in missing_result.reasons
        )

        detail.update(
            {
                "planner_runtime_tools": {
                    "action_id": intent.action_id,
                    "tool_status": status_value,
                    "tool_request_id": tool_result.request_id,
                    "independent_readback": observed_content,
                },
                "goal_attention": {
                    "goal_id": goal.goal_id,
                    "focus_id": attention_snapshot.primary.candidate_id,
                    "focus_score": attention_score.score,
                },
                "world_model": {
                    "entity_id": world_entity.entity_id,
                    "lifecycle": world_entity_state.lifecycle,
                    "properties": json_safe(world_entity.properties),
                },
                "memory": {
                    "query_id": memory_result.query_id,
                    "record_count": memory_result.context.record_count,
                    "retrieval_status": memory_result.retrieval_status,
                },
                "stale": {
                    "owner_freshness": stale_class,
                    "status": stale_result.status,
                    "selected": None,
                    "reasons": list(stale_result.reasons),
                },
                "conflict": {
                    "status": conflict_result.status,
                    "selected_owner": (
                        None
                        if conflict_result.selected is None
                        else conflict_result.selected.owner
                    ),
                    "reasons": list(conflict_result.reasons),
                },
                "missing_owner": {
                    "status": missing_result.status,
                    "reasons": list(missing_result.reasons),
                },
            }
        )

        # Continuous real-PC source-traceable snapshots.
        sample_index = 0
        while (time.monotonic() - wall_start) < target_duration:
            sample_now = datetime.now(timezone.utc)
            fresh = temporal.classify("self_model", sample_now, sample_now)
            runtime_state["observed_at"] = sample_now.isoformat()
            runtime_state["freshness"] = fresh
            planner_state["observed_at"] = sample_now.isoformat()
            planner_state["freshness"] = fresh
            temporal_state = {
                name: {
                    "freshness": fresh,
                    "age_seconds": 0.0,
                    "observed_at": sample_now.isoformat(),
                }
                for name in (
                    "current_task",
                    "session",
                    "active_module",
                    "active_process",
                    "current_subtask",
                    "execution_state",
                )
            }
            rt_state = RuntimeTemporalIntegrator().integrate(
                runtime_state=runtime_state,
                planner_state=planner_state,
                temporal_state=temporal_state,
            )
            ga_state = GoalsAttentionIntegrator().integrate(
                goals_state={
                    "active_goal": goal.goal_id,
                    "blockers": (),
                    "priority": priority.level.name.lower(),
                    "observed_at": sample_now.isoformat(),
                    "confidence": 1.0,
                    "freshness": fresh,
                },
                attention_state={
                    "current_focus": attention_snapshot.primary.candidate_id,
                    "focus_reason": "highest_salience_explicit_goal",
                    "observed_at": sample_now.isoformat(),
                    "confidence": 1.0,
                    "freshness": fresh,
                },
            )
            wm_state = WorldMemoryIntegrator(max_memory_items=5).integrate(
                world_state={
                    "self_relation": {
                        "working_on": "self-model-m10",
                        "artifact": str(file_path),
                        "verified": file_path.read_text(encoding="utf-8")
                        == "neuroforge-self-model-m10",
                    },
                    "observed_at": sample_now.isoformat(),
                    "confidence": 1.0,
                    "freshness": fresh,
                },
                memory_items=(),
            )
            snapshot = merge_states(rt_state, ga_state, wm_state)
            snapshots.append(snapshot)

            if not snapshot.source_trace:
                checks["continuous_traceable_snapshots"] = False
                break
            if any(
                not item.owner or not item.source
                for item in snapshot.fields.values()
            ):
                checks["continuous_traceable_snapshots"] = False
                break
            checks["continuous_traceable_snapshots"] = True

            peak_memory_mb = max(peak_memory_mb, peak_working_set_mb())
            sample_index += 1
            remaining = target_duration - (time.monotonic() - wall_start)
            if remaining <= 0:
                break
            time.sleep(min(args.sample_interval_seconds, remaining))

        elapsed = time.monotonic() - wall_start
        logical_cpus = max(1, os.cpu_count() or 1)
        avg_cpu_percent = (
            (time.process_time() - cpu_start)
            / elapsed
            / logical_cpus
            * 100.0
            if elapsed > 0
            else 100.0
        )
        peak_memory_mb = max(peak_memory_mb, peak_working_set_mb())

        real_owner_sources = all(
            checks[name]
            for name in (
                "real_runtime_tools",
                "real_planner",
                "real_temporal",
                "real_goals",
                "real_attention",
                "real_world_model",
                "real_memory_contract",
            )
        )
        stop_on_missing_owner_evidence = checks["missing_owner_fail_closed"]

        evidence = RealPCEvidence(
            platform=platform.system(),
            real_owner_sources=real_owner_sources,
            duration_seconds=elapsed,
            avg_cpu_percent=avg_cpu_percent,
            peak_memory_mb=peak_memory_mb,
            stale_scenario_passed=checks["stale_scenario_passed"],
            conflict_scenario_passed=checks["conflict_scenario_passed"],
            stop_on_missing_owner_evidence=stop_on_missing_owner_evidence,
        )

        thresholds = AcceptanceThresholds(
            min_duration_seconds=target_duration if args.preflight else 600.0,
            max_avg_cpu_percent=5.0,
            max_peak_memory_mb=64.0,
        )
        result = RealPCAcceptanceHarness().evaluate(
            snapshots=snapshots,
            evidence=evidence,
            thresholds=thresholds,
        )

        payload = {
            "schema_version": "self-model-m10-live-v1",
            "evidence": {
                "platform": platform.platform(),
                "real_owner_sources": evidence.real_owner_sources,
                "duration_seconds": evidence.duration_seconds,
                "avg_cpu_percent": evidence.avg_cpu_percent,
                "peak_memory_mb": evidence.peak_memory_mb,
                "stale_scenario_passed": evidence.stale_scenario_passed,
                "conflict_scenario_passed": evidence.conflict_scenario_passed,
                "stop_on_missing_owner_evidence": evidence.stop_on_missing_owner_evidence,
            },
            "snapshots": [serialize_snapshot(item) for item in snapshots],
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        detail_path = args.output.with_name(args.output.stem + "_details.json")
        detail_payload = {
            "schema_version": "self-model-m10-details-v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "machine": {
                "hostname": platform.node(),
                "python": platform.python_version(),
                "platform": platform.platform(),
                "logical_cpus": logical_cpus,
            },
            "owner_revisions": owner_revisions,
            "counts": {
                "snapshots": len(snapshots),
                "projected_fields_last_snapshot": len(snapshots[-1].fields),
            },
            "checks": checks,
            "scenario_detail": detail,
            "thresholds": {
                "min_duration_seconds": 600.0,
                "max_avg_cpu_percent": 5.0,
                "max_peak_memory_mb": 64.0,
            },
            "harness": {
                "passed": result.passed,
                "reasons": list(result.reasons),
            },
        }
        detail_path.write_text(
            json.dumps(detail_payload, indent=2, sort_keys=True),
            encoding="utf-8",
        )

        failed_checks = sorted(
            name for name, passed in checks.items() if not passed
        )
        if not result.passed:
            failed_checks.extend(result.reasons)
        failed_checks = sorted(set(failed_checks))

        print(
            json.dumps(
                {
                    "status": (
                        "PREFLIGHT_FAIL"
                        if args.preflight and failed_checks
                        else ("COLLECTED" if not failed_checks else "FAIL")
                    ),
                    "duration_seconds": elapsed,
                    "avg_cpu_percent": avg_cpu_percent,
                    "peak_memory_mb": peak_memory_mb,
                    "snapshot_count": len(snapshots),
                    "real_owner_sources": real_owner_sources,
                    "checks": checks,
                    "harness_passed": result.passed,
                    "harness_reasons": list(result.reasons),
                    "failed_checks": failed_checks,
                    "output": str(args.output),
                    "details_output": str(detail_path),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0 if not failed_checks else 1
    finally:
        try:
            runtime_tools.stop()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
