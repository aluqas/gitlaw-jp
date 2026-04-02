from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET


def _to_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


class XmlComparisonTableRenderer:
    """Renders aggregated comparison rows as XML."""

    def write(
        self,
        out_file: Path,
        comparison_rows: list[dict[str, object]],
        *,
        run_id: str,
        mode: str,
    ) -> None:
        root = ET.Element("comparisonTable")
        root.set("run_id", run_id)
        root.set("mode", mode)
        root.set("record_count", str(len(comparison_rows)))

        for idx, row in enumerate(comparison_rows, start=1):
            rec = ET.SubElement(root, "record")
            rec.set("index", str(idx))
            rec.set("law_id", _to_text(row.get("law_id", "")))
            rec.set("from_version_id", _to_text(row.get("from_version_id", "")))
            rec.set("to_version_id", _to_text(row.get("to_version_id", "")))

            law_name = ET.SubElement(rec, "lawName")
            law_name.text = _to_text(row.get("law_name", ""))

            amendment = ET.SubElement(rec, "amendment")
            amendment.set("law_name", _to_text(row.get("amendment_law_name", "")))
            amendment.set("law_num", _to_text(row.get("amendment_law_num", "")))
            amendment.set(
                "promulgation_date",
                _to_text(row.get("amendment_promulgation_date", "")),
            )

            effective_date = ET.SubElement(rec, "effectiveDate")
            effective_date.text = _to_text(row.get("effective_date", ""))

            changed_fields = ET.SubElement(rec, "changedFields")
            for field in row.get("changed_fields", []):
                field_el = ET.SubElement(changed_fields, "field")
                field_el.text = _to_text(field)

            changes_el = ET.SubElement(rec, "changes")
            for change in row.get("changes", []):
                ch = ET.SubElement(changes_el, "change")
                ch.set("field", _to_text(change.get("field", "")))
                ch.set("changed", _to_text(change.get("changed", "")))
                if "from" in change:
                    from_el = ET.SubElement(ch, "from")
                    from_el.text = _to_text(change.get("from"))
                if "to" in change:
                    to_el = ET.SubElement(ch, "to")
                    to_el.text = _to_text(change.get("to"))

        tree = ET.ElementTree(root)
        tree.write(out_file, encoding="utf-8", xml_declaration=True)


class MarkdownComparisonTableRenderer:
    """Renders aggregated comparison rows as Markdown."""

    def write(
        self,
        out_file: Path,
        comparison_rows: list[dict[str, object]],
        *,
        run_id: str,
        mode: str,
    ) -> None:
        del run_id

        lines: list[str] = [
            "# 新旧対照表",
            "",
            f"- mode: {mode}",
            f"- records: {len(comparison_rows)}",
            "",
        ]

        for idx, row in enumerate(comparison_rows, start=1):
            lines.append(f"## {idx}. {row.get('law_name') or row.get('law_id')}")
            lines.append("")
            lines.append(f"- law_id: {row.get('law_id', '')}")
            lines.append(f"- from_version_id: {row.get('from_version_id', '')}")
            lines.append(f"- to_version_id: {row.get('to_version_id', '')}")
            lines.append(f"- amendment_law_num: {row.get('amendment_law_num', '')}")
            lines.append(
                f"- amendment_promulgation_date: {row.get('amendment_promulgation_date', '')}"
            )
            lines.append("")
            lines.append("| field | from | to | changed |")
            lines.append("| --- | --- | --- | --- |")
            for change in row.get("changes", []):
                lines.append(
                    "| "
                    + f"{_to_text(change.get('field', ''))}"
                    + " | "
                    + f"{_to_text(change.get('from', ''))}"
                    + " | "
                    + f"{_to_text(change.get('to', ''))}"
                    + " | "
                    + f"{_to_text(change.get('changed', ''))}"
                    + " |"
                )
            lines.append("")

        out_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
