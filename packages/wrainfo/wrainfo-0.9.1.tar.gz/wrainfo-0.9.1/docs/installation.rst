============
Installation
============
.. _installation:

Using Anaconda or Miniconda (recommended)
-----------------------------------------

Using conda_ (latest version recommended), WRaINfo is installed as follows:


1. Create virtual environment for wrainfo (optional but recommended):

   .. code-block:: bash

    $ conda create -c conda-forge --name wrainfo python=3
    $ conda activate wrainfo


2. Then clone the WRaINfo source code and install WRaINfo and all dependencies from the environment_wrainfo.yml file:

   .. code-block:: bash

    $ git clone git@git.gfz-potsdam.de:fernlab/products/furuno/wrainfo.git
    $ cd wrainfo
    $ conda env update -n wrainfo -f tests/CI_docker/context/environment_wrainfo.yml
    $ pip install .


This is the preferred method to install WRaINfo, as it always installs the most recent stable release and
automatically resolves all the dependencies.


Using pip (not recommended)
---------------------------

It is also possible to install WRaINfo via `pip`_. However, please note that WRaINfo depends on some
open source packages that may cause problems when installed with pip. Therefore, we strongly recommend
to resolve the following dependencies before the pip installer is run:

    * numpy > 1.9
    * scipy > 1.0
    * wradlib > 1.15
    * xarray > 0.17
    * rioxarray = 0.12.0


Then, the pip installer can be run by:

   .. code-block:: bash

    $ pip install git@git.gfz-potsdam.de:fernlab/products/furuno/wrainfo.git

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.


Dependencies
------------

WRaINfo was not designed to be a self-contained library. Besides extensive use of xarray and :math:`\omega radlib`, 
WRaINfo uses additional libraries, which you might need to install before you can use WRaINfo depending on your system and 
installation procedure.

.. tabularcolumns:: |L|L|L|

+------------+-----------+-------------+
| Package    |    min    | recommended |
+============+===========+=============+
| numpy      | >= 1.9    | >= 1.21.0   |
+------------+-----------+-------------+
| scipy      | >= 1.0    | >= 1.7.0    |
+------------+-----------+-------------+
| wradlib    | >= 1.15.0 | >= 1.15.0   |
+------------+-----------+-------------+
| xarray     | >= 0.17   | >= 0.20.2   |
+------------+-----------+-------------+
| rioxarray  | >= 0.11.2 |  = 0.12.0   |
+------------+-----------+-------------+

You can check whether the required `Dependencies`_ are available on your computer by opening a Python console and enter:

>>> import <package_name>
ImportError: No module named <package_name>

This will be the response in case the package is not available.
In case the import is successful, you should also check the version number:

>>> package_name.__version__
some version number

The version number should be consistent with the above `Dependencies`_.


Python version
--------------

.. note::

    WRaINfo has been tested with Python 3.6+., i.e., should be fully compatible with all Python versions from 3.6 onwards.


.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _conda: https://conda.io/docs
