"""Shared wikitext helpers."""

import re


def format_location(element) -> str:
    """Build {{Location dec|lat|long}} from the location field.

    Accepts "lat|long" as well as values pasted from OpenStreetMap
    ("lat, long"). Any legacy "heading:…" part is dropped.
    """
    location = element.lineEditLocation.text().strip()
    if location == '':
        return ''
    parts = [p.strip() for p in location.replace(",", "|").split("|")]
    parts = [p for p in parts if p and not p.lower().startswith("heading:")]
    if len(parts) < 2:
        return ''
    return '{{Location dec|' + parts[0] + '|' + parts[1] + '}}\n'


def format_categories(session, element) -> str:
    cat_text = session.line_edit_categories.text() + '|' + element.line_edit_categories.text()
    cat_text = cat_text.replace("| ", "|")
    cat_text = cat_text.replace(" | ", "|")
    cat_text = cat_text.strip()
    if cat_text == "|":
        cat_text = "Uploaded with PyCommonist"
    else:
        cat_text += "|Uploaded with PyCommonist"
    cat_text = cat_text.replace("||", "|")
    categories = cat_text.split('|')
    cat_final = ''
    for category in categories:
        if category:
            if re.match(r'^\{\{.*\}\}$', category):
                cat_final = cat_final + category + "\n"
            else:
                cat_final = cat_final + "[[Category:" + category + "]]\n"
    return cat_final


def wrap_description(language: str, description: str) -> str:
    if language:
        return "{{" + language + "|1=" + description + "}}"
    return description
