.. _inst.rst:


############
Installation 
############


Supported Configurations
~~~~~~~~~~~~~~~~~~~~~~~~

The Ryzen AI Software Platform supports AMD Ryzen 7040U, 7040HS series mobile processors with Windows 11 OS.

Download the `IPU Driver <https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=ipu_stack_rel_silicon_2308.zip>`_ and install it by following these steps:

1. Extract the downloaded zip file.
2. Open a terminal in administrator mode and execute the ``.\amd_install_kipudrv.bat`` bat file.

Ensure that the IPU driver is installed from ``Device Manager`` -> ``System Devices`` -> ``AMD IPU Device`` as shown in the following image.

.. image:: images/ipu_device_properties1.png

|
|

Note: If you see the "Windows could not verify the digital signature of this driver" error message, follow `this tutorial <https://pureinfotech.com/disable-driver-signature-enforcement-windows-11/>`_ to disable signature checking."

|
|


Prepare Client Device 
~~~~~~~~~~~~~~~~~~~~~

To enable the development and deployment of IPU-based inference on the client device, you must have the following software installed, along with their minimum versions.

.. list-table:: 
   :widths: 25 25 
   :header-rows: 1

   * - Dependencies
     - Version Requirement
   * - Visual Studio
     - 2019
   * - cmake
     - version >= 3.26
   * - python
     - version >= 3.9 (3.9.13 64bit recommended) 
   * - Anaconda or Miniconda
     - Latest version
   * - AMD IPU driver
     - >= 10.105.5.42

|
|

Installation Steps
~~~~~~~~~~~~~~~~~~

The Ryzen AI Software Platform requires using a conda environment (Anaconda or Miniconda) for the installation process. 

Start a conda prompt. In the conda prompt, create and activate an environment for the rest of the installation process. 

.. code-block:: 

  conda create --name <name> python=3.9
  conda activate <name> 

.. _install-olive:

Install Quantizer
#################

Ryzen AI Software platform provides multiple quantization flow support

**Vitis AI ONNX Quantization** 

Vitis AI ONNX Quantization is post-training quantization that works on the models saved in ONNX format. To install it, download the installation file and follow the command:

https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=vai_q_onnx-1.15.0-py2.py3-none-any.whl

.. code-block::

   pip install vai_q_onnx-1.15.0-py2.py3-none-any.whl


**Vitis AI PyTorch/TensorFlow 2/TensorFlow Quantization**

Vitis AI PyTorch and TensorFlow Quantizer, which is part of the Vitis AI toolchain, require the installation of a Docker container on the host server.

The Vitis AI Docker container can be installed on Ubuntu 20.04, CentOS 7.8, 7.9, 8.1, and RHEL 8.3, 8.4. The developers working on Windows 11 can use WSL for installing Vitis AI Docker.

Multiple versions of the Docker container are available, each tailored to specific frameworks. Follow the Docker download and running instructions as per the following links:

.. list-table:: 
   :widths: 25 25 
   :header-rows: 1

   * - Framework
     - Docker location
   * - PyTorch
     - https://hub.docker.com/r/amdih/ryzen-ai-pytorch
   * - TensorFlow 2
     - https://hub.docker.com/r/amdih/ryzen-ai-tensorflow2
   * - TensorFlow 1
     - https://hub.docker.com/r/amdih/ryzen-ai-tensorflow 


The above Docker containers do not have GPU-accelerated quantization support. If you like to leverage GPU for the quantization process, you can download and build GPU Docker containers. The following TAR file has README that you can follow to build and run GPU dockers.  


https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=ryzen-ai-gpudockerfiles-3.5.0-130.tar.gz


**Olive Quantization**

Microsoft Olive framework supports quantization with Vitis AI ONNX Quantization:  

.. code-block::

   pip install olive-ai[cpu]


Note: Current Olive flow is not compatible with the latest pydantic version. Downgrade the pydantic version as follows:

.. code-block::

    pip install pydantic==1.10.9


For additional information regarding the Olive installation, refer to the Microsoft documentation:       
https://microsoft.github.io/Olive/getstarted/installation.html



Install ONNX Runtime
####################

.. code-block::
   
   pip install onnxruntime 

Install Vitis AI Execution Provider
###################################

Download and extract the Execution Provider setup package:

https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=voe-4.0-win-amd64.zip 

Change the directory to the extracted Execution Provider setup package directory and install the necessary packages:

.. code-block:: 

     cd voe-4.0-win_amd64\voe-4.0-win_amd64
     python installer.py
     pip install voe-0.1.0-cp39-cp39-win_amd64.whl
     pip install onnxruntime_vitisai-1.15.1-cp39-cp39-win_amd64.whl

|
|
   
Runtime Environment Setup 
~~~~~~~~~~~~~~~~~~~~~~~~~
   
.. _set-vart-envar:

1. **Runtime IPU Binary selection**: The IPU binaries are located inside the Vitis AI Execution Provider package. Selecting an IPU binary is a required step everytime the application is run from a new terminal. Ryzen AI Software platform provides a couple of IPU binaries using different configurations on the IPU device. 

**IPU binary 1x4.xclbin**: An AI stream using 1x4.xclbin use an IPU configuration that provides up to 2 TOPS performance. Most real-time application (video conferencing use cases) performance requirements can be met using this configuration. In the current Ryzen AI software platform, up to four such AI streams can be run in parallel on the IPU without any visible loss of performance.


**IPU binary 5x4.xclbin**: For more advanced use cases or larger models, IPU binary 5x4.xclbin can be used which uses a larger configuration to provide up to 10 TOPs performance. In the current version of the release, 5x4.xclbin does not support multiple concurrent AI streams, and can only be used by a single application. 


The procedure for selecting a specific binary using environment variables is as follows:

Selecting the 1x4.xclbin IPU binary:

.. code-block::

   set XLNX_VART_FIRMWARE=C:\path\to\1x4.xclbin


Selecting the 5x4.xclbin IPU binary:

.. code-block::

   set XLNX_VART_FIRMWARE=C:\path\to\5x4.xclbin
   set XLNX_TARGET_NAME="AMD_AIE2_5x4_Overlay"

Note: To select the 5x4.xclbin as the IPU binary, the additional XLNX_TARGET_NAME environment variable is required. 

.. _copy-vaip-config:

2. The Execution Provider setup package contains the Vitis AI Execution Provider runtime configuration file ``vaip_config.json``. This file is required when configuring Vitis AI Execution Provider (VAI EP) inside the ONNX Runtime code. 

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
