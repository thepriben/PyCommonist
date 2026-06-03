"""Wikitext builder for {{Information}} uploads."""

from pycommonist.core.wikitext.base import (
    format_categories,
    format_location,
    wrap_description,
)


class InformationWikitextBuilder:
    """Build Commons file description using {{Information}}."""

    def build(self, element, session) -> str:
        location = format_location(element)
        cat_final = format_categories(session, element)
        description = (
            session.line_edit_description.toPlainText()
            + element.line_edit_description.toPlainText()
        )
        description = wrap_description(session.line_edit_language.text(), description)

        additional_templates = element.line_edit_templates.text()
        if additional_templates != '':
            additional_templates = additional_templates + "\n"

        return (
            "== {{int:filedesc}} ==\n"
            "{{Information\n"
            f"|Description = {description}\n"
            f"|Source = {session.line_edit_source.text()}\n"
            f"|Author = {session.line_edit_author.text()}\n"
            f"|Date = {element.line_edit_date_time.text()}\n"
            "|Permission =\n"
            "|other versions =\n"
            "}}\n"
            f"{location}{additional_templates}"
            "== {{int:license-header}} == \n"
            f"{session.line_edit_license.text()}\n\n"
            f"{cat_final}"
        )
