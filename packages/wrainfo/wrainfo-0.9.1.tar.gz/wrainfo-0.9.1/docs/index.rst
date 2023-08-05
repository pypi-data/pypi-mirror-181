WRaINfo: An Open Source Library for Weather Radar Information
=============================================================

WRaINfo is a software to process FURUNO weather radar data.
The FURUNO raw data can already provide useful visual information about the
spatial distribution of precipitation events. But in order to use the FURUNO
data for quantitative studies, the raw data have to be processed in order to account
for typical error sources such as ground clutter, uncertainties in polarimetric
variables and in the z-R relationship as well as attenuation of the radar signal.
Therefore, this python package has been developed for processing FURUNO weather radar
data.

.. note::

    The WRaINfo package was only tested for the weather radar type WR2120 and WR2100 of FURUNO.


.. note::

    * Please cite the WRaINfo as Künzel, A., Mühlbauer, K., Neelmeijer, J., Spengler, D. (2022, October 18). WRaINfo - An open source library for weather radar information (Version 0.8.3). Zenodo. https://doi.org/10.5281/zenodo.7220833
    * Please cite also the :math:`\omega radlib` python package as *Heistermann, M., Jacobi, S., and Pfaff, T.: Technical Note: An open source library for processing weather radar data (wradlib), Hydrol. Earth Syst. Sci., 17, 863-871,* doi:`10.5194/hess-17-863-2013, 2013 <https://hess.copernicus.org/articles/17/863/2013/hess-17-863-2013.pdf>`_


Package status
--------------

.. image:: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo/badges/main/pipeline.svg
        :target: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo/pipelines
        :alt: Pipelines
.. image:: https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo/badges/main/coverage.svg
        :target: https://fernlab.git-pages.gfz-potsdam.de/products/furuno/wrainfo/coverage/
        :alt: Coverage


Documentation
-------------

**Getting started**

* :doc:`installation`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Getting started

   installation

**Tutorials & Examples**

* :doc:`tutorials_and_examples/tutorials_and_examples`
* :doc:`tutorials_and_examples/reader_module`
* :doc:`tutorials_and_examples/data_input`
* :doc:`tutorials_and_examples/clutter_detection_module`
* :doc:`tutorials_and_examples/attenuation_correction_module`
* :doc:`tutorials_and_examples/precipitation_estimation_module`
* :doc:`tutorials_and_examples/geometry_module`
* :doc:`tutorials_and_examples/further_features`


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Tutorials & Examples

   tutorials_and_examples/tutorials_and_examples
   tutorials_and_examples/reader_module
   tutorials_and_examples/data_input
   tutorials_and_examples/clutter_detection_module
   tutorials_and_examples/attenuation_correction_module
   tutorials_and_examples/precipitation_estimation_module
   tutorials_and_examples/geometry_module
   tutorials_and_examples/further_features

**Process chains**

* :doc:`process_chains/introduction`
* :doc:`process_chains/clutter_chain`
* :doc:`process_chains/static_cmap`
* :doc:`process_chains/wr_routine_furuno_level2a`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Process chains

   process_chains/introduction
   process_chains/clutter_chain
   process_chains/static_cmap
   process_chains/wr_routine_furuno_level2a

**Help & References**

* :doc:`modules`
* :doc:`contributing`
* :doc:`authors`
* :doc:`history`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Help & References

   modules
   contributing
   authors
   history
   Source code repository <https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo>


License
-------

Licensed under the Apache License, Version 2.0

Credits
-------

.. |FERNLOGO| image:: /images/fernlab_logo.png
  :width: 10 %

.. list-table::
    :class: borderless

    * - |FERNLOGO|

      - WRaINfo has been developed by `FERN.Lab <https://fernlab.gfz-potsdam.de/>`_,
	  the Helmholtz Innovation Lab "Remote sensing for sustainable use of resources", located
	  at the `Helmholtz Centre Potsdam, GFZ German Research Centre for Geosciences <https://www.gfz-potsdam.de/en/>`_.
	  FERN.Lab is funded by the `Initiative and Networking Fund of the Helmholtz Association <https://www.helmholtz.de/en/about-us/structure-and-governance/initiating-and-networking/>`_.


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

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
