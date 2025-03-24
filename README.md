# sphinx-simpleswitch

A Sphinx extension to do some SimpleSwitch specific tasks

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

## betterinclude

is just like the standard include directive, but really injects a copy of the
referenced file into the doctree - including proper parent information.

usage

```rst
.. betterinclude:: <file to include>
```
