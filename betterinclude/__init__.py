from __future__ import annotations

import os

from docutils.nodes import Node
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.locale import _, __
from sphinx.util import logging
from sphinx.directives.other import Include
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import ExtensionMetadata

logger = logging.getLogger(__name__)


class BetterInclude(SphinxDirective):
    """BetterInclude

    Is a directive that really includes the referenced
    file as a copy into the doctree
    """

    required_arguments = 1

    def run(self) -> list[Node]:
        file, _ = self.get_source_info()
        path = directives.path(self.arguments[0])
        cnt = ''
        try:
            with open(os.path.join(os.path.dirname(file), path)) as i:
                cnt = i.read()
            nodes = self.parse_text_to_nodes(cnt, allow_section_headings=True)
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
