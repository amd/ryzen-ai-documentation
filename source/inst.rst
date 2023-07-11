.. _inst.rst:


############
Installation 
############


Supported Processors
~~~~~~~~~~~~~~~~~~~~

AMD Ryzen 7040U, 7040HS series mobile processors with Windows 11 OS. 

Ensure the IPU driver (officially tested for the 10.105.5.38 version) is installed as shown in the following image.

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

.. note::

  **Temporary Note**: Today the second wheel file is missing from the downloaded package. I have informed this to Andy and Yiming and they confirmed they will fix it. 


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
  Please Read: Important Legal Notices
  #####################################

  The information presented in this document is for informational purposes only and may contain technical inaccuracies, omissions, and typographical errors. The information contained herein is subject to change and may be rendered inaccurate for many reasons, including but not limited to product and roadmap changes, component and motherboard version changes, new model and/or product releases, product differences between differing manufacturers, software changes, BIOS flashes, firmware upgrades, or the like. Any computer system has risks of security vulnerabilities that cannot be completely prevented or mitigated. AMD assumes no obligation to update or
  otherwise correct or revise this information. However, AMD reserves the right to revise this information and to make changes from time to time to the content hereof without obligation of AMD to notify any person of such revisions or changes. THIS INFORMATION IS PROVIDED "AS IS." AMD MAKES NO REPRESENTATIONS OR WARRANTIES WITH RESPECT TO THE CONTENTS HEREOF AND ASSUMES NO RESPONSIBILITY FOR ANY INACCURACIES, ERRORS, OR OMISSIONS THAT MAY APPEAR IN THIS INFORMATION. AMD SPECIFICALLY
  DISCLAIMS ANY IMPLIED WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR ANY PARTICULAR PURPOSE. IN NO EVENT WILL AMD BE LIABLE TO ANY
  PERSON FOR ANY RELIANCE, DIRECT, INDIRECT, SPECIAL, OR OTHER CONSEQUENTIAL DAMAGES ARISING FROM THE USE OF ANY INFORMATION CONTAINED HEREIN, EVEN IF
  AMD IS EXPRESSLY ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. 

  ##################################
  AUTOMOTIVE APPLICATIONS DISCLAIMER
  ##################################


  AUTOMOTIVE PRODUCTS (IDENTIFIED AS "XA" IN THE PART NUMBER) ARE NOT WARRANTED FOR USE IN THE DEPLOYMENT OF AIRBAGS OR FOR USE IN APPLICATIONS
  THAT AFFECT CONTROL OF A VEHICLE ("SAFETY APPLICATION") UNLESS THERE IS A SAFETY CONCEPT OR REDUNDANCY FEATURE CONSISTENT WITH THE ISO 26262 AUTOMOTIVE SAFETY STANDARD ("SAFETY DESIGN"). CUSTOMER SHALL, PRIOR TO USING OR DISTRIBUTING ANY SYSTEMS THAT INCORPORATE PRODUCTS, THOROUGHLY TEST SUCH SYSTEMS FOR SAFETY PURPOSES. USE OF PRODUCTS IN A SAFETY APPLICATION WITHOUT A SAFETY DESIGN IS FULLY AT THE RISK OF CUSTOMER, SUBJECT ONLY TO APPLICABLE LAWS AND REGULATIONS GOVERNING LIMITATIONS ON PRODUCT LIABILITY.

  #########
  Copyright
  #########


  © Copyright 2023 Advanced Micro Devices, Inc. AMD, the AMD Arrow logo, Ryzen, Vitis AI, and combinations thereof are trademarks of Advanced Micro Devices,
  Inc. AMBA, AMBA Designer, Arm, ARM1176JZ-S, CoreSight, Cortex, PrimeCell, Mali, and MPCore are trademarks of Arm Limited in the US and/or elsewhere. PCI, PCIe, and PCI Express are trademarks of PCI-SIG and used under license. OpenCL and the OpenCL logo are trademarks of Apple Inc. used by permission by Khronos. Other product names used in this publication are for identification purposes only and may be trademarks of their respective companies.


