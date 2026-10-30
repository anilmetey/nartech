"""Preserve emphasis from source Word paragraphs in generated page copy."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import re

from docx import Document

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# The English source paragraphs below are translated into Turkish for the site.
# Keep their emphasis on the matching translated phrase as well.
TRANSLATED_BOLD = {
    ("Products (3).docx", 85, "tr"): ["iç yüzer tavan (IFR)"],
    ("Products (3).docx", 87, "tr"): ["Temel İşlevler ve Faydalar"],
    ("Products (3).docx", 88, "tr"): ["Üstün Emisyon Azaltımı:"],
    ("Products (3).docx", 89, "tr"): ["Çevre ve Çalışanların Korunması:"],
    ("Products (3).docx", 90, "tr"): ["Dengeli Kararlılık ve Güvenlik:"],
    ("Products (3).docx", 91, "tr"): ["Tedarik ve Kalite Güvencemiz"],
    ("Products (3).docx", 107, "tr"): ["iç yüzer tavan (IFR)"],
    ("Products (3).docx", 108, "tr"): ["Tam Temas Tipi:"],
    ("Products (3).docx", 109, "tr"): ["Temel İşlevler ve Faydalar"],
    ("Products (3).docx", 110, "tr"): ["Sıfıra Yakın VOC Emisyonu:"],
    ("Products (3).docx", 111, "tr"): ["Çevrenin Korunması:"],
    ("Products (3).docx", 112, "tr"): ["Geliştirilmiş Güvenlik ve Buhar Kontrolü:"],
    ("Products (3).docx", 113, "tr"): ["Tedarik ve Kalite Güvencemiz"],
    ("Products (3).docx", 118, "tr"): ["Chemraz XPE contalar"],
    ("Products (3).docx", 120, "tr"): ["Yüksek yoğunluklu polietilen (HDPE)"],
    ("Products (3).docx", 122, "tr"): [
        "Düşük yoğunluklu polietilen (LDPE) contalar",
        "uçucu organik bileşik (VOC)",
    ],
    ("Products (3).docx", 127, "tr"): ["Sabit Köpük Monitörü"],
    ("Products (3).docx", 128, "tr"): ["NFPA 11 Uyumu:", "NFPA 11"],
    ("Products (3).docx", 129, "tr"): ["UL / FM Onayları:", "UL ve FM"],
    ("Products (3).docx", 131, "tr"): ["Köpük Yapıcı"],
    ("Products (3).docx", 132, "tr"): ["NFPA 11 Uyumu:", "NFPA 11"],
    ("Products (3).docx", 133, "tr"): ["UL / FM Onayları:", "UL", "FM sertifikaları"],
    ("Products (3).docx", 135, "tr"): ["Köpük Karıştırıcı (oranlayıcı)"],
    ("Products (3).docx", 136, "tr"): ["NFPA 11 Uyumu:"],
    ("Products (3).docx", 137, "tr"): ["UL / FM Onayları:"],
    ("Products (3).docx", 139, "tr"): ["Köpük Üstten Dökme Cihazı"],
    ("Products (3).docx", 140, "tr"): ["NFPA 11 Uyumu:", "NFPA 11"],
    ("Products (3).docx", 141, "tr"): ["UL / FM Onayları:", "UL", "FM"],
    ("Products (3).docx", 144, "tr"): ["Kenar Sızdırmazlığı Köpük Dökme Cihazı"],
    ("Products (3).docx", 145, "tr"): ["NFPA 11 Uyumu:", "NFPA 11"],
    ("Products (3).docx", 146, "tr"): ["UL / FM Onayları:", "UL", "FM"],
    ("Products (3).docx", 148, "tr"): ["Köpük Tankı"],
    ("Products (3).docx", 149, "tr"): ["NFPA 11 Uyumu:", "NFPA 11"],
    ("Products (3).docx", 150, "tr"): ["UL / FM Onayları:", "UL", "FM sertifikaları"],
    ("Products (3).docx", 153, "tr"): ["köpük", "su sprinklerleri"],
    ("Products (3).docx", 154, "tr"): [
        "UL / FM Onayları ve K-Faktörü Hassasiyeti:",
        "UL",
        "FM",
        "sertifikaları",
        "K-faktörü",
    ],
    ("Products (3).docx", 170, "tr"): ["Endüstriyel Susturucu"],
    ("Products (3).docx", 180, "tr"): [
        "ATEX sertifikalı",
        "Geri Sarmalı Topraklama Makarası (RGR)",
    ],
    ("Products (3).docx", 76, "en"): [
        "Available in locked, unlocked, and closed-to-atmosphere types."
    ],
    ("Supervision Services.docx", 4, "en"): [
        "Physical and Functional Inspection"
    ],
    ("Supervision Services.docx", 7, "en"): ["Sealing Elements and Equipment:"],
    ("Supervision Services.docx", 10, "en"): ["Sealing Elements and Equipment:"],
}


@lru_cache(maxsize=None)
def _source_bold(source: str) -> tuple[str, ...]:
    try:
        filename, line_text = source.rsplit(":", 1)
        paragraph = Document(DOCS / filename).paragraphs[int(line_text) - 1]
    except (OSError, ValueError, IndexError):
        return ()

    spans: list[str] = []
    current = ""
    previous_bold = False
    for run in paragraph.runs:
        bold = run.bold is True
        if bold == previous_bold:
            current += run.text
        else:
            if current.strip() and previous_bold:
                spans.append(current.strip())
            current = run.text
            previous_bold = bold
    if current.strip() and previous_bold:
        spans.append(current.strip())
    return tuple(spans)


def _collapse_space(value: str) -> tuple[str, list[tuple[int, int]]]:
    normalized: list[str] = []
    positions: list[tuple[int, int]] = []
    index = 0
    while index < len(value):
        start = index
        if value[index].isspace():
            while index < len(value) and value[index].isspace():
                index += 1
            if normalized and normalized[-1] == " ":
                positions[-1] = (positions[-1][0], index)
            else:
                normalized.append(" ")
                positions.append((start, index))
            continue
        normalized.append(value[index])
        positions.append((index, index + 1))
        index += 1
    left = 1 if normalized and normalized[0] == " " else 0
    right = len(normalized) - (1 if normalized and normalized[-1] == " " else 0)
    return "".join(normalized[left:right]), positions[left:right]


def format_source_text(value: str, source: str, language: str) -> str:
    """Escape plain copy and restore its DOCX emphasis plus translated equivalents."""
    from html import escape

    source_name, line_text = source.rsplit(":", 1)
    line = int(line_text)
    phrases = list(TRANSLATED_BOLD.get((source_name, line, language), ()))
    phrases.extend(_source_bold(source))
    normalized, positions = _collapse_space(value)

    selected: list[tuple[int, int]] = []
    for phrase in phrases:
        needle, _ = _collapse_space(phrase)
        if not needle:
            continue
        start_at = 0
        while True:
            start = normalized.find(needle, start_at)
            if start < 0:
                break
            end = start + len(needle)
            if not any(start < right and end > left for left, right in selected):
                selected.append((start, end))
                break
            start_at = end

    selected.sort()
    result: list[str] = []
    cursor = 0
    for start, end in selected:
        raw_start = positions[start][0]
        raw_end = positions[end - 1][1]
        if raw_start < cursor:
            continue
        result.append(escape(value[cursor:raw_start], quote=True))
        result.append(f"<strong>{escape(value[raw_start:raw_end], quote=True)}</strong>")
        cursor = raw_end
    result.append(escape(value[cursor:], quote=True))
    return "".join(result)
