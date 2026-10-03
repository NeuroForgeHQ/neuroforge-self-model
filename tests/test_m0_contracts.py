import unittest

from self_model import IntegratedSelfState, SourceValue


class TestM0SelfStateContracts(unittest.TestCase):
    def test_source_value_rejects_blank_provenance(self):
        with self.assertRaises(ValueError):
            SourceValue(
                field="current_task",
                value="acceptance",
                owner="runtime",
                source="",
            )

    def test_source_value_rejects_invalid_confidence(self):
        with self.assertRaises(ValueError):
            SourceValue(
                field="current_task",
                value="acceptance",
                owner="runtime",
                source="runtime.current_task",
                confidence=1.1,
            )

    def test_source_value_rejects_invalid_freshness(self):
        with self.assertRaises(ValueError):
            SourceValue(
                field="current_task",
                value="acceptance",
                owner="runtime",
                source="runtime.current_task",
                freshness="magic",
            )

    def test_snapshot_rejects_key_field_mismatch(self):
        with self.assertRaises(ValueError):
            IntegratedSelfState(
                fields={
                    "current_task": SourceValue(
                        field="current_focus",
                        value="acceptance",
                        owner="attention",
                        source="attention.current_focus",
                    )
                },
                source_trace=("attention.current_focus",),
            )

    def test_snapshot_rejects_non_source_value_fields(self):
        with self.assertRaises(TypeError):
            IntegratedSelfState(
                fields={"current_task": "acceptance"},
                source_trace=("runtime.current_task",),
            )

    def test_snapshot_is_read_only_and_traceable(self):
        state = IntegratedSelfState(
            fields={
                "current_task": SourceValue(
                    field="current_task",
                    value="self-model acceptance",
                    owner="runtime",
                    source="runtime.current_task",
                    freshness="fresh",
                )
            },
            context={"mode": "acceptance"},
            source_trace=(
                "runtime.current_task",
                "runtime.current_task",
            ),
        )
        self.assertEqual(state.owner_of("current_task"), "runtime")
        self.assertEqual(state.snapshot()["current_task"].source, "runtime.current_task")
        self.assertEqual(state.source_trace, ("runtime.current_task",))
        with self.assertRaises(TypeError):
            state.snapshot()["current_task"] = state.snapshot()["current_task"]
        with self.assertRaises(TypeError):
            state.context["mode"] = "mutated"


if __name__ == "__main__":
    unittest.main()
