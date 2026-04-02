from __future__ import annotations

import unittest

from src.xml_parser import XsdataLawXmlParser


class XmlParserTests(unittest.TestCase):
    def test_parser_extracts_mvp_fields_and_mixed_content(self) -> None:
        xml = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<Law Era=\"Reiwa\" Year=\"6\" Num=\"1\" LawType=\"Act\" Lang=\"ja\">
  <LawNum>令和六年法律第一号</LawNum>
  <LawBody>
    <MainProvision Extract=\"true\">
      <Article Num=\"1\" Delete=\"true\">
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
      <Paragraph Num=\"1\" Hide=\"true\">
        <ParagraphNum>1</ParagraphNum>
        <ParagraphSentence>
          <Sentence>削除される条文</Sentence>
        </ParagraphSentence>
      </Paragraph>
    </SupplProvision>
  </LawBody>
</Law>
"""

        parser = XsdataLawXmlParser()
        parsed = parser.parse(
            law_id="123AC0000000001",
            version_id="20240101_001",
            xml_bytes=xml.encode("utf-8"),
        )

        self.assertEqual(parsed.law_meta.law_num, "令和六年法律第一号")
        self.assertEqual(parsed.law_meta.law_type, "Act")
        self.assertEqual(parsed.law_meta.lang, "ja")

        self.assertGreaterEqual(len(parsed.structure), 2)
        self.assertEqual(parsed.structure[0].article_num, "1")
        self.assertEqual(parsed.structure[0].paragraph_num, "1")
        self.assertIn("私権はしけん、公共の福祉", parsed.structure[0].sentence_text)

        self.assertTrue(parsed.has_delete)
        self.assertTrue(parsed.has_hide)
        self.assertTrue(parsed.has_extract)

        self.assertEqual(len(parsed.suppl_provisions), 1)
        self.assertEqual(parsed.suppl_provisions[0].suppl_type, "Amend")
        self.assertEqual(parsed.suppl_provisions[0].amend_law_num, "令和六年法律第二号")


if __name__ == "__main__":
    unittest.main()
