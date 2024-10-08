#############################
Additional Quantization Setup 
#############################

.. note::
   The Vitis AI Quantizer has been deprecated as of the Ryzen AI 3.0 release. Users are strongly recommended to use the new Quantizer Quark (please refer to the main Quantization documentation).

The Vitis AI PyTorch or TensorFlow 2 quantizer is distributed through framework-specific Docker containers.

The Vitis AI Docker containers can be installed on Ubuntu 20.04, CentOS 7.8, 7.9, 8.1, and RHEL 8.3, 8.4. For developers working on Windows 11, WSL can be used to install the Vitis AI Docker containers.

Standard Containers
===================

Multiple versions of the Docker container are available, each tailored to specific frameworks. Follow the Docker download and running instructions as per the following links:

.. list-table:: 
   :widths: 30 70 
   :header-rows: 1

   * - Framework
     - Docker location
   * - PyTorch
     - https://hub.docker.com/r/amdih/ryzen-ai-pytorch
   * - TensorFlow 2
     - https://hub.docker.com/r/amdih/ryzen-ai-tensorflow2



GPU-Accelerated Quantization Containers
=======================================

The standard Vitis AI Docker containers do not support GPU-accelerated quantization. To create a container with GPU-accelerated quantization enabled, download the following archive and follow the instructions in the README file.

`Download and build GPU Docker containers <https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=ipu-rel-3.5.0-325-20240726.tar.gz>`_

.. note::
   In this documentation, **"NPU"** is used in descriptions, while **"IPU"** is retained in the tool's language, code, screenshots, and commands. This intentional 
   distinction aligns with existing tool references and does not affect functionality. Avoid making replacements in the code.



..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
