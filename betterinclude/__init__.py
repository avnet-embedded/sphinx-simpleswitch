from __future__ import annotations

import os

from docutils.nodes import Element, Node
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.locale import _, __
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx.util.parsing import (_fresh_title_style_context,
                                 _text_to_string_list)
from sphinx.util.typing import ExtensionMetadata

logger = logging.getLogger(__name__)


class BetterInclude(SphinxDirective):
    """BetterInclude

    Is a directive that really includes the referenced
    file as a copy into the doctree
    """

    required_arguments = 1

    def _parse_nested(self, state, text, source, allow_section_headings):
        """This is a modified version of parse_text_to_nodes

        which allows us to define the source of the subnodes
        """
        document = state.document
        content = _text_to_string_list(
            text, source=source, tab_width=document.settings.tab_width
        )
        node = Element()  # Anonymous container for parsing
        node.document = document

        with _fresh_title_style_context(state):
            state.nested_parse(
                content, 0, node, match_titles=allow_section_headings
            )
        return node.children

    def run(self) -> list[Node]:
        file, _ = self.get_source_info()
        path = directives.path(self.arguments[0])
        cnt = ''
        try:
            with open(os.path.join(os.path.dirname(file), path)) as i:
                cnt = i.read()
            nodes = self._parse_nested(
                self.state, cnt, source=file, allow_section_headings=True)
            for node in nodes:
                self.set_source_info(node)
            return nodes
        except FileNotFoundError:
            self.error(f'{path} is not accessible')
            return []


def setup(app: Sphinx) -> ExtensionMetadata:
    directives.register_directive('betterinclude', BetterInclude)

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
