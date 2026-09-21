import unittest

from self_model import (
    AcceptanceThresholds,
    CapabilityEvidence,
    ConsumerViews,
    GoalsAttentionIntegrator,
    RealPCAcceptanceHarness,
    RealPCEvidence,
    RuntimeTemporalIntegrator,
    WorldMemoryIntegrator,
    merge_states,
)


class TestM6RuntimeTemporalIntegration(unittest.TestCase):
    def test_runtime_and_temporal_owners_remain_separate(self):
        state = RuntimeTemporalIntegrator().integrate(
            runtime_state={
                "current_task": "acceptance",
                "session": "s1",
                "active_module": "runtime",
                "active_process": "python",
            },
            planner_state={
                "current_subtask": "rerun",
                "execution_state": "ready",
            },
            temporal_state={
                "current_task": {
                    "freshness": "fresh",
                    "age_seconds": 2,
                    "observed_at": "2026-09-21T18:00:00+05:30",
                }
            },
        )
        self.assertEqual(state.owner_of("current_task"), "runtime")
        self.assertEqual(state.fields["current_task"].freshness, "fresh")
        self.assertEqual(state.context["temporal"]["current_task"]["age_seconds"], 2)
        self.assertIn("temporal_awareness.current_task", state.source_trace)


class TestM7GoalsAttentionIntegration(unittest.TestCase):
    def test_goal_and_focus_ownership(self):
        state = GoalsAttentionIntegrator().integrate(
            goals_state={
                "active_goal": "deploy NeuroForge",
                "blockers": ["voice acceptance"],
                "priority": "high",
                "freshness": "recent",
            },
            attention_state={
                "current_focus": "self-model",
                "focus_reason": "active implementation",
                "freshness": "fresh",
            },
        )
        self.assertEqual(state.owner_of("active_goal"), "goals_drives")
        self.assertEqual(state.owner_of("current_focus"), "attention")
        self.assertEqual(state.fields["goal_blockers"].value, ["voice acceptance"])


class TestM8WorldMemoryIntegration(unittest.TestCase):
    def test_memory_context_is_bounded(self):
        integrator = WorldMemoryIntegrator(max_memory_items=2)
        state = integrator.integrate(
            world_state={
                "self_relation": {"working_on": "neuroforge-self-model"},
                "freshness": "fresh",
            },
            memory_items=[
                {"memory_id": "1", "summary": "old"},
                {"memory_id": "2", "summary": "middle"},
                {"memory_id": "3", "summary": "recent"},
            ],
        )
        self.assertEqual(state.owner_of("world_relation"), "world_model")
        self.assertEqual(state.context["memory_items_received"], 3)
        self.assertEqual(state.context["memory_items_projected"], 2)
        self.assertEqual(state.context["memory_context"][0]["memory_id"], "2")


class TestM9ConsumerIntegration(unittest.TestCase):
    def test_planner_view_is_projection_only(self):
        base = RuntimeTemporalIntegrator().integrate(
            runtime_state={"current_task": "x"},
            planner_state={},
        )
        view = ConsumerViews().planner_view(
            base,
            capability_evidence=[
                CapabilityEvidence(
                    capability="run_local_tests",
                    state="available",
                    owner="runtime",
                    source="runtime.capabilities",
                )
            ],
        )
        self.assertEqual(view["capabilities"]["run_local_tests"], "available")
        self.assertNotIn("authorization", view)
        with self.assertRaises(TypeError):
            view["authorization"] = True

    def test_autonomy_view_contains_no_action_decision(self):
        base = GoalsAttentionIntegrator().integrate(
            goals_state={"active_goal": "x"},
            attention_state={"current_focus": "y"},
        )
        view = ConsumerViews().autonomy_view(
            base,
            blockers=["missing evidence"],
            limitations=["read-only"],
        )
        self.assertNotIn("may_execute", view)
        self.assertNotIn("risk_decision", view)

    def test_state_merge_rejects_owner_conflict(self):
        a = GoalsAttentionIntegrator().integrate(
            goals_state={"active_goal": "a"},
        )
        b = GoalsAttentionIntegrator().integrate(
            goals_state={"active_goal": "b"},
        )
        with self.assertRaises(ValueError):
            merge_states(a, b)


class TestM10AcceptanceHarness(unittest.TestCase):
    def setUp(self):
        self.thresholds = AcceptanceThresholds(
            min_duration_seconds=300,
            max_avg_cpu_percent=5,
            max_peak_memory_mb=64,
        )
        self.snapshot = RuntimeTemporalIntegrator().integrate(
            runtime_state={"current_task": "real test"},
            temporal_state={"current_task": {"freshness": "fresh"}},
        )

    def test_fails_closed_without_real_windows_evidence(self):
        result = RealPCAcceptanceHarness().evaluate(
            snapshots=[self.snapshot],
            evidence=RealPCEvidence(
                platform="linux",
                real_owner_sources=False,
                duration_seconds=10,
                avg_cpu_percent=0.1,
                peak_memory_mb=1,
                stale_scenario_passed=True,
                conflict_scenario_passed=True,
                stop_on_missing_owner_evidence=True,
            ),
            thresholds=self.thresholds,
        )
        self.assertFalse(result.passed)
        self.assertIn("real_windows_required", result.reasons)
        self.assertIn("real_owner_sources_required", result.reasons)

    def test_accepts_complete_real_pc_evidence_contract(self):
        result = RealPCAcceptanceHarness().evaluate(
            snapshots=[self.snapshot],
            evidence=RealPCEvidence(
                platform="Windows",
                real_owner_sources=True,
                duration_seconds=600,
                avg_cpu_percent=1.2,
                peak_memory_mb=20,
                stale_scenario_passed=True,
                conflict_scenario_passed=True,
                stop_on_missing_owner_evidence=True,
            ),
            thresholds=self.thresholds,
        )
        self.assertTrue(result.passed)


if __name__ == "__main__":
    unittest.main()
