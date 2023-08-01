############
Installation
############


Vitis AI PyTorch and Tensorflow Quantizer, which is part of the Vitis AI toolchain, requires the installation of a Docker container on the host server.

Host Server Requirement
~~~~~~~~~~~~~~~~~~~~~~~

The Vitis AI Docker container can be installed on Ubuntu 20.04, CentOS 7.8, 7.9, 8.1, and RHEL 8.3, 8.4. The developers working on Windows 11 can use `WSL <https://learn.microsoft.com/en-us/windows/wsl/install>`_ for installing Vitis AI docker. 


Docker Container Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Multiple versions of the Docker container are available, each tailored to specific frameworks. Please follow the docker download and running instructions as per the following links 

.. list-table:: 
   :widths: 25 25 
   :header-rows: 1

   * - Framework
     - Docker location
   * - PyTorch
     - https://hub.docker.com/r/amdih/ryzen-ai-pytorch
   * - Tensorflow 2
     - https://hub.docker.com/r/amdih/ryzen-ai-tensorflow2
   * - Tensorflow 1
     - https://hub.docker.com/r/amdih/ryzen-ai-tensorflow 


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
