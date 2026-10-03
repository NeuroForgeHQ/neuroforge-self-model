from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import platform
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from self_model import (
    IntegratedSelfState,
    RealPCAcceptanceHarness,
    RealPCEvidence,
    SourceValue,
)
from self_model.acceptance import AcceptanceThresholds


DEFAULT_THRESHOLDS = AcceptanceThresholds(
    min_duration_seconds=600.0,
    max_avg_cpu_percent=5.0,
    max_peak_memory_mb=64.0,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence_json", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("self_model_m10_result.json"),
    )
    args = parser.parse_args()

    if platform.system().casefold() != "windows":
        raise SystemExit("Self Model M10 acceptance must run on Windows")

    payload = json.loads(args.evidence_json.read_text(encoding="utf-8"))
    raw_evidence = dict(payload["evidence"])
    raw_evidence["platform"] = platform.system()
    evidence = RealPCEvidence(**raw_evidence)

    snapshots = []
    for raw in payload["snapshots"]:
        fields = {
            name: SourceValue(**item)
            for name, item in raw["fields"].items()
        }
        snapshots.append(
            IntegratedSelfState(
                fields=fields,
                context=raw.get("context", {}),
                source_trace=tuple(raw.get("source_trace", ())),
            )
        )

    result = RealPCAcceptanceHarness().evaluate(
        snapshots=snapshots,
        evidence=evidence,
        thresholds=DEFAULT_THRESHOLDS,
    )
    rendered = {
        "passed": result.passed,
        "reasons": list(result.reasons),
        "thresholds": asdict(DEFAULT_THRESHOLDS),
        "evidence": asdict(evidence),
        "snapshot_count": len(snapshots),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(rendered, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(rendered, indent=2, sort_keys=True))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
