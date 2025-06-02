from __future__ import annotations

import glob
import os
import json
import shutil

from docutils.nodes import Node, raw
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.locale import _, __
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import ExtensionMetadata

logger = logging.getLogger(__name__)

module_dir = os.path.dirname(__file__)
assets_dir = os.path.join(module_dir, 'assets')


class UserJourney(SphinxDirective):
    """
    Directive creating user journey breadcrumb like bar.
    """
    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True

    option_spec = {
        "active-section": directives.unchanged,
        "active-subsection": directives.unchanged,
        "active-step": directives.unchanged,
        "sections": directives.unchanged,
        "subsections": directives.unchanged,
        "steps": directives.unchanged,
    }

    def _create_raw(self) -> str:

        def render_ul(list_: list, active, def_css, act_css, top_css, pre_list=None):
            result = f'<ul class="{top_css}"">\n'
            if pre_list:
                result += pre_list

            prefix = ''
            suffix = ''

            list_len = len(list_)

            if list_len > 3:
                index = list_.index(active) + 1
                index_from = max(0, index - 1)
                index_to = min(index + 1, list_len)
                iterlist = list_[index_from:index_to]
                if index_from != 0:
                    prefix = f'<li><span class="{def_css}">...</span></li>\n'
                if index_to != list_len:
                    suffix = f'<li><span class="{def_css}">...</span></li>\n'
            else:
                iterlist = list_
            result += prefix
            for item in iterlist:
                if item == active:
                    result += f'<li><span class="{act_css}">{item}</span></li>\n'
                else:
                    result += f'<li><span class="{def_css}">{item}</span></li>\n'
            result += suffix
            result += "</ul>\n"
            return result

        result = '<div class="before-userjourney"></div>'
        result += render_ul(list(self._sections.keys()), self._active_section,
                            'userjourney-level-top', 'userjourney-level-top-active', 'userjourney')

        if self._has_subsection:
            result += render_ul(self._subsections, self._active_subsection,
                                'userjourney-level-sub',
                                'userjourney-level-sub-active',
                                'userjourney userjourney-subsection',
                                pre_list='<img class="pre-userjourney-subsection"/>'
                                )

            if self._has_step:
                result += render_ul(self._steps, self._active_step, 'userjourney-level-step',
                                    'userjourney-level-step-active',
                                    'userjourney userjourney-step',
                                    pre_list='<img class="pre-userjourney-step"/>')

        return result

    def _parse_sections(self):
        self._active_section = self.options.get('active-section')
        try:
            self._sections = json.loads(self.options.get(
                'sections', '{}')) or self.env.app.config.userjourney_sections
            if not self._active_section:
                self.error('active-section needs to be set')
            if not self._active_section in self._sections.keys():
                self.error('active-section is not known')
        except json.JSONDecodeError:
            self.error('sections is not a dictionary')

    def _parse_subsections(self):
        self._active_subsection = self.options.get('active-subsection', '')
        self._has_subsection = len(self._active_subsection) > 0
        if not self._has_subsection:
            return
        if any(self.options.get('subsections', '').split(',')):
            self._subsections = [x.strip() for x in self.options.get(
                'subsections', '').split(',')]
        else:
            self._subsections = [x.strip()
                                 for x in self._sections.get(self._active_section)]
        if not self._active_subsection in self._subsections:
            self.error('active-subsection is not known')

    def _parse_steps(self):
        self._active_step = self.options.get('active-step', '')
        self._has_step = len(self._active_step) > 0
        if not self._has_step:
            return
        self._steps = [x.strip()
                       for x in self.options.get('steps', '').split(',')]
        if not self._active_step in self._steps:
            self.error('active-step is not known')

    def run(self) -> list[Node]:
        self._parse_sections()
        self._parse_subsections()
        self._parse_steps()
        return [raw('', self._create_raw(), format='html')]


def copy_asset_files(app: Sphinx, exc):
    if app.builder.format == 'html' and not exc:
        static_dir = os.path.join(app.builder.outdir, '_static')
        for file in glob.glob(assets_dir + '/*') + glob.glob(assets_dir + '/**/*'):
            if not os.path.isfile(file):
                continue
            relpath = os.path.relpath(file, assets_dir)
            targetpath = os.path.join(static_dir, relpath)
            os.makedirs(os.path.dirname(targetpath), exist_ok=True)
            shutil.copy(file, targetpath)


def setup(app: Sphinx) -> ExtensionMetadata:
    app.connect('build-finished', copy_asset_files)

    app.add_config_value('userjourney_sections', {}, False)

    directives.register_directive('userjourney', UserJourney)

    app.add_css_file('userjourney.css')

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
