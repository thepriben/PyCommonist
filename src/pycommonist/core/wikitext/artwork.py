"""Wikitext builder for {{Artwork}} uploads."""

from pycommonist.core.wikitext.base import (
    format_categories,
    format_location,
    wrap_description,
)


class ArtworkWikitextBuilder:
    """Build Commons file description using {{Artwork}}."""

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

        lines = [
            "== {{int:filedesc}} ==",
            "{{Artwork",
            f"|artist = {session.line_edit_artist.text()}",
            f"|title = {session.line_edit_title.text()}",
            f"|object type = {session.line_edit_object_type.text()}",
            f"|description = {description}",
            f"|date = {element.line_edit_date_time.text() or session.line_edit_date.text()}",
            f"|medium = {session.line_edit_medium.text()}",
            f"|institution = {session.line_edit_institution.text()}",
            f"|source = {session.line_edit_source.text()}",
        ]
        wikidata = session.line_edit_wikidata.text().strip()
        if wikidata:
            lines.append(f"|wikidata = {wikidata}")
        lines.extend([
            "|permission =",
            "|other versions =",
            "}}",
            location.rstrip(),
            additional_templates.rstrip(),
            "== {{int:license-header}} ==",
            session.line_edit_license.text(),
            "",
            cat_final.rstrip(),
        ])
        return "\n".join(part for part in lines if part is not None) + "\n"
