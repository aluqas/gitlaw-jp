from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class AppdxFigTitleWritingMode(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class AppdxFormatTitleWritingMode(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class AppdxNoteTitleWritingMode(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class AppdxStyleTitleWritingMode(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class AppdxTableTitleWritingMode(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class ColumnAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"


@dataclass(kw_only=True)
class Fig:
    src: object = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class LawNum:
    value: str = field(default="")


class LawEra(Enum):
    MEIJI = "Meiji"
    TAISHO = "Taisho"
    SHOWA = "Showa"
    HEISEI = "Heisei"
    REIWA = "Reiwa"


class LawLang(Enum):
    JA = "ja"
    EN = "en"


class LawLawType(Enum):
    CONSTITUTION = "Constitution"
    ACT = "Act"
    CABINET_ORDER = "CabinetOrder"
    IMPERIAL_ORDER = "ImperialOrder"
    MINISTERIAL_ORDINANCE = "MinisterialOrdinance"
    RULE = "Rule"
    MISC = "Misc"


class LineStyle(Enum):
    DOTTED = "dotted"
    DOUBLE = "double"
    NONE = "none"
    SOLID = "solid"


@dataclass(kw_only=True)
class Preamble:
    paragraph: list[Paragraph] = field(
        default_factory=list,
        metadata={
            "name": "Paragraph",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class Rt:
    value: str = field(default="")


class SentenceFunction(Enum):
    MAIN = "main"
    PROVISO = "proviso"


class SentenceIndent(Enum):
    PARAGRAPH = "Paragraph"
    ITEM = "Item"
    SUBITEM1 = "Subitem1"
    SUBITEM2 = "Subitem2"
    SUBITEM3 = "Subitem3"
    SUBITEM4 = "Subitem4"
    SUBITEM5 = "Subitem5"
    SUBITEM6 = "Subitem6"
    SUBITEM7 = "Subitem7"
    SUBITEM8 = "Subitem8"
    SUBITEM9 = "Subitem9"
    SUBITEM10 = "Subitem10"


class SentenceWritingMode(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


@dataclass(kw_only=True)
class Sub:
    value: str = field(default="")


@dataclass(kw_only=True)
class Sup:
    value: str = field(default="")


class SupplProvisionAppdxStyleTitleWritingMode(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class SupplProvisionAppdxTableTitleWritingMode(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class SupplProvisionType(Enum):
    NEW = "New"
    AMEND = "Amend"


class TableColumnAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"


class TableColumnBorderBottom(Enum):
    SOLID = "solid"
    NONE = "none"
    DOTTED = "dotted"
    DOUBLE = "double"


class TableColumnBorderLeft(Enum):
    SOLID = "solid"
    NONE = "none"
    DOTTED = "dotted"
    DOUBLE = "double"


class TableColumnBorderRight(Enum):
    SOLID = "solid"
    NONE = "none"
    DOTTED = "dotted"
    DOUBLE = "double"


class TableColumnBorderTop(Enum):
    SOLID = "solid"
    NONE = "none"
    DOTTED = "dotted"
    DOUBLE = "double"


class TableColumnValign(Enum):
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"


class TableStructTitleWritingMode(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class TableWritingMode(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


@dataclass(kw_only=True)
class AnyType:
    class Meta:
        name = "any"

    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass(kw_only=True)
class ArithFormula(AnyType):
    num: None | int = field(
        default=None,
        metadata={
            "name": "Num",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Format(AnyType):
    pass


@dataclass(kw_only=True)
class Note(AnyType):
    pass


@dataclass(kw_only=True)
class QuoteStruct(AnyType):
    pass


@dataclass(kw_only=True)
class Ruby:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Rt",
                    "type": Rt,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Style(AnyType):
    pass


@dataclass(kw_only=True)
class Line:
    style: LineStyle = field(
        default=LineStyle.SOLID,
        metadata={
            "name": "Style",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "QuoteStruct",
                    "type": QuoteStruct,
                },
                {
                    "name": "ArithFormula",
                    "type": ArithFormula,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class AppdxFigTitle:
    writing_mode: AppdxFigTitleWritingMode = field(
        default=AppdxFigTitleWritingMode.VERTICAL,
        metadata={
            "name": "WritingMode",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class AppdxFormatTitle:
    writing_mode: AppdxFormatTitleWritingMode = field(
        default=AppdxFormatTitleWritingMode.VERTICAL,
        metadata={
            "name": "WritingMode",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class AppdxNoteTitle:
    writing_mode: AppdxNoteTitleWritingMode = field(
        default=AppdxNoteTitleWritingMode.VERTICAL,
        metadata={
            "name": "WritingMode",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class AppdxStyleTitle:
    writing_mode: AppdxStyleTitleWritingMode = field(
        default=AppdxStyleTitleWritingMode.VERTICAL,
        metadata={
            "name": "WritingMode",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class AppdxTableTitle:
    writing_mode: AppdxTableTitleWritingMode = field(
        default=AppdxTableTitleWritingMode.VERTICAL,
        metadata={
            "name": "WritingMode",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class ArithFormulaNum:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class ArticleCaption:
    common_caption: None | bool = field(
        default=None,
        metadata={
            "name": "CommonCaption",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class ArticleRange:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class ArticleTitle:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class ChapterTitle:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class ClassTitle:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class DivisionTitle:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class EnactStatement:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class FigStructTitle:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class FormatStructTitle:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class ItemTitle:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class LawTitle:
    kana: None | object = field(
        default=None,
        metadata={
            "name": "Kana",
            "type": "Attribute",
        },
    )
    abbrev: None | object = field(
        default=None,
        metadata={
            "name": "Abbrev",
            "type": "Attribute",
        },
    )
    abbrev_kana: None | object = field(
        default=None,
        metadata={
            "name": "AbbrevKana",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class NoteStructTitle:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class ParagraphCaption:
    common_caption: None | bool = field(
        default=None,
        metadata={
            "name": "CommonCaption",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class ParagraphNum:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class PartTitle:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class RelatedArticleNum:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class RemarksLabel:
    line_break: bool = field(
        default=False,
        metadata={
            "name": "LineBreak",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class SectionTitle:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Sentence:
    num: None | int = field(
        default=None,
        metadata={
            "name": "Num",
            "type": "Attribute",
        },
    )
    function: None | SentenceFunction = field(
        default=None,
        metadata={
            "name": "Function",
            "type": "Attribute",
        },
    )
    indent: None | SentenceIndent = field(
        default=None,
        metadata={
            "name": "Indent",
            "type": "Attribute",
        },
    )
    writing_mode: SentenceWritingMode = field(
        default=SentenceWritingMode.VERTICAL,
        metadata={
            "name": "WritingMode",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "QuoteStruct",
                    "type": QuoteStruct,
                },
                {
                    "name": "ArithFormula",
                    "type": ArithFormula,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class StyleStructTitle:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Subitem10Title:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Subitem1Title:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Subitem2Title:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Subitem3Title:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Subitem4Title:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Subitem5Title:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Subitem6Title:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Subitem7Title:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Subitem8Title:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Subitem9Title:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class SubsectionTitle:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class SupplNote:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class SupplProvisionAppdxStyleTitle:
    writing_mode: SupplProvisionAppdxStyleTitleWritingMode = field(
        default=SupplProvisionAppdxStyleTitleWritingMode.VERTICAL,
        metadata={
            "name": "WritingMode",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class SupplProvisionAppdxTableTitle:
    writing_mode: SupplProvisionAppdxTableTitleWritingMode = field(
        default=SupplProvisionAppdxTableTitleWritingMode.VERTICAL,
        metadata={
            "name": "WritingMode",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class SupplProvisionLabel:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class TocappdxTableLabel:
    class Meta:
        name = "TOCAppdxTableLabel"

    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Toclabel:
    class Meta:
        name = "TOCLabel"

    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class TocpreambleLabel:
    class Meta:
        name = "TOCPreambleLabel"

    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class TableHeaderColumn:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class TableStructTitle:
    writing_mode: TableStructTitleWritingMode = field(
        default=TableStructTitleWritingMode.VERTICAL,
        metadata={
            "name": "WritingMode",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "Line",
                    "type": Line,
                },
                {
                    "name": "Ruby",
                    "type": Ruby,
                },
                {
                    "name": "Sup",
                    "type": Sup,
                },
                {
                    "name": "Sub",
                    "type": Sub,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class AmendProvisionSentence:
    sentence: Sentence = field(
        metadata={
            "name": "Sentence",
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class Article:
    article_caption: list[ArticleCaption] = field(
        default_factory=list,
        metadata={
            "name": "ArticleCaption",
            "type": "Element",
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    article_title: list[ArticleTitle] = field(
        default_factory=list,
        metadata={
            "name": "ArticleTitle",
            "type": "Element",
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    paragraph: list[Paragraph] = field(
        default_factory=list,
        metadata={
            "name": "Paragraph",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    suppl_note: None | SupplNote = field(
        default=None,
        metadata={
            "name": "SupplNote",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Chapter:
    chapter_title: ChapterTitle = field(
        metadata={
            "name": "ChapterTitle",
            "type": "Element",
        }
    )
    article: list[Article] = field(
        default_factory=list,
        metadata={
            "name": "Article",
            "type": "Element",
        },
    )
    section: list[Section] = field(
        default_factory=list,
        metadata={
            "name": "Section",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Column:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    num: None | int = field(
        default=None,
        metadata={
            "name": "Num",
            "type": "Attribute",
        },
    )
    line_break: bool = field(
        default=False,
        metadata={
            "name": "LineBreak",
            "type": "Attribute",
        },
    )
    align: None | ColumnAlign = field(
        default=None,
        metadata={
            "name": "Align",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Division:
    division_title: DivisionTitle = field(
        metadata={
            "name": "DivisionTitle",
            "type": "Element",
        }
    )
    article: list[Article] = field(
        default_factory=list,
        metadata={
            "name": "Article",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ParagraphSentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class Part:
    part_title: PartTitle = field(
        metadata={
            "name": "PartTitle",
            "type": "Element",
        }
    )
    article: list[Article] = field(
        default_factory=list,
        metadata={
            "name": "Article",
            "type": "Element",
        },
    )
    chapter: list[Chapter] = field(
        default_factory=list,
        metadata={
            "name": "Chapter",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Section:
    section_title: SectionTitle = field(
        metadata={
            "name": "SectionTitle",
            "type": "Element",
        }
    )
    article: list[Article] = field(
        default_factory=list,
        metadata={
            "name": "Article",
            "type": "Element",
        },
    )
    subsection: list[Subsection] = field(
        default_factory=list,
        metadata={
            "name": "Subsection",
            "type": "Element",
        },
    )
    division: list[Division] = field(
        default_factory=list,
        metadata={
            "name": "Division",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Subsection:
    subsection_title: SubsectionTitle = field(
        metadata={
            "name": "SubsectionTitle",
            "type": "Element",
        }
    )
    article: list[Article] = field(
        default_factory=list,
        metadata={
            "name": "Article",
            "type": "Element",
        },
    )
    division: list[Division] = field(
        default_factory=list,
        metadata={
            "name": "Division",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class SupplProvisionAppdx:
    arith_formula_num: None | ArithFormulaNum = field(
        default=None,
        metadata={
            "name": "ArithFormulaNum",
            "type": "Element",
        },
    )
    related_article_num: None | RelatedArticleNum = field(
        default=None,
        metadata={
            "name": "RelatedArticleNum",
            "type": "Element",
        },
    )
    arith_formula: list[ArithFormula] = field(
        default_factory=list,
        metadata={
            "name": "ArithFormula",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    num: None | int = field(
        default=None,
        metadata={
            "name": "Num",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Tocarticle:
    class Meta:
        name = "TOCArticle"

    article_title: ArticleTitle = field(
        metadata={
            "name": "ArticleTitle",
            "type": "Element",
        }
    )
    article_caption: ArticleCaption = field(
        metadata={
            "name": "ArticleCaption",
            "type": "Element",
        }
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Tocdivision:
    class Meta:
        name = "TOCDivision"

    division_title: DivisionTitle = field(
        metadata={
            "name": "DivisionTitle",
            "type": "Element",
        }
    )
    article_range: None | ArticleRange = field(
        default=None,
        metadata={
            "name": "ArticleRange",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class TableHeaderRow:
    table_header_column: list[TableHeaderColumn] = field(
        default_factory=list,
        metadata={
            "name": "TableHeaderColumn",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class AmendProvision:
    amend_provision_sentence: None | AmendProvisionSentence = field(
        default=None,
        metadata={
            "name": "AmendProvisionSentence",
            "type": "Element",
        },
    )
    new_provision: list[NewProvision] = field(
        default_factory=list,
        metadata={
            "name": "NewProvision",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class ListSentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Sublist1Sentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Sublist2Sentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Sublist3Sentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Tocsubsection:
    class Meta:
        name = "TOCSubsection"

    subsection_title: SubsectionTitle = field(
        metadata={
            "name": "SubsectionTitle",
            "type": "Element",
        }
    )
    article_range: None | ArticleRange = field(
        default=None,
        metadata={
            "name": "ArticleRange",
            "type": "Element",
        },
    )
    tocdivision: list[Tocdivision] = field(
        default_factory=list,
        metadata={
            "name": "TOCDivision",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Sublist3Sentence1:
    class Meta:
        name = "Sublist3Sentence"

    sublist3_sentence: Sublist3Sentence = field(
        metadata={
            "name": "Sublist3Sentence",
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class Tocsection:
    class Meta:
        name = "TOCSection"

    section_title: SectionTitle = field(
        metadata={
            "name": "SectionTitle",
            "type": "Element",
        }
    )
    article_range: None | ArticleRange = field(
        default=None,
        metadata={
            "name": "ArticleRange",
            "type": "Element",
        },
    )
    tocsubsection: list[Tocsubsection] = field(
        default_factory=list,
        metadata={
            "name": "TOCSubsection",
            "type": "Element",
        },
    )
    tocdivision: list[Tocdivision] = field(
        default_factory=list,
        metadata={
            "name": "TOCDivision",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Sublist3(Sublist3Sentence1):
    pass


@dataclass(kw_only=True)
class Tocchapter:
    class Meta:
        name = "TOCChapter"

    chapter_title: ChapterTitle = field(
        metadata={
            "name": "ChapterTitle",
            "type": "Element",
        }
    )
    article_range: None | ArticleRange = field(
        default=None,
        metadata={
            "name": "ArticleRange",
            "type": "Element",
        },
    )
    tocsection: list[Tocsection] = field(
        default_factory=list,
        metadata={
            "name": "TOCSection",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Sublist2:
    sublist2_sentence: Sublist2Sentence = field(
        metadata={
            "name": "Sublist2Sentence",
            "type": "Element",
        }
    )
    sublist3: list[Sublist3] = field(
        default_factory=list,
        metadata={
            "name": "Sublist3",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Tocpart:
    class Meta:
        name = "TOCPart"

    part_title: PartTitle = field(
        metadata={
            "name": "PartTitle",
            "type": "Element",
        }
    )
    article_range: None | ArticleRange = field(
        default=None,
        metadata={
            "name": "ArticleRange",
            "type": "Element",
        },
    )
    tocchapter: list[Tocchapter] = field(
        default_factory=list,
        metadata={
            "name": "TOCChapter",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class TocsupplProvision:
    class Meta:
        name = "TOCSupplProvision"

    suppl_provision_label: SupplProvisionLabel = field(
        metadata={
            "name": "SupplProvisionLabel",
            "type": "Element",
        }
    )
    article_range: None | ArticleRange = field(
        default=None,
        metadata={
            "name": "ArticleRange",
            "type": "Element",
        },
    )
    tocarticle: list[Tocarticle] = field(
        default_factory=list,
        metadata={
            "name": "TOCArticle",
            "type": "Element",
        },
    )
    tocchapter: list[Tocchapter] = field(
        default_factory=list,
        metadata={
            "name": "TOCChapter",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Sublist1:
    sublist1_sentence: Sublist1Sentence = field(
        metadata={
            "name": "Sublist1Sentence",
            "type": "Element",
        }
    )
    sublist2: list[Sublist2] = field(
        default_factory=list,
        metadata={
            "name": "Sublist2",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Toc:
    class Meta:
        name = "TOC"

    toclabel: None | Toclabel = field(
        default=None,
        metadata={
            "name": "TOCLabel",
            "type": "Element",
        },
    )
    tocpreamble_label: None | TocpreambleLabel = field(
        default=None,
        metadata={
            "name": "TOCPreambleLabel",
            "type": "Element",
        },
    )
    tocpart: list[Tocpart] = field(
        default_factory=list,
        metadata={
            "name": "TOCPart",
            "type": "Element",
        },
    )
    tocchapter: list[Tocchapter] = field(
        default_factory=list,
        metadata={
            "name": "TOCChapter",
            "type": "Element",
        },
    )
    tocsection: list[Tocsection] = field(
        default_factory=list,
        metadata={
            "name": "TOCSection",
            "type": "Element",
        },
    )
    tocarticle: list[Tocarticle] = field(
        default_factory=list,
        metadata={
            "name": "TOCArticle",
            "type": "Element",
        },
    )
    tocsuppl_provision: None | TocsupplProvision = field(
        default=None,
        metadata={
            "name": "TOCSupplProvision",
            "type": "Element",
        },
    )
    tocappdx_table_label: list[TocappdxTableLabel] = field(
        default_factory=list,
        metadata={
            "name": "TOCAppdxTableLabel",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class LawBody:
    law_title: list[LawTitle] = field(
        default_factory=list,
        metadata={
            "name": "LawTitle",
            "type": "Element",
            "max_occurs": 2,
        },
    )
    enact_statement: list[EnactStatement] = field(
        default_factory=list,
        metadata={
            "name": "EnactStatement",
            "type": "Element",
        },
    )
    toc: list[Toc] = field(
        default_factory=list,
        metadata={
            "name": "TOC",
            "type": "Element",
            "max_occurs": 3,
        },
    )
    preamble: None | Preamble = field(
        default=None,
        metadata={
            "name": "Preamble",
            "type": "Element",
        },
    )
    main_provision: MainProvision = field(
        metadata={
            "name": "MainProvision",
            "type": "Element",
        }
    )
    suppl_provision: list[SupplProvision] = field(
        default_factory=list,
        metadata={
            "name": "SupplProvision",
            "type": "Element",
        },
    )
    appdx_table: list[AppdxTable] = field(
        default_factory=list,
        metadata={
            "name": "AppdxTable",
            "type": "Element",
        },
    )
    appdx_note: list[AppdxNote] = field(
        default_factory=list,
        metadata={
            "name": "AppdxNote",
            "type": "Element",
        },
    )
    appdx_style: list[AppdxStyle] = field(
        default_factory=list,
        metadata={
            "name": "AppdxStyle",
            "type": "Element",
        },
    )
    appdx: list[Appdx] = field(
        default_factory=list,
        metadata={
            "name": "Appdx",
            "type": "Element",
        },
    )
    appdx_fig: list[AppdxFig] = field(
        default_factory=list,
        metadata={
            "name": "AppdxFig",
            "type": "Element",
        },
    )
    appdx_format: list[AppdxFormat] = field(
        default_factory=list,
        metadata={
            "name": "AppdxFormat",
            "type": "Element",
        },
    )
    subject: None | object = field(
        default=None,
        metadata={
            "name": "Subject",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class List:
    list_sentence: ListSentence = field(
        metadata={
            "name": "ListSentence",
            "type": "Element",
        }
    )
    sublist1: list[Sublist1] = field(
        default_factory=list,
        metadata={
            "name": "Sublist1",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Item:
    item_title: None | ItemTitle = field(
        default=None,
        metadata={
            "name": "ItemTitle",
            "type": "Element",
        },
    )
    item_sentence: ItemSentence = field(
        metadata={
            "name": "ItemSentence",
            "type": "Element",
        }
    )
    subitem1: list[Subitem1] = field(
        default_factory=list,
        metadata={
            "name": "Subitem1",
            "type": "Element",
        },
    )
    table_struct: list[TableStruct] = field(
        default_factory=list,
        metadata={
            "name": "TableStruct",
            "type": "Element",
        },
    )
    fig_struct: list[FigStruct] = field(
        default_factory=list,
        metadata={
            "name": "FigStruct",
            "type": "Element",
        },
    )
    style_struct: list[StyleStruct] = field(
        default_factory=list,
        metadata={
            "name": "StyleStruct",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "List",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Law:
    law_num: LawNum = field(
        metadata={
            "name": "LawNum",
            "type": "Element",
        }
    )
    law_body: LawBody = field(
        metadata={
            "name": "LawBody",
            "type": "Element",
        }
    )
    era: LawEra = field(
        metadata={
            "name": "Era",
            "type": "Attribute",
        }
    )
    year: int = field(
        metadata={
            "name": "Year",
            "type": "Attribute",
        }
    )
    num: int = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    promulgate_month: None | int = field(
        default=None,
        metadata={
            "name": "PromulgateMonth",
            "type": "Attribute",
        },
    )
    promulgate_day: None | int = field(
        default=None,
        metadata={
            "name": "PromulgateDay",
            "type": "Attribute",
        },
    )
    law_type: LawLawType = field(
        metadata={
            "name": "LawType",
            "type": "Attribute",
        }
    )
    lang: LawLang = field(
        metadata={
            "name": "Lang",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class Paragraph:
    paragraph_caption: None | ParagraphCaption = field(
        default=None,
        metadata={
            "name": "ParagraphCaption",
            "type": "Element",
        },
    )
    paragraph_num: ParagraphNum = field(
        metadata={
            "name": "ParagraphNum",
            "type": "Element",
        }
    )
    paragraph_sentence: ParagraphSentence = field(
        metadata={
            "name": "ParagraphSentence",
            "type": "Element",
        }
    )
    amend_provision: list[AmendProvision] = field(
        default_factory=list,
        metadata={
            "name": "AmendProvision",
            "type": "Element",
        },
    )
    class_value: list[Class] = field(
        default_factory=list,
        metadata={
            "name": "Class",
            "type": "Element",
        },
    )
    table_struct: list[TableStruct] = field(
        default_factory=list,
        metadata={
            "name": "TableStruct",
            "type": "Element",
            "sequence": 1,
        },
    )
    fig_struct: list[FigStruct] = field(
        default_factory=list,
        metadata={
            "name": "FigStruct",
            "type": "Element",
            "sequence": 1,
        },
    )
    style_struct: list[StyleStruct] = field(
        default_factory=list,
        metadata={
            "name": "StyleStruct",
            "type": "Element",
            "sequence": 1,
        },
    )
    item: list[Item] = field(
        default_factory=list,
        metadata={
            "name": "Item",
            "type": "Element",
            "sequence": 1,
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "List",
            "type": "Element",
        },
    )
    num: int = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    old_style: bool = field(
        default=False,
        metadata={
            "name": "OldStyle",
            "type": "Attribute",
        },
    )
    old_num: bool = field(
        default=False,
        metadata={
            "name": "OldNum",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class MainProvision:
    part: list[Part] = field(
        default_factory=list,
        metadata={
            "name": "Part",
            "type": "Element",
        },
    )
    chapter: list[Chapter] = field(
        default_factory=list,
        metadata={
            "name": "Chapter",
            "type": "Element",
        },
    )
    section: list[Section] = field(
        default_factory=list,
        metadata={
            "name": "Section",
            "type": "Element",
        },
    )
    article: list[Article] = field(
        default_factory=list,
        metadata={
            "name": "Article",
            "type": "Element",
        },
    )
    paragraph: list[Paragraph] = field(
        default_factory=list,
        metadata={
            "name": "Paragraph",
            "type": "Element",
        },
    )
    extract: None | bool = field(
        default=None,
        metadata={
            "name": "Extract",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Remarks:
    remarks_label: RemarksLabel = field(
        metadata={
            "name": "RemarksLabel",
            "type": "Element",
        }
    )
    item: list[Item] = field(
        default_factory=list,
        metadata={
            "name": "Item",
            "type": "Element",
        },
    )
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Appdx:
    arith_formula_num: None | ArithFormulaNum = field(
        default=None,
        metadata={
            "name": "ArithFormulaNum",
            "type": "Element",
        },
    )
    related_article_num: None | RelatedArticleNum = field(
        default=None,
        metadata={
            "name": "RelatedArticleNum",
            "type": "Element",
        },
    )
    arith_formula: list[ArithFormula] = field(
        default_factory=list,
        metadata={
            "name": "ArithFormula",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    remarks: None | Remarks = field(
        default=None,
        metadata={
            "name": "Remarks",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class FigStruct:
    fig_struct_title: None | FigStructTitle = field(
        default=None,
        metadata={
            "name": "FigStructTitle",
            "type": "Element",
        },
    )
    remarks: list[Remarks] = field(
        default_factory=list,
        metadata={
            "name": "Remarks",
            "type": "Element",
        },
    )
    fig: Fig = field(
        metadata={
            "name": "Fig",
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class FormatStruct:
    format_struct_title: None | FormatStructTitle = field(
        default=None,
        metadata={
            "name": "FormatStructTitle",
            "type": "Element",
        },
    )
    remarks: list[Remarks] = field(
        default_factory=list,
        metadata={
            "name": "Remarks",
            "type": "Element",
        },
    )
    format: Format = field(
        metadata={
            "name": "Format",
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class NoteStruct:
    note_struct_title: None | NoteStructTitle = field(
        default=None,
        metadata={
            "name": "NoteStructTitle",
            "type": "Element",
        },
    )
    remarks: list[Remarks] = field(
        default_factory=list,
        metadata={
            "name": "Remarks",
            "type": "Element",
        },
    )
    note: Note = field(
        metadata={
            "name": "Note",
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class StyleStruct:
    style_struct_title: None | StyleStructTitle = field(
        default=None,
        metadata={
            "name": "StyleStructTitle",
            "type": "Element",
        },
    )
    remarks: list[Remarks] = field(
        default_factory=list,
        metadata={
            "name": "Remarks",
            "type": "Element",
        },
    )
    style: Style = field(
        metadata={
            "name": "Style",
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class AppdxFormat:
    appdx_format_title: None | AppdxFormatTitle = field(
        default=None,
        metadata={
            "name": "AppdxFormatTitle",
            "type": "Element",
        },
    )
    related_article_num: None | RelatedArticleNum = field(
        default=None,
        metadata={
            "name": "RelatedArticleNum",
            "type": "Element",
        },
    )
    format_struct: list[FormatStruct] = field(
        default_factory=list,
        metadata={
            "name": "FormatStruct",
            "type": "Element",
        },
    )
    remarks: None | Remarks = field(
        default=None,
        metadata={
            "name": "Remarks",
            "type": "Element",
        },
    )
    num: None | int = field(
        default=None,
        metadata={
            "name": "Num",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AppdxStyle:
    appdx_style_title: None | AppdxStyleTitle = field(
        default=None,
        metadata={
            "name": "AppdxStyleTitle",
            "type": "Element",
        },
    )
    related_article_num: None | RelatedArticleNum = field(
        default=None,
        metadata={
            "name": "RelatedArticleNum",
            "type": "Element",
        },
    )
    style_struct: list[StyleStruct] = field(
        default_factory=list,
        metadata={
            "name": "StyleStruct",
            "type": "Element",
        },
    )
    remarks: None | Remarks = field(
        default=None,
        metadata={
            "name": "Remarks",
            "type": "Element",
        },
    )
    num: None | int = field(
        default=None,
        metadata={
            "name": "Num",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Subitem1:
    subitem1_title: None | Subitem1Title = field(
        default=None,
        metadata={
            "name": "Subitem1Title",
            "type": "Element",
        },
    )
    subitem1_sentence: Subitem1Sentence = field(
        metadata={
            "name": "Subitem1Sentence",
            "type": "Element",
        }
    )
    subitem2: list[Subitem2] = field(
        default_factory=list,
        metadata={
            "name": "Subitem2",
            "type": "Element",
        },
    )
    table_struct: list[TableStruct] = field(
        default_factory=list,
        metadata={
            "name": "TableStruct",
            "type": "Element",
        },
    )
    fig_struct: list[FigStruct] = field(
        default_factory=list,
        metadata={
            "name": "FigStruct",
            "type": "Element",
        },
    )
    style_struct: list[StyleStruct] = field(
        default_factory=list,
        metadata={
            "name": "StyleStruct",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "List",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Subitem10:
    subitem10_title: None | Subitem10Title = field(
        default=None,
        metadata={
            "name": "Subitem10Title",
            "type": "Element",
        },
    )
    subitem10_sentence: Subitem10Sentence = field(
        metadata={
            "name": "Subitem10Sentence",
            "type": "Element",
        }
    )
    table_struct: list[TableStruct] = field(
        default_factory=list,
        metadata={
            "name": "TableStruct",
            "type": "Element",
        },
    )
    fig_struct: list[FigStruct] = field(
        default_factory=list,
        metadata={
            "name": "FigStruct",
            "type": "Element",
        },
    )
    style_struct: list[StyleStruct] = field(
        default_factory=list,
        metadata={
            "name": "StyleStruct",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "List",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Subitem2:
    subitem2_title: None | Subitem2Title = field(
        default=None,
        metadata={
            "name": "Subitem2Title",
            "type": "Element",
        },
    )
    subitem2_sentence: Subitem2Sentence = field(
        metadata={
            "name": "Subitem2Sentence",
            "type": "Element",
        }
    )
    subitem3: list[Subitem3] = field(
        default_factory=list,
        metadata={
            "name": "Subitem3",
            "type": "Element",
        },
    )
    table_struct: list[TableStruct] = field(
        default_factory=list,
        metadata={
            "name": "TableStruct",
            "type": "Element",
        },
    )
    fig_struct: list[FigStruct] = field(
        default_factory=list,
        metadata={
            "name": "FigStruct",
            "type": "Element",
        },
    )
    style_struct: list[StyleStruct] = field(
        default_factory=list,
        metadata={
            "name": "StyleStruct",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "List",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Subitem3:
    subitem3_title: None | Subitem3Title = field(
        default=None,
        metadata={
            "name": "Subitem3Title",
            "type": "Element",
        },
    )
    subitem3_sentence: Subitem3Sentence = field(
        metadata={
            "name": "Subitem3Sentence",
            "type": "Element",
        }
    )
    subitem4: list[Subitem4] = field(
        default_factory=list,
        metadata={
            "name": "Subitem4",
            "type": "Element",
        },
    )
    table_struct: list[TableStruct] = field(
        default_factory=list,
        metadata={
            "name": "TableStruct",
            "type": "Element",
        },
    )
    fig_struct: list[FigStruct] = field(
        default_factory=list,
        metadata={
            "name": "FigStruct",
            "type": "Element",
        },
    )
    style_struct: list[StyleStruct] = field(
        default_factory=list,
        metadata={
            "name": "StyleStruct",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "List",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Subitem4:
    subitem4_title: None | Subitem4Title = field(
        default=None,
        metadata={
            "name": "Subitem4Title",
            "type": "Element",
        },
    )
    subitem4_sentence: Subitem4Sentence = field(
        metadata={
            "name": "Subitem4Sentence",
            "type": "Element",
        }
    )
    subitem5: list[Subitem5] = field(
        default_factory=list,
        metadata={
            "name": "Subitem5",
            "type": "Element",
        },
    )
    table_struct: list[TableStruct] = field(
        default_factory=list,
        metadata={
            "name": "TableStruct",
            "type": "Element",
        },
    )
    fig_struct: list[FigStruct] = field(
        default_factory=list,
        metadata={
            "name": "FigStruct",
            "type": "Element",
        },
    )
    style_struct: list[StyleStruct] = field(
        default_factory=list,
        metadata={
            "name": "StyleStruct",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "List",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Subitem5:
    subitem5_title: None | Subitem5Title = field(
        default=None,
        metadata={
            "name": "Subitem5Title",
            "type": "Element",
        },
    )
    subitem5_sentence: Subitem5Sentence = field(
        metadata={
            "name": "Subitem5Sentence",
            "type": "Element",
        }
    )
    subitem6: list[Subitem6] = field(
        default_factory=list,
        metadata={
            "name": "Subitem6",
            "type": "Element",
        },
    )
    table_struct: list[TableStruct] = field(
        default_factory=list,
        metadata={
            "name": "TableStruct",
            "type": "Element",
        },
    )
    fig_struct: list[FigStruct] = field(
        default_factory=list,
        metadata={
            "name": "FigStruct",
            "type": "Element",
        },
    )
    style_struct: list[StyleStruct] = field(
        default_factory=list,
        metadata={
            "name": "StyleStruct",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "List",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Subitem6:
    subitem6_title: None | Subitem6Title = field(
        default=None,
        metadata={
            "name": "Subitem6Title",
            "type": "Element",
        },
    )
    subitem6_sentence: Subitem6Sentence = field(
        metadata={
            "name": "Subitem6Sentence",
            "type": "Element",
        }
    )
    subitem7: list[Subitem7] = field(
        default_factory=list,
        metadata={
            "name": "Subitem7",
            "type": "Element",
        },
    )
    table_struct: list[TableStruct] = field(
        default_factory=list,
        metadata={
            "name": "TableStruct",
            "type": "Element",
        },
    )
    fig_struct: list[FigStruct] = field(
        default_factory=list,
        metadata={
            "name": "FigStruct",
            "type": "Element",
        },
    )
    style_struct: list[StyleStruct] = field(
        default_factory=list,
        metadata={
            "name": "StyleStruct",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "List",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Subitem7:
    subitem7_title: None | Subitem7Title = field(
        default=None,
        metadata={
            "name": "Subitem7Title",
            "type": "Element",
        },
    )
    subitem7_sentence: Subitem7Sentence = field(
        metadata={
            "name": "Subitem7Sentence",
            "type": "Element",
        }
    )
    subitem8: list[Subitem8] = field(
        default_factory=list,
        metadata={
            "name": "Subitem8",
            "type": "Element",
        },
    )
    table_struct: list[TableStruct] = field(
        default_factory=list,
        metadata={
            "name": "TableStruct",
            "type": "Element",
        },
    )
    fig_struct: list[FigStruct] = field(
        default_factory=list,
        metadata={
            "name": "FigStruct",
            "type": "Element",
        },
    )
    style_struct: list[StyleStruct] = field(
        default_factory=list,
        metadata={
            "name": "StyleStruct",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "List",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Subitem8:
    subitem8_title: None | Subitem8Title = field(
        default=None,
        metadata={
            "name": "Subitem8Title",
            "type": "Element",
        },
    )
    subitem8_sentence: Subitem8Sentence = field(
        metadata={
            "name": "Subitem8Sentence",
            "type": "Element",
        }
    )
    subitem9: list[Subitem9] = field(
        default_factory=list,
        metadata={
            "name": "Subitem9",
            "type": "Element",
        },
    )
    table_struct: list[TableStruct] = field(
        default_factory=list,
        metadata={
            "name": "TableStruct",
            "type": "Element",
        },
    )
    fig_struct: list[FigStruct] = field(
        default_factory=list,
        metadata={
            "name": "FigStruct",
            "type": "Element",
        },
    )
    style_struct: list[StyleStruct] = field(
        default_factory=list,
        metadata={
            "name": "StyleStruct",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "List",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Subitem9:
    subitem9_title: None | Subitem9Title = field(
        default=None,
        metadata={
            "name": "Subitem9Title",
            "type": "Element",
        },
    )
    subitem9_sentence: Subitem9Sentence = field(
        metadata={
            "name": "Subitem9Sentence",
            "type": "Element",
        }
    )
    subitem10: list[Subitem10] = field(
        default_factory=list,
        metadata={
            "name": "Subitem10",
            "type": "Element",
        },
    )
    table_struct: list[TableStruct] = field(
        default_factory=list,
        metadata={
            "name": "TableStruct",
            "type": "Element",
        },
    )
    fig_struct: list[FigStruct] = field(
        default_factory=list,
        metadata={
            "name": "FigStruct",
            "type": "Element",
        },
    )
    style_struct: list[StyleStruct] = field(
        default_factory=list,
        metadata={
            "name": "StyleStruct",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "List",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )
    delete: bool = field(
        default=False,
        metadata={
            "name": "Delete",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "name": "Hide",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class SupplProvisionAppdxStyle:
    suppl_provision_appdx_style_title: SupplProvisionAppdxStyleTitle = field(
        metadata={
            "name": "SupplProvisionAppdxStyleTitle",
            "type": "Element",
        }
    )
    related_article_num: None | RelatedArticleNum = field(
        default=None,
        metadata={
            "name": "RelatedArticleNum",
            "type": "Element",
        },
    )
    style_struct: list[StyleStruct] = field(
        default_factory=list,
        metadata={
            "name": "StyleStruct",
            "type": "Element",
        },
    )
    num: None | int = field(
        default=None,
        metadata={
            "name": "Num",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class TableColumn:
    part: list[Part] = field(
        default_factory=list,
        metadata={
            "name": "Part",
            "type": "Element",
        },
    )
    chapter: list[Chapter] = field(
        default_factory=list,
        metadata={
            "name": "Chapter",
            "type": "Element",
        },
    )
    section: list[Section] = field(
        default_factory=list,
        metadata={
            "name": "Section",
            "type": "Element",
        },
    )
    subsection: list[Subsection] = field(
        default_factory=list,
        metadata={
            "name": "Subsection",
            "type": "Element",
        },
    )
    division: list[Division] = field(
        default_factory=list,
        metadata={
            "name": "Division",
            "type": "Element",
        },
    )
    article: list[Article] = field(
        default_factory=list,
        metadata={
            "name": "Article",
            "type": "Element",
        },
    )
    paragraph: list[Paragraph] = field(
        default_factory=list,
        metadata={
            "name": "Paragraph",
            "type": "Element",
        },
    )
    item: list[Item] = field(
        default_factory=list,
        metadata={
            "name": "Item",
            "type": "Element",
        },
    )
    subitem1: list[Subitem1] = field(
        default_factory=list,
        metadata={
            "name": "Subitem1",
            "type": "Element",
        },
    )
    subitem2: list[Subitem2] = field(
        default_factory=list,
        metadata={
            "name": "Subitem2",
            "type": "Element",
        },
    )
    subitem3: list[Subitem3] = field(
        default_factory=list,
        metadata={
            "name": "Subitem3",
            "type": "Element",
        },
    )
    subitem4: list[Subitem4] = field(
        default_factory=list,
        metadata={
            "name": "Subitem4",
            "type": "Element",
        },
    )
    subitem5: list[Subitem5] = field(
        default_factory=list,
        metadata={
            "name": "Subitem5",
            "type": "Element",
        },
    )
    subitem6: list[Subitem6] = field(
        default_factory=list,
        metadata={
            "name": "Subitem6",
            "type": "Element",
        },
    )
    subitem7: list[Subitem7] = field(
        default_factory=list,
        metadata={
            "name": "Subitem7",
            "type": "Element",
        },
    )
    subitem8: list[Subitem8] = field(
        default_factory=list,
        metadata={
            "name": "Subitem8",
            "type": "Element",
        },
    )
    subitem9: list[Subitem9] = field(
        default_factory=list,
        metadata={
            "name": "Subitem9",
            "type": "Element",
        },
    )
    subitem10: list[Subitem10] = field(
        default_factory=list,
        metadata={
            "name": "Subitem10",
            "type": "Element",
        },
    )
    fig_struct: list[FigStruct] = field(
        default_factory=list,
        metadata={
            "name": "FigStruct",
            "type": "Element",
        },
    )
    remarks: None | Remarks = field(
        default=None,
        metadata={
            "name": "Remarks",
            "type": "Element",
        },
    )
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )
    border_top: TableColumnBorderTop = field(
        default=TableColumnBorderTop.SOLID,
        metadata={
            "name": "BorderTop",
            "type": "Attribute",
        },
    )
    border_bottom: TableColumnBorderBottom = field(
        default=TableColumnBorderBottom.SOLID,
        metadata={
            "name": "BorderBottom",
            "type": "Attribute",
        },
    )
    border_left: TableColumnBorderLeft = field(
        default=TableColumnBorderLeft.SOLID,
        metadata={
            "name": "BorderLeft",
            "type": "Attribute",
        },
    )
    border_right: TableColumnBorderRight = field(
        default=TableColumnBorderRight.SOLID,
        metadata={
            "name": "BorderRight",
            "type": "Attribute",
        },
    )
    rowspan: None | object = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    colspan: None | object = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    align: None | TableColumnAlign = field(
        default=None,
        metadata={
            "name": "Align",
            "type": "Attribute",
        },
    )
    valign: None | TableColumnValign = field(
        default=None,
        metadata={
            "name": "Valign",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class TableRow:
    table_column: list[TableColumn] = field(
        default_factory=list,
        metadata={
            "name": "TableColumn",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class Table:
    table_header_row: list[TableHeaderRow] = field(
        default_factory=list,
        metadata={
            "name": "TableHeaderRow",
            "type": "Element",
        },
    )
    table_row: list[TableRow] = field(
        default_factory=list,
        metadata={
            "name": "TableRow",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    writing_mode: TableWritingMode = field(
        default=TableWritingMode.VERTICAL,
        metadata={
            "name": "WritingMode",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ClassSentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )
    table: None | Table = field(
        default=None,
        metadata={
            "name": "Table",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class ItemSentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )
    table: None | Table = field(
        default=None,
        metadata={
            "name": "Table",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Subitem10Sentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )
    table: None | Table = field(
        default=None,
        metadata={
            "name": "Table",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Subitem1Sentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )
    table: None | Table = field(
        default=None,
        metadata={
            "name": "Table",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Subitem2Sentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )
    table: None | Table = field(
        default=None,
        metadata={
            "name": "Table",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Subitem3Sentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )
    table: None | Table = field(
        default=None,
        metadata={
            "name": "Table",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Subitem4Sentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )
    table: None | Table = field(
        default=None,
        metadata={
            "name": "Table",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Subitem5Sentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )
    table: None | Table = field(
        default=None,
        metadata={
            "name": "Table",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Subitem6Sentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )
    table: None | Table = field(
        default=None,
        metadata={
            "name": "Table",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Subitem7Sentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )
    table: None | Table = field(
        default=None,
        metadata={
            "name": "Table",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Subitem8Sentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )
    table: None | Table = field(
        default=None,
        metadata={
            "name": "Table",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Subitem9Sentence:
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    column: list[Column] = field(
        default_factory=list,
        metadata={
            "name": "Column",
            "type": "Element",
        },
    )
    table: None | Table = field(
        default=None,
        metadata={
            "name": "Table",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class TableStruct:
    table_struct_title: None | TableStructTitle = field(
        default=None,
        metadata={
            "name": "TableStructTitle",
            "type": "Element",
        },
    )
    remarks: list[Remarks] = field(
        default_factory=list,
        metadata={
            "name": "Remarks",
            "type": "Element",
        },
    )
    table: Table = field(
        metadata={
            "name": "Table",
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class AppdxFig:
    appdx_fig_title: None | AppdxFigTitle = field(
        default=None,
        metadata={
            "name": "AppdxFigTitle",
            "type": "Element",
        },
    )
    related_article_num: None | RelatedArticleNum = field(
        default=None,
        metadata={
            "name": "RelatedArticleNum",
            "type": "Element",
        },
    )
    fig_struct: list[FigStruct] = field(
        default_factory=list,
        metadata={
            "name": "FigStruct",
            "type": "Element",
        },
    )
    table_struct: list[TableStruct] = field(
        default_factory=list,
        metadata={
            "name": "TableStruct",
            "type": "Element",
        },
    )
    num: None | int = field(
        default=None,
        metadata={
            "name": "Num",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AppdxNote:
    appdx_note_title: None | AppdxNoteTitle = field(
        default=None,
        metadata={
            "name": "AppdxNoteTitle",
            "type": "Element",
        },
    )
    related_article_num: None | RelatedArticleNum = field(
        default=None,
        metadata={
            "name": "RelatedArticleNum",
            "type": "Element",
        },
    )
    note_struct: list[NoteStruct] = field(
        default_factory=list,
        metadata={
            "name": "NoteStruct",
            "type": "Element",
        },
    )
    fig_struct: list[FigStruct] = field(
        default_factory=list,
        metadata={
            "name": "FigStruct",
            "type": "Element",
        },
    )
    table_struct: list[TableStruct] = field(
        default_factory=list,
        metadata={
            "name": "TableStruct",
            "type": "Element",
        },
    )
    remarks: None | Remarks = field(
        default=None,
        metadata={
            "name": "Remarks",
            "type": "Element",
        },
    )
    num: None | int = field(
        default=None,
        metadata={
            "name": "Num",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AppdxTable:
    appdx_table_title: None | AppdxTableTitle = field(
        default=None,
        metadata={
            "name": "AppdxTableTitle",
            "type": "Element",
        },
    )
    related_article_num: None | RelatedArticleNum = field(
        default=None,
        metadata={
            "name": "RelatedArticleNum",
            "type": "Element",
        },
    )
    table_struct: list[TableStruct] = field(
        default_factory=list,
        metadata={
            "name": "TableStruct",
            "type": "Element",
        },
    )
    item: list[Item] = field(
        default_factory=list,
        metadata={
            "name": "Item",
            "type": "Element",
        },
    )
    remarks: None | Remarks = field(
        default=None,
        metadata={
            "name": "Remarks",
            "type": "Element",
        },
    )
    num: None | int = field(
        default=None,
        metadata={
            "name": "Num",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Class:
    class_title: None | ClassTitle = field(
        default=None,
        metadata={
            "name": "ClassTitle",
            "type": "Element",
        },
    )
    class_sentence: ClassSentence = field(
        metadata={
            "name": "ClassSentence",
            "type": "Element",
        }
    )
    item: list[Item] = field(
        default_factory=list,
        metadata={
            "name": "Item",
            "type": "Element",
        },
    )
    num: object = field(
        metadata={
            "name": "Num",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class SupplProvisionAppdxTable:
    suppl_provision_appdx_table_title: SupplProvisionAppdxTableTitle = field(
        metadata={
            "name": "SupplProvisionAppdxTableTitle",
            "type": "Element",
        }
    )
    related_article_num: None | RelatedArticleNum = field(
        default=None,
        metadata={
            "name": "RelatedArticleNum",
            "type": "Element",
        },
    )
    table_struct: list[TableStruct] = field(
        default_factory=list,
        metadata={
            "name": "TableStruct",
            "type": "Element",
        },
    )
    num: None | int = field(
        default=None,
        metadata={
            "name": "Num",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class NewProvision:
    law_title: None | LawTitle = field(
        default=None,
        metadata={
            "name": "LawTitle",
            "type": "Element",
        },
    )
    preamble: None | Preamble = field(
        default=None,
        metadata={
            "name": "Preamble",
            "type": "Element",
        },
    )
    toc: None | Toc = field(
        default=None,
        metadata={
            "name": "TOC",
            "type": "Element",
        },
    )
    part: list[Part] = field(
        default_factory=list,
        metadata={
            "name": "Part",
            "type": "Element",
        },
    )
    part_title: list[PartTitle] = field(
        default_factory=list,
        metadata={
            "name": "PartTitle",
            "type": "Element",
        },
    )
    chapter: list[Chapter] = field(
        default_factory=list,
        metadata={
            "name": "Chapter",
            "type": "Element",
        },
    )
    chapter_title: list[ChapterTitle] = field(
        default_factory=list,
        metadata={
            "name": "ChapterTitle",
            "type": "Element",
        },
    )
    section: list[Section] = field(
        default_factory=list,
        metadata={
            "name": "Section",
            "type": "Element",
        },
    )
    section_title: list[SectionTitle] = field(
        default_factory=list,
        metadata={
            "name": "SectionTitle",
            "type": "Element",
        },
    )
    subsection: list[Subsection] = field(
        default_factory=list,
        metadata={
            "name": "Subsection",
            "type": "Element",
        },
    )
    subsection_title: list[SubsectionTitle] = field(
        default_factory=list,
        metadata={
            "name": "SubsectionTitle",
            "type": "Element",
        },
    )
    division: list[Division] = field(
        default_factory=list,
        metadata={
            "name": "Division",
            "type": "Element",
        },
    )
    division_title: list[DivisionTitle] = field(
        default_factory=list,
        metadata={
            "name": "DivisionTitle",
            "type": "Element",
        },
    )
    article: list[Article] = field(
        default_factory=list,
        metadata={
            "name": "Article",
            "type": "Element",
        },
    )
    suppl_note: list[SupplNote] = field(
        default_factory=list,
        metadata={
            "name": "SupplNote",
            "type": "Element",
        },
    )
    paragraph: list[Paragraph] = field(
        default_factory=list,
        metadata={
            "name": "Paragraph",
            "type": "Element",
        },
    )
    item: list[Item] = field(
        default_factory=list,
        metadata={
            "name": "Item",
            "type": "Element",
        },
    )
    subitem1: list[Subitem1] = field(
        default_factory=list,
        metadata={
            "name": "Subitem1",
            "type": "Element",
        },
    )
    subitem2: list[Subitem2] = field(
        default_factory=list,
        metadata={
            "name": "Subitem2",
            "type": "Element",
        },
    )
    subitem3: list[Subitem3] = field(
        default_factory=list,
        metadata={
            "name": "Subitem3",
            "type": "Element",
        },
    )
    subitem4: list[Subitem4] = field(
        default_factory=list,
        metadata={
            "name": "Subitem4",
            "type": "Element",
        },
    )
    subitem5: list[Subitem5] = field(
        default_factory=list,
        metadata={
            "name": "Subitem5",
            "type": "Element",
        },
    )
    subitem6: list[Subitem6] = field(
        default_factory=list,
        metadata={
            "name": "Subitem6",
            "type": "Element",
        },
    )
    subitem7: list[Subitem7] = field(
        default_factory=list,
        metadata={
            "name": "Subitem7",
            "type": "Element",
        },
    )
    subitem8: list[Subitem8] = field(
        default_factory=list,
        metadata={
            "name": "Subitem8",
            "type": "Element",
        },
    )
    subitem9: list[Subitem9] = field(
        default_factory=list,
        metadata={
            "name": "Subitem9",
            "type": "Element",
        },
    )
    subitem10: list[Subitem10] = field(
        default_factory=list,
        metadata={
            "name": "Subitem10",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "List",
            "type": "Element",
        },
    )
    sentence: list[Sentence] = field(
        default_factory=list,
        metadata={
            "name": "Sentence",
            "type": "Element",
        },
    )
    amend_provision: list[AmendProvision] = field(
        default_factory=list,
        metadata={
            "name": "AmendProvision",
            "type": "Element",
        },
    )
    appdx_table: list[AppdxTable] = field(
        default_factory=list,
        metadata={
            "name": "AppdxTable",
            "type": "Element",
        },
    )
    appdx_note: list[AppdxNote] = field(
        default_factory=list,
        metadata={
            "name": "AppdxNote",
            "type": "Element",
        },
    )
    appdx_style: list[AppdxStyle] = field(
        default_factory=list,
        metadata={
            "name": "AppdxStyle",
            "type": "Element",
        },
    )
    appdx: list[Appdx] = field(
        default_factory=list,
        metadata={
            "name": "Appdx",
            "type": "Element",
        },
    )
    appdx_fig: list[AppdxFig] = field(
        default_factory=list,
        metadata={
            "name": "AppdxFig",
            "type": "Element",
        },
    )
    appdx_format: list[AppdxFormat] = field(
        default_factory=list,
        metadata={
            "name": "AppdxFormat",
            "type": "Element",
        },
    )
    suppl_provision_appdx_style: list[SupplProvisionAppdxStyle] = field(
        default_factory=list,
        metadata={
            "name": "SupplProvisionAppdxStyle",
            "type": "Element",
        },
    )
    suppl_provision_appdx_table: list[SupplProvisionAppdxTable] = field(
        default_factory=list,
        metadata={
            "name": "SupplProvisionAppdxTable",
            "type": "Element",
        },
    )
    suppl_provision_appdx: list[SupplProvisionAppdx] = field(
        default_factory=list,
        metadata={
            "name": "SupplProvisionAppdx",
            "type": "Element",
        },
    )
    table_struct: None | TableStruct = field(
        default=None,
        metadata={
            "name": "TableStruct",
            "type": "Element",
        },
    )
    table_row: list[TableRow] = field(
        default_factory=list,
        metadata={
            "name": "TableRow",
            "type": "Element",
        },
    )
    table_column: list[TableColumn] = field(
        default_factory=list,
        metadata={
            "name": "TableColumn",
            "type": "Element",
        },
    )
    fig_struct: None | FigStruct = field(
        default=None,
        metadata={
            "name": "FigStruct",
            "type": "Element",
        },
    )
    note_struct: None | NoteStruct = field(
        default=None,
        metadata={
            "name": "NoteStruct",
            "type": "Element",
        },
    )
    style_struct: None | StyleStruct = field(
        default=None,
        metadata={
            "name": "StyleStruct",
            "type": "Element",
        },
    )
    format_struct: None | FormatStruct = field(
        default=None,
        metadata={
            "name": "FormatStruct",
            "type": "Element",
        },
    )
    remarks: None | Remarks = field(
        default=None,
        metadata={
            "name": "Remarks",
            "type": "Element",
        },
    )
    law_body: None | LawBody = field(
        default=None,
        metadata={
            "name": "LawBody",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class SupplProvision:
    suppl_provision_label: SupplProvisionLabel = field(
        metadata={
            "name": "SupplProvisionLabel",
            "type": "Element",
        }
    )
    chapter: list[Chapter] = field(
        default_factory=list,
        metadata={
            "name": "Chapter",
            "type": "Element",
        },
    )
    article: list[Article] = field(
        default_factory=list,
        metadata={
            "name": "Article",
            "type": "Element",
        },
    )
    paragraph: list[Paragraph] = field(
        default_factory=list,
        metadata={
            "name": "Paragraph",
            "type": "Element",
        },
    )
    suppl_provision_appdx_table: list[SupplProvisionAppdxTable] = field(
        default_factory=list,
        metadata={
            "name": "SupplProvisionAppdxTable",
            "type": "Element",
        },
    )
    suppl_provision_appdx_style: list[SupplProvisionAppdxStyle] = field(
        default_factory=list,
        metadata={
            "name": "SupplProvisionAppdxStyle",
            "type": "Element",
        },
    )
    suppl_provision_appdx: list[SupplProvisionAppdx] = field(
        default_factory=list,
        metadata={
            "name": "SupplProvisionAppdx",
            "type": "Element",
        },
    )
    type_value: None | SupplProvisionType = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Attribute",
        },
    )
    amend_law_num: None | object = field(
        default=None,
        metadata={
            "name": "AmendLawNum",
            "type": "Attribute",
        },
    )
    extract: None | bool = field(
        default=None,
        metadata={
            "name": "Extract",
            "type": "Attribute",
        },
    )
