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

Note: If you see the "Windows could not verify the digital signature of this driver" error message, follow `this tutorial <https://pureinfotech.com/disable-driver-signature-enforcement-windows-11/>`_ to disable signature checking.


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
~~~~~~~~~~~~~~~~~~~

The Ryzen AI Software Platform requires using a conda environment (Anaconda or Miniconda) for the installation process. 

Start a conda prompt. In the conda prompt, create and activate an environment for the rest of the installation process. 

.. code-block:: 

  conda create --name <name> python=3.9
  conda activate <name> 

Install Quantizer
#################

Ryzen AI Software platform provides multiple quantization flow support. The Vitis AI ONNX Quantization is one of the quickest ways to enable quantization. 

**Vitis AI ONNX Quantization**

Vitis AI ONNX Quantization is a post-training quantization method that works on models saved in the ONNX format. If you'd like to explore this advanced quantization method, you can follow the installation steps below:

1. Download the installation file from the following link:

   `Vitis AI ONNX Quantization <https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=vai_q_onnx-1.15.0-py2.py3-none-any.whl>`_

2. Install Vitis AI ONNX Quantization using the following command:

.. code-block:: shell

   pip install vai_q_onnx-1.15.0-py2.py3-none-any.whl

For other quantization options please refer to the :doc:`advanced_installation` page. 


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
     pip install voe-0.1.0-cp39-cp39-win-amd64.whl
     pip install onnxruntime_vitisai-1.15.1-cp39-cp39-win-amd64.whl

|
|
   
Runtime Environment Setup 
~~~~~~~~~~~~~~~~~~~~~~~~~
   
Runtime IPU Binary Selection
############################

The IPU binaries are located inside the Vitis AI Execution Provider package. Selecting an IPU binary is a required step every time the application is run from a new terminal. For example, IPU binary 1x4.xclbin is selected as below 

.. code-block::

   set XLNX_VART_FIRMWARE=C:\path\to\1x4.xclbin

To understand different other IPU binary options please refer to the :doc:`advanced_installation` page.


Runtime Configuration File
##########################

The Execution Provider setup package contains the Vitis AI Execution Provider runtime configuration file ``vaip_config.json``. This file is required when configuring Vitis AI Execution Provider (VAI EP) inside the ONNX Runtime code.

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
