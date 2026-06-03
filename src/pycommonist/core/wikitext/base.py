"""Shared wikitext helpers."""

import re


def format_location(element) -> str:
    location = element.lineEditLocation.text()
    if location == '':
        return ''
    location = location.replace(",", "|")
    return '{{Location dec|' + location + '}}\n'


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
