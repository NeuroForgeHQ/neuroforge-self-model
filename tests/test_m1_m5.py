import unittest

from self_model import (
    ActionOutcome,
    ActionOutcomeProjector,
    CapabilityEvidence,
    CapabilityProjector,
    KnowledgeClaim,
    KnowledgeProjector,
    OperationalStateProjector,
    SelfStateReconciler,
    SourceValue,
)


class TestM1OperationalProjection(unittest.TestCase):
    def test_owner_projection_without_lifecycle_mutation(self):
        projection = OperationalStateProjector().project(
            runtime_state={
                "current_task": "runtime acceptance",
                "session": "s-1",
                "active_module": "runtime",
                "active_process": "python",
                "observed_at": "2026-09-21T18:00:00+05:30",
                "freshness": "fresh",
            },
            planner_state={
                "current_subtask": "rerun tests",
                "execution_state": "ready",
                "observed_at": "2026-09-21T18:00:01+05:30",
                "freshness": "fresh",
            },
        )
        self.assertEqual(projection.snapshot()["current_task"], "runtime acceptance")
        self.assertEqual(projection.fields["current_task"].owner, "runtime")
        self.assertEqual(projection.fields["current_subtask"].owner, "planner")
        self.assertFalse(hasattr(OperationalStateProjector(), "start_task"))


class TestM2CapabilityProjection(unittest.TestCase):
    def test_capability_evidence_is_owner_sourced(self):
        p = CapabilityProjector().project(
            [
                CapabilityEvidence(
                    capability="run_local_tests",
                    state="available",
                    owner="runtime",
                    source="runtime.capabilities",
                    freshness="fresh",
                ),
                CapabilityEvidence(
                    capability="send_external_message",
                    state="permission_required",
                    owner="tools",
                    source="tools.policy",
                    freshness="fresh",
                ),
            ]
        )
        self.assertEqual(p.state_of("run_local_tests"), "available")
        self.assertEqual(p.state_of("unknown_capability"), "unknown")

    def test_rejects_unrecognized_capability_owner(self):
        with self.assertRaises(ValueError):
            CapabilityEvidence(
                capability="x",
                state="available",
                owner="self_model",
                source="self_model.fake",
            )


class TestM3KnowledgeProjection(unittest.TestCase):
    def test_self_relevant_claim(self):
        p = KnowledgeProjector().project(
            [
                KnowledgeClaim(
                    category="required_tool",
                    key="microphone",
                    state="unknown",
                    owner="runtime",
                    source="runtime.device_state",
                )
            ]
        )
        self.assertEqual(p.get("microphone").state, "unknown")

    def test_general_knowledge_is_rejected(self):
        with self.assertRaises(ValueError):
            KnowledgeClaim(
                category="world_history",
                key="capital_of_france",
                state="known",
                owner="knowledge",
                source="knowledge.fact",
                value="Paris",
            )


class TestM4ActionOutcomeProjection(unittest.TestCase):
    def test_unverified_success_is_not_success(self):
        outcome = ActionOutcome(
            action_id="a1",
            action="run acceptance",
            owner="runtime",
            source="runtime.events",
            result="success",
            verified=False,
        )
        self.assertEqual(outcome.projected_result, "unverified")

    def test_verified_result_requires_provenance(self):
        with self.assertRaises(ValueError):
            ActionOutcome(
                action_id="a1",
                action="run acceptance",
                owner="runtime",
                source="runtime.events",
                result="success",
                verified=True,
            )

    def test_history_is_bounded_projection(self):
        outcomes = [
            ActionOutcome(str(i), f"a{i}", "runtime", "runtime.events")
            for i in range(5)
        ]
        p = ActionOutcomeProjector(max_items=2).project(outcomes)
        self.assertEqual([x.action_id for x in p.recent], ["3", "4"])


class TestM5ConflictAndFreshness(unittest.TestCase):
    def test_conflict_is_not_silently_merged(self):
        r = SelfStateReconciler().reconcile(
            "current_task",
            [
                SourceValue(
                    "current_task",
                    "task-a",
                    "runtime",
                    "runtime.state",
                    freshness="fresh",
                ),
                SourceValue(
                    "current_task",
                    "task-b",
                    "planner",
                    "planner.state",
                    freshness="fresh",
                ),
            ],
            expected_owner="runtime",
        )
        self.assertEqual(r.status, "conflicted")
        self.assertTrue(r.refresh_requested)
        self.assertEqual(r.selected.owner, "runtime")

    def test_stale_is_consumed_not_recomputed(self):
        r = SelfStateReconciler().reconcile(
            "current_task",
            [
                SourceValue(
                    "current_task",
                    "task-a",
                    "runtime",
                    "runtime.state",
                    freshness="stale",
                )
            ],
        )
        self.assertEqual(r.status, "stale")
        self.assertTrue(r.refresh_requested)

    def test_consistent_fresh_evidence(self):
        r = SelfStateReconciler().reconcile(
            "current_focus",
            [
                SourceValue(
                    "current_focus",
                    "failure",
                    "attention",
                    "attention.state",
                    freshness="fresh",
                    confidence=0.9,
                ),
                SourceValue(
                    "current_focus",
                    "failure",
                    "runtime",
                    "runtime.view",
                    freshness="recent",
                    confidence=0.7,
                ),
            ],
        )
        self.assertEqual(r.status, "known")
        self.assertFalse(r.refresh_requested)
        self.assertEqual(r.selected.owner, "attention")


if __name__ == "__main__":
    unittest.main()
