Getting started with WRaINfo
============================


Import WRaINfo
--------------

To use WRaINfo in a project::

    import wrainfo

----

Check the version
*****************

Check the version of WRaINfo::

    print(wrainfo.__version__)

----

Command line utilities
**********************

wrainfo_cli.py
--------------

At the command line, WRaINfo provides the **wrainfo_cli.py** command:

.. argparse::
   :filename: ./../bin/wrainfo_cli.py
   :func: get_argparser
   :prog: wrainfo_cli.py
