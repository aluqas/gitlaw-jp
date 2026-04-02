from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from src.config import RunConfig
from src.contracts import IngestManifest
from src.stages.snapshot import create_snapshot_records


class SnapshotTests(unittest.TestCase):
    def _build_input_zip(self, zip_path: Path) -> None:
        csv_entry = "all_xml/all_law_list.csv"
        law_id = "123AC0000000001"
        version_id = "20240101_001"
        xml_entry = f"all_xml/{law_id}_{version_id}/{law_id}_{version_id}.xml"

        csv_content = "\n".join(
            [
                "法令種別,法令番号,法令名,公布日,改正法令名,改正法令番号,改正法令公布日,施行日,施行日備考,法令ID,本文URL,未施行",
                (
                    "Act,法律第1号,テスト法,2024-01-01,改正テスト法,法律第2号,2024-02-01,2024-03-01,,"
                    f"{law_id},https://laws.e-gov.go.jp/law/{version_id},"
                ),
            ]
        )

        xml_content = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<Law Era=\"Reiwa\" Year=\"6\" Num=\"1\" LawType=\"Act\" Lang=\"ja\">
  <LawNum>令和六年法律第一号</LawNum>
  <LawBody>
    <MainProvision Extract=\"true\">
      <Article Num=\"1\">
        <Paragraph Num=\"1\">
          <ParagraphNum>1</ParagraphNum>
          <ParagraphSentence>
            <Sentence>私権は<Ruby>しけん</Ruby>、公共の福祉に適合しなければならない。</Sentence>
          </ParagraphSentence>
        </Paragraph>
      </Article>
    </MainProvision>
    <SupplProvision Type=\"Amend\" AmendLawNum=\"令和六年法律第二号\">
      <SupplProvisionLabel>附則</SupplProvisionLabel>
      <Paragraph Num=\"1\">
        <ParagraphNum>1</ParagraphNum>
        <ParagraphSentence>
          <Sentence>附則</Sentence>
        </ParagraphSentence>
      </Paragraph>
    </SupplProvision>
  </LawBody>
</Law>
"""

        with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
            zf.writestr(csv_entry, csv_content)
            zf.writestr(xml_entry, xml_content)

    def test_snapshot_records_include_xml_mvp(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            input_zip = tmp_path / "input.zip"
            output_root = tmp_path / "runs"
            self._build_input_zip(input_zip)

            config = RunConfig(
                input_zip=input_zip,
                output_root=output_root,
                snapshot_parse_xml=True,
            )
            manifest = IngestManifest(
                run_id="run-xml",
                input_zip=str(input_zip),
                input_sha256="dummy",
                csv_entry="all_xml/all_law_list.csv",
                xml_entry_count=1,
                xml_entries_sample=[
                    "all_xml/123AC0000000001_20240101_001/123AC0000000001_20240101_001.xml"
                ],
            )

            snapshot_manifest = create_snapshot_records(config, manifest)
            self.assertEqual(snapshot_manifest.record_count, 1)
            self.assertEqual(snapshot_manifest.xml_parsed_count, 1)
            self.assertEqual(snapshot_manifest.xml_parse_policy, "strict_fail_fast")

            out_jsonl = (
                output_root
                / "run-xml"
                / "stages"
                / "03_snapshot"
                / "law_versions.jsonl"
            )
            with out_jsonl.open("r", encoding="utf-8") as f:
                rows = [json.loads(line) for line in f if line.strip()]

            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual(row["law_id"], "123AC0000000001")
            self.assertIn("xml_entry", row)
            self.assertIn("xml_mvp", row)

            self.assertEqual(
                row["xml_mvp"]["law_meta"]["law_num"], "令和六年法律第一号"
            )
            self.assertEqual(row["xml_mvp"]["law_meta"]["law_type"], "Act")
            self.assertTrue(row["xml_mvp"]["flags"]["extract"])
            self.assertGreaterEqual(
                row["xml_mvp"]["structure_summary"]["sentence_count"], 1
            )
            self.assertEqual(
                row["xml_mvp"]["amend"]["suppl_provisions"][0]["suppl_type"], "Amend"
            )


if __name__ == "__main__":
    unittest.main()
