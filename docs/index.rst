User journey full

.. userjourney::
  :active-section: base image
  :active-subsection: Setup HW
  :steps: Download, Flash, Configure hardware
  :active-step: Download

User journey full autowrap

.. tabs::

  .. tab:: 1

    .. userjourney::
      :active-section: base image
      :active-subsection: Setup HW
      :steps: 1, 2, 3, 4, 5, 6
      :active-step: 1

  .. tab:: 2

    .. userjourney::
      :active-section: base image
      :active-subsection: Setup HW
      :steps: 1, 2, 3, 4, 5, 6
      :active-step: 2

  .. tab:: 3

    .. userjourney::
      :active-section: base image
      :active-subsection: Setup HW
      :steps: 1, 2, 3, 4, 5, 6
      :active-step: 3

  .. tab:: 4

      .. userjourney::
        :active-section: base image
        :active-subsection: Setup HW
        :steps: 1, 2, 3, 4, 5, 6
        :active-step: 4

  .. tab:: 5

      .. userjourney::
        :active-section: base image
        :active-subsection: Setup HW
        :steps: 1, 2, 3, 4, 5, 6
        :active-step: 5

  .. tab:: 6

      .. userjourney::
        :active-section: base image
        :active-subsection: Setup HW
        :steps: 1, 2, 3, 4, 5, 6
        :active-step: 6

User journey full #2

.. userjourney::
  :active-section: base image
  :active-subsection: Setup HW
  :steps: Download, Flash, Configure hardware
  :active-step: Flash

User journey subsections

.. userjourney::
  :active-section: base image
  :active-subsection: Setup HW

User journey top level only

.. userjourney::
  :active-section: base image

Some text

.. tabs::

  .. tab:: Test tab

  .. tab:: Test tab 2
  
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

section c
#########

.. betterinclude:: inc/test.inc

.. toctree::
   :titlesonly:

   sub/sub/sub/other