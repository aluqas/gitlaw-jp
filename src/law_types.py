from __future__ import annotations

ENGLISH_TO_JAPANESE = {
    "Act": "法律",
    "CabinetOrder": "政令",
    "ImperialOrder": "勅令",
    "MinisterialOrdinance": "省令",
    "Rule": "規則",
    "Ordinance": "府令",
    "PrimeMinisterOfficeOrdinance": "府令",
    "CabinetOfficeOrdinance": "府令",
    "MinistryOrdinance": "省令",
    "告示": "告示",
}

KNOWN_TYPES = {"法律", "政令", "勅令", "府令", "省令", "規則", "告示", "法令"}


def law_category_from_num(law_num: str) -> str:
    for token in ("法律", "政令", "勅令", "府令", "省令", "規則", "告示"):
        if token in law_num:
            return token
    return ""


def normalize_law_type(law_type: str, law_num: str = "") -> str:
    normalized = law_type.strip()
    if normalized in KNOWN_TYPES:
        return normalized
    if normalized in ENGLISH_TO_JAPANESE:
        return ENGLISH_TO_JAPANESE[normalized]

    from_num = law_category_from_num(law_num)
    if from_num:
        return from_num

    if normalized:
        return normalized
    return "法令"
