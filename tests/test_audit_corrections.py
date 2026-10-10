import csv, hashlib, json, math, tempfile, unittest
from pathlib import Path
from src.prospective import categorical_score

class AuditCorrectionsTests(unittest.TestCase):
    def test_baseline_definitions_and_scores(self):
        path=Path("baselines/public_report.json")
        self.assertTrue(path.exists(), "separate baseline artifact is required")
        data=json.loads(path.read_text())
        self.assertEqual(data["counts"], [2,2,0,0])
        source=Path(data["historical_source"])
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),data["historical_source_sha256"])
        rows=list(csv.DictReader(source.read_text().splitlines()))
        self.assertTrue(all(r["result"]=="success" for r in rows))
        self.assertEqual(sum(int(r["reported_anomalies"])>0 for r in rows),2)
        from build_baseline_scores import build
        table=build()["scores"]
        self.assertEqual(table["historical_add_one"][0]["brier_multiclass_sum"],9/16)
        self.assertEqual(table["historical_add_one"][2]["brier_multiclass_sum"],17/16)
        for name, probs in data["probabilities"].items():
            self.assertEqual(len(probs),4)
            self.assertAlmostEqual(sum(probs),1)
        self.assertEqual(data["probabilities"]["historical_add_one"],[(n+1)/8 for n in data["counts"]])
        for i in range(4):
            score=categorical_score(data["probabilities"]["uniform"],i)
            self.assertAlmostEqual(score["brier_multiclass_sum"],.75)
            self.assertAlmostEqual(score["negative_log_likelihood_nats"],math.log(4))
        score=categorical_score(data["probabilities"]["historical_raw"],2)
        self.assertIsNone(score["negative_log_likelihood_nats"])
        self.assertTrue(score["zero_probability_observed"])

    def test_manifest_tampering_missing_and_inventory(self):
        self.assertTrue(Path("scripts/package_manifest.py").exists(), "manifest checker is required")
        from scripts.package_manifest import generate, verify
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/"a.txt").write_text("original")
            generate(root,["a.txt"]); verify(root,["a.txt"])
            with self.assertRaises(ValueError): verify(root,["a.txt","new.txt"])
            (root/"a.txt").write_text("modified")
            with self.assertRaises(ValueError): verify(root,["a.txt"])
            generate(root,["a.txt"])
            manifest=root/"SHA256SUMS";manifest.write_text(manifest.read_text()*2)
            with self.assertRaises(ValueError): verify(root,["a.txt"])
            generate(root,["a.txt"]);(root/"a.txt").unlink()
            with self.assertRaises(ValueError): verify(root,["a.txt"])
