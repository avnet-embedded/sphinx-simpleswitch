from __future__ import annotations

import glob
from hashlib import sha1
import os
import shutil
import json

from docutils.nodes import Node, raw
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.locale import _, __
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import ExtensionMetadata
from sphinx.util.fileutil import copy_asset
from sphinx.util.osutil import ensuredir

logger = logging.getLogger(__name__)

module_dir = os.path.dirname(__file__)
assets_dir = os.path.join(module_dir, 'assets')

_tcmodal_counter = 0

class TermsAndConditionsModal(SphinxDirective):
    """
    Directive creating a modal T&C acceptance dialog.
    """
    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True

    option_spec = {
        "alt-text": directives.unchanged(""),
        "height": directives.unchanged("32"),
        "image": directives.unchanged_required,
        "target": directives.unchanged_required,
        "tc-links": directives.unchanged_required,
        "width": directives.unchanged("32"),
    }

    def _create_raw(self) -> str:
        tc_boxes = ''

        for name, link in self._tclinks.items():

            _id = self._id + '-' + sha1(link.encode()).hexdigest()
            tc_boxes += f'''
                <div>
                    <input id="checkbox-{_id}" type="checkbox" onchange="tcmodal_eval(\'{self._id}\')">
                    <label for="checkbox-{_id}"><a href="{link}" target="_blank">I read and I agree to {name}</a></label>
                <div>
            '''
        img_path = os.path.join(
            self._docrelpath, '_images', os.path.basename(self._image))
        result = f'''
        <img width="{self._width}" height="{self._height}" src="{img_path}" alt="{self._alttext}" onclick="tcmodal(\'{self._id}\')">
        <div id="{self._id}" class="tcmodal">
            <div class="tcmodal-content">
                <strong>
                    Before downloading you need to accept the following
                    Terms and Conditions, listed below
                </strong>
                <br/>
                <button type="button" disabled id="button-{self._id}" onclick="window.open(\'{self._target}\')">Download</button>
                <br/>
                {tc_boxes}
                <br/>
            </div>
        </div>
        '''
        return result

    def run(self) -> list[Node]:
        global _tcmodal_counter
        env = self.state.document.settings.env

        _tcmodal_counter += 1
        file, line = self.get_source_info()
        self._docrelpath = os.path.relpath(env.tcmodal_root_path, os.path.dirname(file))

        loc_info = f'{file}-{line}-{_tcmodal_counter}'
        self._id = sha1(loc_info.encode()).hexdigest()
        try:
            self._tclinks = json.loads(self.options.get('tc-links') or '{}')
        except json.JSONDecodeError:
            logger.error('tc-links is not a valid json')
            self._tclinks = {}
        self._width = self.options.get('width') or "32"
        self._height = self.options.get('height') or "32"
        self._alttext = self.options.get('alt-text') or ""
        self._target = self.options.get('target')
        self._image = self.options.get('image')

        if not self._image:
            raise Exception('image is missing')

        fullpath = os.path.join(os.path.dirname(file), self._image)
        env.tcmodal_image_files[fullpath] = fullpath
        self.env.app.emit('env-updated', env)
        rawsource = self._create_raw()
        return [raw('', rawsource, format='html')]


def copy_asset_files(app: Sphinx, exc):
    if app.builder.format == 'html' and not exc:
        static_dir = os.path.join(app.builder.outdir, '_static')
        for file in glob.glob(assets_dir + '/*'):
            copy_asset(file, static_dir, force=True)

def install_static_files(app, env):
    images_dir = os.path.join(app.builder.outdir, '_images')
    ensuredir(images_dir)

    for image in env.tcmodal_image_files.values():
        if not os.path.exists(image):
            logger.warning(f'{image} does not exist')
            continue
        _targetpath = os.path.join(images_dir, os.path.basename(image))
        logger.info(f'Exporting {image} to {_targetpath}')
        if os.path.exists(_targetpath):
            os.remove(_targetpath)
        shutil.copy(image, _targetpath)

def builder_init_hook(app: Sphinx):
    app.env.tcmodal_root_path = app.builder.srcdir
    app.env.tcmodal_image_files = {}
                                
def setup(app: Sphinx) -> ExtensionMetadata:
    app.connect('build-finished', copy_asset_files)
    app.connect('builder-inited', builder_init_hook)
    app.connect('env-updated', install_static_files)

    directives.register_directive('tcmodal', TermsAndConditionsModal)

    app.add_js_file('tcmodal.js')
    app.add_css_file('tcmodal.css')

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
