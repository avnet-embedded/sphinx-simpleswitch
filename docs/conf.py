# -- Path cleanup ------------------------------------------------------------

# static project config
project = 'Test'
copyright = '2024, Avnet Embedded GmbH'

# -- Project information -----------------------------------------------------
release = '1.0.0'
# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.graphviz',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx_code_tabs',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinx_userjourney_bar',
    'sphinx_toolbox.collapse',
    'sphinxcontrib.jquery',
    'sphinxcontrib.programoutput',
    'sphinxcontrib.youtube',
    'sphinx_simpleswitch',
    'sphinx_tcmodal',
    'betterinclude',
]

# enable embedded of sphinx directives from markdown
myst_enable_extensions = [
    "colon_fence",
]

intersphinx_mapping = {
    'yocto': ('https://docs.yoctoproject.org/kirkstone/', None)
}

# spelling settings
spelling_show_suggestions = True
spelling_warning = True
spelling_ignore_contributor_names = False

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_show_sourcelink = False
html_theme = 'pydata_sphinx_theme'

html_context = {
    "default_mode": "light"
}

html_theme_options = {
    "check_switcher": False,
    "navbar_align": "left",
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
}

primary_domain = 'rst'

# Todo configuration
todo_include_todos = True

# code copy config
copybutton_exclude = '.linenos, .gp, .go'
copybutton_copy_empty_lines = False

# Autosectionlabel configuration
# Prefix auto generated labels with document name, to avoid conflicts
autosectionlabel_prefix_document = True

# enable auto link generation for markdown
myst_heading_anchors = 3

userjourney_sections = {
    'base image': ['Setup HW', 'Setup SW', 'Premade'],
    'sdk': [],
    'yocto': [],
    'production': []
}
userjourney_section_bg_color = "#001F63"
userjourney_section_bg_color_active = "#FF00A3"
userjourney_section_txt_color = "white"
userjourney_section_txt_color_active = "black"
userjourney_step_bg_color = "#00A1BE"
userjourney_step_bg_color_active = "#C8C9C7"
userjourney_step_txt_color = "black"
userjourney_step_txt_color_active = "black"
userjourney_subsection_bg_color = "#97999B"
userjourney_subsection_bg_color_active = "#53565A"
userjourney_subsection_txt_color = "black"
userjourney_subsection_txt_color_active = "white"
