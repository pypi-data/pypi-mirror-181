Features overview
=================

Remove ground clutter
---------------------

To remove ground clutter from raw data there exists a function from :math:`\omega radlib` based on all
polarimetric variables and on a static clutter map, which is generated over a long time period.
Pixels which are identified as clutter were excluded from further processing by setting the pixels to NaN. 
For processing a clutter map, the package includes a function to read only the values from raw data sequentially to not 
overload the memory. Here is an example before and after removing ground clutter using WRaINfo.

.. image:: ../images/wr_furuno_raw_reflectivity.png
.. image:: ../images/wr_furuno_reflectivity_clutter_corrected.png


Attenuation correction
----------------------

Rainfall-induced attenuation is a major source of underestimation for radar-based precipitation estimation at X-band. 
After phase processing, the attenuation correction is used with the approach of `Testud et al. (2001) <https://www.sciencedirect.com/science/article/pii/S1464190900001155?via%3Dihub>`__ is used.
Here is an example before and after attenuation correction using WRaINfo and the differences.

.. image:: ../images/wr_furuno_reflectivity_clutter_corrected_1.png
.. image:: ../images/wr_furuno_reflectivity_attenuation_correction.png
.. image:: ../images/wr_furuno_difference_reflectivity.png


Precipitation Estimation
------------------------

There exist several methods for deriving the amount of precipitation from reflectivity. In general, 
the z - R conversion is used. The precipitation amount is determined with an integration interval (in seconds) based on the scan interval.

.. image:: ../images/wr_furuno_precipitation_amount.png


Georeferencing and gridding
---------------------------

After clutter and attenuation correction as well as precipitation estimation, the polar data are georeferenced using the specified EPSG 
code and saved as a NetCDF file. Here is an example of a georeferenced dataset.

.. image:: ../images/wr_furuno_georeferenced_reflectivity.png
