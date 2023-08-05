Introduction
============

WRaINfo contains the module "process_chains", which is based on the modules "reader", "clutter detection", "attenuation_correction", 
"precipitation estimation" and "geometry". 

The module process_chains shows how the operational mode can be set up to process the raw data of the FURUNO weather radar and subsequently 
generate georeferenced precipitation products with a temporal resolution of 5 minutes.
In this chapter, the individual process chains and the respective parameters of the process chains are described in detail. However, 
there are no examples of the individual process chains. The functionality of the process chains is ensured by means of tests in a CI pipeline in 
GitLab. In addition, the individual steps of the process chains were explained using examples in the "Tutorials & Examples" chapter.