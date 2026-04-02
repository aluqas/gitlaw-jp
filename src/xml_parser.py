from __future__ import annotations

import re
from dataclasses import fields, is_dataclass
from enum import Enum

from xsdata.formats.dataclass.parsers import XmlParser

from .contracts import ParsedLawXml, XmlLawMeta, XmlStructureItem, XmlSupplProvision
from .generated.xsd.xmlschema_for_japanese_law_v3 import Law

WS_RE = re.compile(r"\s+")


def _to_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, Enum):
        return str(value.value)
    return str(value)


def _normalize_text(value: str) -> str:
    return WS_RE.sub(" ", value).strip()


def _flatten_mixed_content(content: list[object]) -> str:
    parts: list[str] = []
    for item in content:
        if isinstance(item, str):
            parts.append(item)
            continue
        if hasattr(item, "content"):
            nested = item.content
            if isinstance(nested, list):
                parts.append(_flatten_mixed_content(nested))
                continue
        if hasattr(item, "value"):
            parts.append(_to_text(item.value))
            continue
        parts.append(_to_text(item))
    return "".join(parts)


def _iter_dataclass_nodes(root: object) -> list[object]:
    if not is_dataclass(root):
        return []

    nodes: list[object] = []
    stack: list[object] = [root]
    while stack:
        current = stack.pop()
        if not is_dataclass(current):
            continue
        nodes.append(current)
        for fd in fields(current):
            value = getattr(current, fd.name)
            if is_dataclass(value):
                stack.append(value)
                continue
            if isinstance(value, list):
                for item in value:
                    if is_dataclass(item):
                        stack.append(item)
    return nodes


def _paragraph_num_text(paragraph: object) -> str:
    paragraph_num = getattr(paragraph, "paragraph_num", None)
    if paragraph_num is None:
        return ""
    content = getattr(paragraph_num, "content", None)
    if not isinstance(content, list):
        return ""
    return _normalize_text(_flatten_mixed_content(content))


def _sentence_text(sentence: object) -> str:
    content = getattr(sentence, "content", None)
    if not isinstance(content, list):
        return ""
    return _normalize_text(_flatten_mixed_content(content))


def _collect_paragraph_sentences(
    paragraph: object, *, article_num: str
) -> list[XmlStructureItem]:
    paragraph_sentence = getattr(paragraph, "paragraph_sentence", None)
    if paragraph_sentence is None:
        return []

    sentence_list = getattr(paragraph_sentence, "sentence", None)
    if not isinstance(sentence_list, list):
        return []

    paragraph_num = _paragraph_num_text(paragraph)
    rows: list[XmlStructureItem] = []
    for sentence in sentence_list:
        text = _sentence_text(sentence)
        if not text:
            continue
        rows.append(
            XmlStructureItem(
                article_num=article_num,
                paragraph_num=paragraph_num,
                sentence_text=text,
            )
        )
    return rows


def _walk_article_container(node: object) -> list[XmlStructureItem]:
    rows: list[XmlStructureItem] = []

    articles = getattr(node, "article", None)
    if isinstance(articles, list):
        for article in articles:
            article_num = _to_text(getattr(article, "num", ""))
            paragraphs = getattr(article, "paragraph", None)
            if isinstance(paragraphs, list):
                for paragraph in paragraphs:
                    rows.extend(
                        _collect_paragraph_sentences(paragraph, article_num=article_num)
                    )

    paragraphs = getattr(node, "paragraph", None)
    if isinstance(paragraphs, list):
        for paragraph in paragraphs:
            rows.extend(_collect_paragraph_sentences(paragraph, article_num=""))

    for child_name in ("part", "chapter", "section", "subsection", "division"):
        child_nodes = getattr(node, child_name, None)
        if not isinstance(child_nodes, list):
            continue
        for child in child_nodes:
            rows.extend(_walk_article_container(child))

    return rows


def _collect_structure(law: Law) -> list[XmlStructureItem]:
    rows: list[XmlStructureItem] = []
    law_body = law.law_body
    rows.extend(_walk_article_container(law_body.main_provision))
    for suppl in law_body.suppl_provision:
        rows.extend(_walk_article_container(suppl))
    return rows


def _has_flag(law: Law, attr_name: str) -> bool:
    for node in _iter_dataclass_nodes(law):
        if hasattr(node, attr_name) and bool(getattr(node, attr_name)):
            return True
    return False


def _collect_suppl_provisions(law: Law) -> list[XmlSupplProvision]:
    provisions: list[XmlSupplProvision] = []
    for element in law.law_body.suppl_provision:
        provisions.append(
            XmlSupplProvision(
                suppl_type=_to_text(getattr(element, "type_value", None)),
                amend_law_num=_normalize_text(
                    _to_text(getattr(element, "amend_law_num", None))
                ),
            )
        )
    return provisions


class XsdataLawXmlParser:
    """Parses e-Gov law XML with xsdata generated dataclasses."""

    def __init__(self) -> None:
        self._parser = XmlParser()

    def parse(self, *, law_id: str, version_id: str, xml_bytes: bytes) -> ParsedLawXml:
        del law_id
        del version_id

        law = self._parser.from_bytes(xml_bytes, Law)
        law_num = _normalize_text(_to_text(law.law_num.value))

        law_meta = XmlLawMeta(
            law_num=law_num,
            era=_to_text(law.era),
            year=_to_text(law.year),
            num=_to_text(law.num),
            law_type=_to_text(law.law_type),
            lang=_to_text(law.lang),
        )

        return ParsedLawXml(
            law_meta=law_meta,
            structure=_collect_structure(law),
            has_delete=_has_flag(law, "delete"),
            has_hide=_has_flag(law, "hide"),
            has_extract=_has_flag(law, "extract"),
            suppl_provisions=_collect_suppl_provisions(law),
        )
