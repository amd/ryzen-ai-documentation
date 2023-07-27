.. _inst.rst:


############
Installation 
############


Supported Processors
~~~~~~~~~~~~~~~~~~~~

AMD Ryzen 7040U, 7040HS series mobile processors with Windows 11 OS. 

Ensure that the IPU driver (tested for the 10.105.5.38 version) is installed as shown in the following image.

.. image:: images/ipu_driver.png


|
|


Prepare Client Device 
~~~~~~~~~~~~~~~~~~~~~

To enable the development and deployment of IPU-based inference on the client device, it is crucial to have the following software installed, along with their minimum versions. 

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
     - >= 10.105.5.38

|
|

Installation Steps
~~~~~~~~~~~~~~~~~~

Using a conda environment (Anaconda or Miniconda) is recommended for the installation. 

Start a conda prompt. In the conda prompt, create and activate an environment for the rest of the installation process. 

.. code-block:: 

  conda create --name <name> python=3.9
  conda activate <name> 

.. _install-olive:

1. Install Olive:

.. code-block::

   pip install olive-ai[cpu]

For additional information regarding the Olive installation, refer to the Microsoft documentation:       
https://microsoft.github.io/Olive/getstarted/installation.html


2. Ensure ONNX Runtime is installed:

.. code-block::
   
   pip install onnxruntime 

3. Download and extract the setup package:

   https://www.xilinx.com/bin/public/openDownload?filename=voe-3.0-win_amd64.zip 


4. Install the necessary packages:

   Change the directory to the extracted setup package directory:

   .. code-block:: 
   
      cd voe-3.0-win_amd64\voe-3.0-win_amd64\Install
   
   Install packages:

   .. code-block:: 

      pip install voe-0.1.0-cp39-cp39-win_amd64.whl
      pip install onnxruntime_vitisai-1.16.0-cp39-cp39-win_amd64.whl

|
|
   
Runtime Environment Setup 
~~~~~~~~~~~~~~~~~~~~~~~~~
   
.. _set-vart-envar:

1. Specify the IPU binary path. It is a required step everytime the application is run from a new terminal:

.. code-block::

   set XLNX_VART_FIRMWARE=C:\[path_to_package]\voe-3.0-win_amd64\voe-3.0-win_amd64\Install\1x4.xclbin


.. _copy-vaip-config:

2. The setup package (``voe-3.0-win_amd64.zip``) contains the Vitis AI Execution Provider runtime configuration file ``vaip_config.json``. This file is required when configuring Vitis AI Execution Provider (VAI EP) inside the ONNX Runtime code. 


Runtime IPU Binary selection 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ryzen AI Software platform provides a couple of IPU binaries using different configurations on the IPU device. 

**IPU binary 1x4.xclbin**: An AI stream using 1x4.xclbin use a 1x4 grid-style configuration on the IPU device that provides 2 TOPS performance. Most real-time application (video conferencing use cases) performance requirements can be met using this configuration. Four such AI streams (each utilizing 1x4.xclbin) can be run in parallel on the IPU device without any visible loss of performance. When using 1x4.xclbin, Ryzen AI supports up to 8 concurrent AI streams by spatial and temporal sharing of the IPU device by multiple 1x4 style configurations. 


**IPU binary 5x4.xclbin**: For a more advanced use case or larger model, IPU binary 5x4.xclbin can be used which uses a larger 5x4 grid-style configuration that occupies the complete IPU device to provide 10 TOPs performance. With this configuration, up to 8 AI streams can be run concurrently by temporal share of the IPU device.  

The procedure of selecting a specific binary by using the environment variables as shown below:

Selecting 1x4.xclbin IPU binary

..code-block::

   set XLNX_VART_FIRMWARE=C:\path\to\1x4.xclbin
   set XLNX_TARGET_NAME="AMD_AIE2_Nx4_Overlay"


Selecting 5x4.xclbin IPU binary

..code-block::

   set XLNX_VART_FIRMWARE=C:\path\to\5x4.xclbin
   set XLNX_TARGET_NAME="AMD_AIE2_5x4_Overlay"


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
