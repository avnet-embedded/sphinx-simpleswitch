from __future__ import annotations

import base64
import glob
import gzip
from hashlib import sha1
import os
import posixpath
import sys
import textwrap
from typing import ClassVar

import requests
from docutils.nodes import Node
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.locale import _, __
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import ExtensionMetadata, OptionSpec
from oelint_parser.cls_stash import Stash

from sphinx.writers.html5 import HTML5Translator
from sphinx.writers.latex import LaTeXTranslator
from sphinx.writers.texinfo import TexinfoTranslator

from m2r2 import convert
from jinja2 import Environment

logger = logging.getLogger(__name__)


def _get_data(config):
    url = f'{config.simpleswitch_launcher_url}/data.json'
    resp = requests.get(url=url)
    return resp.json()


class SimpleSwitchContainer(SphinxDirective):
    """
    Directive for a list of names.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec: ClassVar[OptionSpec] = {
        "name": directives.unchanged,
        "file": directives.unchanged,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._repmap = {
            '%availablefor%': self.__availableFor,
            '%categories%': self.__categories,
            '%summary%': self.__summary,
            '%description%': self.__description,
            '%header%': self.__heading,
            '%image%': self.__image,
            '%recommends%': self.__recommends,
            '%requires%': self.__requires,
            '%tab_helper%': self.__tab_by_helper,
            '%tab_launcher%': self.__tab_by_launcher,
            '%tab_scotty%': self.__tab_by_scotty,
            '%video%': self.__video,
        }

    def __heading(self, data, indent) -> str:
        res = f'{data["name"]}\n'
        res += '"'*len(data['name'])
        return textwrap.indent(res, ' ' * indent).lstrip()

    def __description(self, data, indent) -> str:
        desc = data.get('description', '').replace('!!!inlineblock!!!', '')
        jinja_env = Environment(trim_blocks=True, lstrip_blocks=True)

        res = jinja_env.from_string(desc).render(
            web=True
        )
        return textwrap.indent(convert(textwrap.dedent(res)), ' ' * indent).lstrip()

    def __summary(self, data, indent) -> str:
        return textwrap.indent(data.get('summary', ''), ' ' * indent).lstrip()

    def __tab_by_launcher(self, data, indent) -> str:
        if data.get('local', True):
            return ''
        res = '.. tab:: with SimpleSwitch Launcher\n\n'
        res += f'    .. button-link:: {self.config.simpleswitch_launcher_url}/?showItem={data["name"]}\n'
        res += f'        :color: info\n\n'
        res += f'        See in Launcher'
        return textwrap.indent(res, ' ' * indent).lstrip()

    def __tab_by_helper(self, data, indent) -> str:
        if data.get('local', True):
            return ''
        version = 'latest'
        if len(data.get('versions', [])) > 1:
            version = '$RELEASE_VERSION'
        res = textwrap.dedent(f'''
        .. code-tab:: console
            :caption: with container-helper

                ## From the base image run
                $ skopeo login ghcr.io
                $ container-helper --tag={version} ghcr.io/{self.config.simpleswitch_github_org}/simpleswitch/$CONTAINER_HELPER_ARCH/{data["name"]}
                $ simpleswitch-helper start {data["name"]}
        ''')
        return textwrap.indent(res, ' ' * indent).lstrip()

    def __tab_by_scotty(self, data, indent) -> str:
        res = textwrap.dedent(f'''
        .. code-tab:: console
            :caption: with Scotty

                ## On your computer run
                $ scotty build {data["name"]}
        ''')
        return textwrap.indent(res, ' ' * indent).lstrip()

    def __video(self, data, indent) -> str:
        res = ''
        if data.get('video', ''):
            res += f'..  youtube:: {data["video"].replace("https://youtu.be/", "", 1)}\n'
        return textwrap.indent(res, ' ' * indent).lstrip()

    def __categories(self, data, indent) -> str:
        if not data.get('categories', []):
            return ''
        res = ':bdg-primary-line:`Categories`\n'
        res += ' '.join(f':bdg-primary:`{x}`' for x in sorted(data.get(
            'categories', [])))
        return textwrap.indent(res, ' ' * indent).lstrip()

    def __availableFor(self, data, indent) -> str:
        if not data.get('arch', []):
            return ''
        res = ':bdg-success-line:`Available for`\n'
        res += ' '.join(
            f':bdg-success:`{x}`' for x in sorted(data.get('arch', [])))
        return textwrap.indent(res, ' ' * indent).lstrip()

    def __requires(self, data, indent) -> str:
        if not data.get('dependencies.mandatory', []):
            return ''
        res = ':bdg-info-line:`Required SimpleSwitch packages`\n'
        res += ' '.join(f':bdg-info:`{x}`' for x in sorted(data.get(
            'dependencies.mandatory', [])))
        return textwrap.indent(res, ' ' * indent).lstrip()

    def __recommends(self, data, indent) -> str:
        if not data.get('dependencies.recommended', []):
            return ''
        res = ':bdg-black-line:`Recommended SimpleSwitch packages`\n'
        res += ' '.join(f':bdg-black:`{x}`' for x in sorted(data.get(
            'dependencies.recommended', [])))
        return textwrap.indent(res, ' ' * indent).lstrip()

    def __image(self, data, indent) -> str:
        res = ''
        if data.get('picture', ''):
            image = base64.b64decode(data["picture"].encode())
            image = gzip.decompress(image)
            image = base64.b64encode(image).decode('utf-8')
            res += '.. raw:: html\n\n'
            res += f'    <img src="data:image/jpeg;base64,{image}" />\n'
        return textwrap.indent(res, ' ' * indent).lstrip()

    def __extract_from_recipe(self, file):
        def extract(_stash, var):
            res = _stash.ExpandTerm(file, f'${{{var}}}') or ''
            res = res.replace(f'${{{var}}}', '')
            res = res.replace('\x1b', '')
            return textwrap.dedent(res)

        data = {}
        _stash = Stash(quiet=True)
        _stash.AddFile(file)
        data['description'] = extract(_stash, 'DESCRIPTION')
        data['summary'] = extract(_stash, 'SUMMARY')
        if not data['description']:
            data['description'] = data['summary'] or ''
        data['categories'] = [x for x in extract(
            _stash, 'SIMPLESWITCH_CATEGORIES').split(' ') if x]
        return data

    def run(self) -> list[Node]:
        name = self.options.get('name')
        file = self.options.get('file')

        _simpleswitch_data = _get_data(self.config)

        _lines = []
        _first_line_found = False
        for line in self.block_text.splitlines():
            _first_line_found |= not line.strip()
            if _first_line_found:
                _lines.append(line)

        data = {}

        if name in _simpleswitch_data:
            data = {**_simpleswitch_data[name],
                    'local': False,
                    'name': name}
        else:
            data = {**self.__extract_from_recipe(file),
                    'local': True,
                    'name': name}

        for k, v in self._repmap.items():
            for index, line in enumerate(_lines):
                if k in line:
                    indent = len(line) - len(line.lstrip())
                    _lines[index] = line.replace(k, v(data, indent))

        _result = textwrap.dedent('\n'.join(_lines))

        logger.debug(_result)

        children = self.parse_text_to_nodes(
            _result, allow_section_headings=True)
        return [*children]


class SimpleSwitchContainerList(SphinxDirective):
    """
    Directive for a list of names.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False

    option_spec = {
        "paths": directives.unchanged,
        "ignore": directives.unchanged
    }

    def run(self) -> list[Node]:
        _paths = [x for x in (self.options.get('paths') or '').split(' ') if x]
        _ignore = [x for x in (self.options.get(
            'ignore') or '').split(' ') if x]
        if not _paths:
            self.error('At least one path must be defined')

        self._template = ''
        _first_line_found = False
        for line in self.block_text.splitlines():
            _first_line_found |= not line.strip()
            if _first_line_found:
                self._template += line + '\n'

        _location, _ = self.get_source_info()
        _search_paths = [os.path.dirname(_location)] + sys.path

        items = []
        for path in _paths:
            for searchpath in _search_paths:
                _globs = glob.glob(os.path.join(searchpath, path))
                for item in _globs:
                    name, _ = os.path.splitext(os.path.basename(item))
                    name = name[::-1].replace('_1.0'[::-1], '', 1)[::-1]
                    if name not in _ignore:
                        items.append((name, os.path.abspath(item)))
                if _globs:
                    continue

        self._result = ''
        seen = []
        for item in sorted(items, key=lambda tup: tup[0]):
            if item[0] in seen:
                continue
            seen.append(item[0])
            logger.info(f'Adding {item[0]}:{item[1]}')
            self._result += f'.. simpleswitch_container::\n'
            self._result += f'    :name: {item[0]}\n'
            self._result += f'    :file: {item[1]}\n\n'
            self._result += f'    {self._template}\n\n'

        children = []
        children = self.parse_text_to_nodes(
            self._result, allow_section_headings=True)
        return [*children]


def setup(app: Sphinx) -> ExtensionMetadata:
    directives.register_directive(
        'simpleswitch_containerlist', SimpleSwitchContainerList)
    directives.register_directive(
        'simpleswitch_container', SimpleSwitchContainer)

    app.add_config_value('simpleswitch_github_org', 'avnet-embedded', 'html')
    app.add_config_value('simpleswitch_launcher_url',
                         'https://avnet-embedded.github.io/simpleswitch-launcher-web/', 'html')

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
