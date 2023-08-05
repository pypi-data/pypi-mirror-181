=======
History
=======

0.9.1 (2022-12-12)
------------------

Test:

* add test for reader module

Bugs:

* fixed bug in wrainfo.reader.get_cmap()
* minor revision of wrainfo.reader.read_single_file()
* minor revision of wrainfo.clutter.fuzzy_echo_classification()
* minor revision of wrainfo.geometry.furuno_sweep_to_netcdf()

0.9.0 (2022-12-06)
------------------

New features:

* add a function to read multiple files

General settings:

* delete images
* revision of the configuration file

Publication:

* revision of .gitlab-ci.yml file because of a second release on zenodo
* revision of AUTHORS and CITATION file
* add badge for zenodo release

Documentation:

* revision of the index file

Bugs:

* fixed bug in reader module
* minor revision of the clutter module
* minor revision of precipitation module
* minor revision of geometry module

0.8.3 (2022-10-18)
------------------

General settings:

* repair links of images for PyPi

Publication:

* revision of the citation file
* add codemeta file
* add CI job to create release on zenodo

Bugs:

* fixed bug for upload to zenodo


0.8.2 (2022-10-13)
------------------

General settings:

* repair links of images for PyPi
* define project links and keywords for PyPi


0.8.1 (2022-10-10)
------------------

General settings:

* revision of the readme file
* revision of the documentation on GitLab pages

Publication:

* add Citation file
* add .zenodo.json file
* add .gitattributes - file
* add CI job to create release on Zenodo sandbox
* add CI job to create release on PyPi

0.8.0 (2022-09-29)
------------------

General settings:

* revision of the readme file
* add file gfz_software_dissemination
* add FERN.Lab Logo
* exclude an URL from URL Checker
* revision of the already existing documentation


0.7.3 (2022-09-22)
------------------

Test:

* write test for process chains module


0.7.2 (2022-09-20)
------------------

Documentation:

* revision of the already existing documentation


0.7.1 (2022-09-19)
------------------

Documentation:

* write the documentation for process chains module

Bugs:

* fixed bug in process chains module


0.7.0 (2022-09-16)
------------------

Bugs:

* fixed bug in geometry module
* fixed bug in compression module

Test:

* write tests for geometry module
* write tests for compression module
* write tests for error filelist module

Documentation:

* write the documentation for geometry module
* write documentation for compression module
* write documentation for error filelist module
* revision of the already existing documentation

General settings:

* add version for rioxarray in dependencies


0.6.0 (2022-09-14)
------------------

Test:

* write tests for geometry module

General settings:

* add dependencies to the package


0.5.5 (2022-09-11)
------------------

Test:

* write tests for attenuation correction and precipitation module
* add test function in reader_test.py

General settings:

* rename a function in compression module


0.5.4 (2022-09-09)
------------------

Test:

* write tests for clutter module


0.5.3 (2022-08-27)
------------------

Documentation:

* write the documentation for the precipitation estimation module


0.5.2 (2022-08-26)
------------------

Bugs:

* fixed bug in reader test module
* fixed bug of install urlchecker (now use previous version)
* fixed bug of install xarray (now use complete package and previous version)


0.5.1 (2022-08-24)
------------------

Bugs:

* fixed bug in get_cmap function: now get a cmap for a specific elevation angle

Documentation:

* write the documentation for the attenuation correction module


0.5.0 (2022-08-21)
------------------


Bugs:

* fixed bug in get_cmap function: now get a cmap for a specific elevation angle
* fixed bug in dbzh_no_clutter function

Documentation:

* write the documentation for the clutter module

General settings:

* revision of the structure from GitLab pages


0.4.1 (2022-08-17)
------------------

Documentation:

* write the documentation for the reader module
* revision of the already existing documentation

General settings:

* update dependencies in setup.py and gitlab-ci.yml
* add test jupyter notebooks to gitignore file


0.4.0 (2022-08-15)
------------------

Documentation:

* write the documentation for reading FURUNO data with WRaINfo

General settings:

* add configurations to the settings of setup.py and docker gitlab-ci.yml to add jupyter notebooks to GitLab pages


0.3.2 (2022-08-11)
------------------

General settings:

* update the documentation of the package on GitLab pages
* minor revisions of the description in 2 python modules
* minor revision of the README file
* minor revision of the .gitlab-ci.yml file


0.3.1 (2022-08-10)
------------------

General settings:

* add dependencies to docker in test directory
* add an expression to the .gitlab-ci.yml file
* revision of the source code style
* revision of the CITATION file
* revision of the README file


0.3.0 (2022-08-07)
------------------

Bugs:

* fixed bugs in the source code discovered through pipeline

General settings:

* add test data to the package


0.2.1 (2022-08-05)
------------------

General settings:

* add contributors to the AUTHORS file
* revision of the source code style


0.2.0 (2022-08-04)
------------------

General settings:

* modified the README file
* add source code to the package
* modified settings of the package


0.1.0 (2022-08-02)
------------------

General settings:

* Package skeleton as created by https://github.com/danschef/cookiecutter-pypackage.
