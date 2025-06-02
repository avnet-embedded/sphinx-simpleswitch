# sphinx-simpleswitch

A Sphinx extension to do some SimpleSwitch specific tasks

## show case

you can show case all of the directives by running

```console
python3 -m venv .env
. .env/bin/activate
pip3 install -r requirements.txt
./test-build.sh
```

the result can be viewed at `result/index.html`

The following new directives are added

## simpleswitch_containerlist

usage

```rst
.. simpleswitch_containerlist::
    :paths: <paths to simpleswitch recipe files>
    :ignore: <list of recipes to ignore>

    <template>
```

## simpleswitch_container

usage

```rst
.. simpleswitch_container::
    :name: <Name of the container>
    :file: <absolute path to the recipe>

    <template>
```

## tcmodal

renders a modal dialog with terms and conditions to be accepted before a download is enabled.

usage

usage

```rst
.. tcmodal::
    :image: <relative path to an image>
    :target: <link to the download file>
    :tc-links: <json encoded dictionary. Key = shown name, Value = link to terms and conditions page>
    :alt-text: <optional alternative text on the image - default: empty>
    :height: <optional height of the image - default: 32>
    :width: <optional width of the image - default: 32>
```

### color configuration

in your css you can override the defaults for the following color settings

- ``--tcmodal-bg-color`` - color of the blurred area
- ``--tcmodal-content-bg-color`` - modal box background color
- ``--tcmodal-content-border-color`` - modal box border color
- ``--tcmodal-content-font-color`` - modal box font color
- ``--tcmodal-content-button-bg-color`` - download button background color
- ``--tcmodal-content-button-font-color`` - download button font color

## betterinclude

is just like the standard include directive, but really injects a copy of the
referenced file into the doctree - including proper parent information.

usage

```rst
.. betterinclude:: <file to include>
```

## userjourney

is a directive to draw breadcrump bar like guides, where the user currently
is, in the entire "journey"

usage

in the configuration

```python
userjourney_sections = {
    '1': ['1.1', '1.2', '1.3'],
    '2': ['Section in 2', '2.1'],
    ...
}
```

in the doctree

```rst
.. userjourney::
  :active-section: 1
  :active-subsection: Section in 2
  :steps: Step 1, Step 2, Yet another step
  :active-step: Step 2
```

or with just the first two level

```rst
.. userjourney::
  :active-section: 1
  :active-subsection: Section in 2
```

or just the top level

```rst
.. userjourney::
  :active-section: 1
```

### color configuration

in your css you can override the defaults for the following color settings

- ``--userjourney_border_color`` - color of the border of each item
- ``--userjourney_section_bg_color`` - background color top level inactive
- ``--userjourney_section_bg_color_active`` - background color top level active
- ``--userjourney_section_txt_color`` - text color top level inactive
- ``--userjourney_section_txt_color_active`` - text color top level active
- ``--userjourney_subsection_bg_color`` - background color second level inactive
- ``--userjourney_subsection_bg_color_active`` - background color second level active
- ``--userjourney_subsection_txt_color`` - text color top 2nd level inactive
- ``--userjourney_subsection_txt_color_active`` - text color top 2nd level active
- ``--userjourney_step_bg_color`` - background color 3rd level inactive
- ``--userjourney_step_bg_color_active`` - background color 3rd level inactive
- ``--userjourney_step_txt_color`` - text color top 3rd level inactive
- ``--userjourney_step_txt_color_active`` - text color top 3rd level active

### Material icons

``userjourney`` is using [Material Icons](https://fonts.google.com/icons) licensed under ``Apache 2.0``
