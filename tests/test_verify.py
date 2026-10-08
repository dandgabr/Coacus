"""Tests for the evidence primitives: completion ledger and unknown registry."""

from __future__ import annotations

import unittest

from engine.verify import ledger, unknowns


class TestLedger(unittest.TestCase):
    def test_all_pass_is_complete(self) -> None:
        built = ledger.build(
            [
                {"claim_id": "c1", "status": "pass", "evidence_ids": ["ev_1"]},
                {"claim_id": "c2", "status": "pass", "evidence_ids": ["ev_2"]},
            ]
        )
        self.assertEqual(built["overall"], "pass")
        self.assertTrue(built["summary"]["complete"])
        self.assertEqual(ledger.validate(built), [])

    def test_fail_dominates(self) -> None:
        built = ledger.build(
            [
                {"claim_id": "c1", "status": "pass", "evidence_ids": ["ev_1"]},
                {"claim_id": "c2", "status": "fail", "evidence_ids": ["ev_2"]},
            ]
        )
        self.assertEqual(built["overall"], "fail")
        self.assertFalse(built["summary"]["complete"])

    def test_non_pass_states_never_aggregate_to_pass(self) -> None:
        for status in ("unknown", "unsupported", "truncated", "skipped"):
            built = ledger.build([{"claim_id": "c", "status": status, "evidence_ids": []}])
            self.assertEqual(built["overall"], "unknown", status)
            self.assertFalse(built["summary"]["complete"], status)

    def test_pass_without_evidence_is_an_error(self) -> None:
        built = ledger.build([{"claim_id": "c", "status": "pass", "evidence_ids": []}])
        self.assertTrue(any("must cite" in e for e in ledger.validate(built)))

    def test_tampered_id_is_an_error(self) -> None:
        built = ledger.build([{"claim_id": "c", "status": "pass", "evidence_ids": ["ev_1"]}])
        built["ledger_id"] = "ecl_deadbeef"
        self.assertTrue(any("ledger_id" in e for e in ledger.validate(built)))

    def test_rounded_up_overall_is_an_error(self) -> None:
        built = ledger.build([{"claim_id": "c", "status": "fail", "evidence_ids": ["ev_1"]}])
        built["overall"] = "pass"
        self.assertTrue(any("fail-closed" in e for e in ledger.validate(built)))


class TestUnknowns(unittest.TestCase):
    def test_new_entry_is_valid(self) -> None:
        entry = unknowns.build("Why does the cache miss?", severity="high")
        self.assertEqual(entry["status"], "open")
        self.assertEqual(entry["revision"], 1)
        self.assertEqual(unknowns.validate(entry), [])

    def test_update_is_optimistic(self) -> None:
        entry = unknowns.build("q")
        revised = unknowns.update(entry, expected_revision=1)
        self.assertEqual(revised["revision"], 2)
        self.assertEqual(revised["previous_revision_digest"], entry["revision_digest"])
        with self.assertRaises(ValueError):
            unknowns.update(entry, expected_revision=5)

    def test_overlapping_evidence_is_an_error(self) -> None:
        entry = unknowns.build("q")
        entry["supporting_evidence_ids"] = ["ev_1"]
        entry["contradicting_evidence_ids"] = ["ev_1"]
        entry["revision_digest"] = unknowns._revision_digest(entry)
        self.assertTrue(any("both sides" in e for e in unknowns.validate(entry)))

    def test_contradicted_requires_contradicting_evidence(self) -> None:
        entry = unknowns.build("q")
        entry["status"] = "contradicted"
        entry["revision_digest"] = unknowns._revision_digest(entry)
        self.assertTrue(any("contradicting evidence" in e for e in unknowns.validate(entry)))

    def test_verified_resolution_requires_evidence(self) -> None:
        entry = unknowns.build("q")
        entry["status"] = "resolved"
        entry["resolution"] = {"disposition": "verified", "evidence_ids": []}
        entry["revision_digest"] = unknowns._revision_digest(entry)
        self.assertTrue(any("verified resolution" in e for e in unknowns.validate(entry)))

    def test_tampered_entry_is_an_error(self) -> None:
        entry = unknowns.build("q")
        entry["severity"] = "critical"
        self.assertTrue(any("revision_digest" in e for e in unknowns.validate(entry)))


if __name__ == "__main__":
    unittest.main()
