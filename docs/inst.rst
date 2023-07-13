.. _inst.rst:


############
Installation 
############


Supported Processors
~~~~~~~~~~~~~~~~~~~~

AMD Ryzen 7040U, 7040HS series mobile processors with Windows 11 OS. 

Ensure the IPU driver (tested for the 10.105.5.38 version) is installed as shown in the following image.

.. image:: images/ipu_driver.png


|
|


Prepare Client Device 
~~~~~~~~~~~~~~~~~~~~~

To enable development and deployment of IPU-based inference on the client device, it is crucial to have the following software installed, along with their minimum versions. 

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

For the installation, we recommend using a conda environment (Anaconda or Miniconda). 

Start a conda prompt. In the conda prompt, create and activate an environment for the rest of the installation process. 

.. code-block:: 

  conda create --name <name> python=3.9
  conda activate <name> 

.. _install-olive:

**1. Install Olive**


.. code-block::

  pip install olive-ai[cpu]


For additional information regarding the Olive installation, refer to the Microsoft documentation: https://microsoft.github.io/Olive/getstarted/installation.html


**2. Ensure ONNX Runtime is Installed**

.. code-block::
   
   pip install onnxruntime 

**3. Download and Extract Setup Package** 

https://www.xilinx.com/bin/public/openDownload?filename=voe-3.0-win_amd64.zip 


**4. Install Necessary Packages**

Change directory to the extracted setup package directory:

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

1. Specify IPU binary path. It is a required step everytime the application is run from a new terminal

.. code-block::

   set XLNX_VART_FIRMWARE=C:\[path_to_package]\voe-3.0-win_amd64\voe-3.0-win_amd64\Install\1x4.xclbin


.. _copy-vaip-config:

2. The setup package (``voe-3.0-win_amd64.zip``) contains the Vitis AI Execution Provider runtime configuration file ``vaip_config.json``. This file is required when configuring Vitis AI Execution Provider inside the ONNX runtime code. 

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
