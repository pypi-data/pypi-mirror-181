.. figure:: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo/-/raw/main/docs/images/wrainfo_logo.png
    :target: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo
    :align: center


==============================================================
WRaINfo - An Open Source Library for Weather Radar Information
==============================================================

is a software for real-time weather radar data processing. It is specifically designed for X-band weather radars of FURUNO.

.. image:: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo/badges/main/pipeline.svg
        :target: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo/pipelines
.. image:: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo/badges/main/coverage.svg
        :target: https://fernlab.git-pages.gfz-potsdam.de/products/furuno/wrainfo/coverage/
.. image:: https://img.shields.io/static/v1?label=Documentation&message=GitLab%20Pages&color=orange
        :target: https://fernlab.git-pages.gfz-potsdam.de/products/furuno/wrainfo/doc/
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.7220833.svg
        :target: https://doi.org/10.5281/zenodo.7220833

For detailed information, refer to the `documentation <https://fernlab.git-pages.gfz-potsdam.de/products/furuno/wrainfo/doc/>`_.
See also the latest coverage_ report and the pytest_ HTML report.

* **Contact**: Alice Künzel (alicek@gfz-potsdam.de)
* Information on how to **cite the WRaINfo Python package** can be found in the `CITATION <CITATION.rst>`__ file.
* Please **cite also the Wradlib Python package** as follows:
	An Open Source Library for Weather Radar Data Processing
	Heistermann, M., Jacobi, S., and Pfaff, T.: Technical Note: An open source library for processing weather
	radar data (wradlib), Hydrol. Earth Syst. Sci., 17, 863-871, doi:10.5194/hess-17-863-2013, 2013


.. contents:: Table of Contents
   :depth: 2

=================
Features overview
=================

The FURUNO raw data can already provide useful visual information about the
spatial distribution of precipitation events. But in order to use the FURUNO
data for quantitatvie studies, the raw data has to be processed in order to account
for typical error sources such as ground clutter, uncertainities in polarimetric
variables and in the z-R relationship as well as attenuation of the radar signal.
Therefore this python package has been developed for processing FURUNO weather radar
data.


Remove ground clutter
---------------------

To remove ground clutter from raw data exists a function from :math:`\omega radlib` based on all
polarimetric variables and on a static clutter map, which is generated over a long time period.
Pixel which are identified as clutter were exclude from further processing by set the pixels to NaN.
For processing a clutter map, the package includes a function to read only the values from raw data sequentially to not overload the memory.
Here is an example before and after removing ground clutter using WRaINfo.

.. figure:: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo/-/raw/main/docs/images/wr_furuno_raw_reflectivity.png
    :target: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo
	:width: 80 %
.. figure:: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo/-/raw/main/docs/images/wr_furuno_reflectivity_clutter_corrected.png
    :target: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo
	:width: 80 %


Attenuation correction
----------------------

Rainfall-induced attenuation is a major source of underestimation for radar-based precipitation estimation at X-band.
After phase processing, the attenuation correction is used with the approach of `Testud et al. (2001) <https://www.sciencedirect.com/science/article/pii/S1464190900001155?via%3Dihub>`__ is used.
Here is an example before and after attenuation correction using WRaINfo and the differences.

.. figure:: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo/-/raw/main/docs/images/wr_furuno_reflectivity_clutter_corrected_1.png
    :target: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo
    :width: 50 %
.. figure:: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo/-/raw/main/docs/images/wr_furuno_reflectivity_attenuation_correction.png
    :target: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo
    :width: 50 %
.. figure:: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo/-/raw/main/docs/images/wr_furuno_difference_reflectivity.png
    :target: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo
    :width: 50 %


Precipitation Estimation
------------------------

There are several methods for deriving the amount of precipitation from reflectivity. In general, the z - R conversion is used.
The precipitation amount is determined with an integration interval of seconds based on the scan interval.

.. figure:: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo/-/raw/main/docs/images/wr_furuno_precipitation_amount.png
    :target: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo
    :width: 80 %
    :align: center


Georeferencing and gridding
---------------------------

After clutter and attenuation correction and precipitation estimation, the polar data are georeferenced using the specified EPSG code
and saved as a NetCDF file. Here is an example of a georeferenced dataset.

.. figure:: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo/-/raw/main/docs/images/wr_furuno_georeferenced_reflectivity.png
    :target: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo
    :width: 30 %


============
Installation
============

`Install <https://fernlab.git-pages.gfz-potsdam.de/products/furuno/wrainfo/doc/installation.html>`_ wrainfo

===================
History / Changelog
===================

You can find the protocol of recent changes in the WRaINfo package
`here <HISTORY.rst>`__.

=======
License
=======

The software is available under the `Apache 2.0 <LICENSE/>`_.

============
Contribution
============

`Contributions <https://fernlab.git-pages.gfz-potsdam.de/products/furuno/wrainfo/doc/contributing.html>`__ are always welcome.

=================
Data availability
=================

Preprocessed FURUNO weather radar data (level 2a) for the Neubrandenburg site are made available in the `TERENO Data DiscoveryPortal <https://ddp.tereno.net/ddp/>`__
under the `CC BY-NC 4.0 license <https://creativecommons.org/licenses/by-nc/4.0/>`__.
Please contact us (fernlab@gfz-potsdam.de), if you wish to use the data under another license (e.g. commercially).

========
Credits
========

.. |FERNLOGO| image:: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo/-/raw/main/docs/images/fernlab_logo.png
    :width: 10 %

.. list-table::
    :class: borderless

    * - |FERNLOGO|

      - WRaINfo has been developed by `FERN.Lab <https://fernlab.gfz-potsdam.de/>`_, the Helmholtz Innovation Lab "Remote sensing for sustainable use of resources", located at the `Helmholtz Centre Potsdam, GFZ German Research Centre for Geosciences <https://www.gfz-potsdam.de/en/>`_. FERN.Lab is funded by the `Initiative and Networking Fund of the Helmholtz Association <https://www.helmholtz.de/en/about-us/structure-and-governance/initiating-and-networking/>`_.


Development Team:
 - Alice Künzel, researcher
   *Helmholtz Centre Potsdam German Research Centre for Geosciences GFZ, Section 1.4 - Remote Sensing and Geoinformatics*
 - Kai Mühlbauer, researcher
   *University of Bonn, Institute of Geosciences - Meteorology Section*
 - Julia Neelmeijer, supervisor
   *Helmholtz Centre Potsdam German Research Centre for Geosciences GFZ, Section 1.4 - Remote Sensing and Geoinformatics*
 - Daniel Spengler, supervisor
   *Helmholtz Centre Potsdam German Research Centre for Geosciences GFZ, Section 1.4 - Remote Sensing and Geoinformatics*

This package was created with Cookiecutter_ and the `fernlab/cookiecutter-pypackage`_ project template.
The test data represent raw data of the weather radar FURUNO and files which are created with the WRaINfo package.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`fernlab/cookiecutter-pypackage`: https://github.com/fernlab/cookiecutter-pypackage
.. _coverage: https://fernlab.git-pages.gfz-potsdam.de/products/furuno/wrainfo/coverage/
.. _pytest: https://fernlab.git-pages.gfz-potsdam.de/products/furuno/wrainfo/test_reports/report.html
