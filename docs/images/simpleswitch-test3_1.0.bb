DESCRIPTION = "${@oe.utils.read_file(d.expand('${THISDIR}/${BPN}-description.txt')) or '${SUMMARY}'}"

SIMPLESWITCH_PICTURE = "file://recipes-core/images/_pictures/simpleswitch-hello-world-shell.jpg"
SIMPLESWITCH_CATEGORIES = "shell demo terminal"
