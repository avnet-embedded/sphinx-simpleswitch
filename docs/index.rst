.. simpleswitch_containerlist::
    :paths: images/simpleswitch-*.bb
    :ignore: simpleswitch-test-container simpleswitch-test-container-tiny

    %header%

    %image%

    %categories%

    %description%

    %availablefor%

    %video%

    %requires%
    %recommends%

    How to get it...
    
    .. tabs::

        %tab_launcher%
        %tab_helper%
        %tab_scotty%

section a
#########

.. tcmodal::
    :image: foo.jpg
    :target: https://file-examples.com/wp-content/storage/2017/02/zip_2MB.zip
    :tc-links: {"NXP EULA": "https://github.com/Freescale/meta-freescale/blob/master/EULA", "SimpleCore EULA": "https://simple.embedded.avnet.com/stable/tools/sphinx/legal.html"}

section b
#########

+-------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| SimpleSwitch base image | Option 1                                                                                                                                                                          |  Option 2                                                                                                                                                                    |
+-------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Graphical               | .. tcmodal::                                                                                                                                                                      |   .. tcmodal::                                                                                                                                                               |
|                         |   :image: foo.jpg                                                                                                                                                                 |     :image: bar.jpg                                                                                                                                                          |
|                         |   :target: https://file-examples.com/wp-content/storage/2017/02/zip_2MB.zip                                                                                                       |     :target: https://github.com/avnet-embedded/simplecore-manifest/releases/latest/download/bundle-02_qemux86-64-simpleswitch-os-simplecore-simpleswitch-os-weston-image.bz2 |
|                         |   :tc-links: {"NXP EULA": "https://github.com/Freescale/meta-freescale/blob/master/EULA", "SimpleCore EULA": "https://simple.embedded.avnet.com/stable/tools/sphinx/legal.html"}  |     :tc-links: {"SimpleCore EULA": "https://simple.embedded.avnet.com/stable/tools/sphinx/legal.html"}                                                                       |
+-------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. toctree::
   :titlesonly:

   sub/sub/sub/other