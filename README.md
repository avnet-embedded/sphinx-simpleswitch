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
