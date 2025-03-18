.. include:: icons.txt

#########################
Installation Instructions
#########################



*************
Prerequisites
*************

The Ryzen AI Software supports AMD processors with a Neural Processing Unit (NPU). Consult the release notes for the full list of :ref:`supported configurations <supported-configurations>`. 

The following dependencies must be present on the system before installing the Ryzen AI Software:

.. list-table:: 
   :widths: 25 25 
   :header-rows: 1

   * - Dependencies
     - Version Requirement
   * - Windows 11
     - build >= 22621.3527
   * - Visual Studio
     - 2022
   * - cmake
     - version >= 3.26
   * - Anaconda or Miniconda
     - Latest version

|

|warning| **IMPORTANT**: 

- Visual Studio 2022 Community: ensure that "Desktop Development with C++" is installed

- Anaconda or Miniconda: ensure that the following path is set in the System PATH variable: ``path\to\anaconda3\Scripts`` or ``path\to\miniconda3\Scripts`` (The System PATH variable should be set in the *System Variables* section of the *Environment Variables* window). 

|

*******************
Install NPU Drivers
*******************

- Download the NPU driver installation package :download:`NPU Driver <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=NPU_RAI1.4_GA_257_WHQL.zip>`

- Install the NPU drivers by following these steps:

  - Extract the downloaded ``NPU_RAI1.4_GA_257_WHQL.zip`` zip file.
  - Open a terminal in administrator mode and execute the ``.\npu_sw_installer.exe`` exe file.

- Ensure that NPU MCDM driver (Version:32.0.203.257, Date:3/12/2025) is correctly installed by opening ``Device Manager`` -> ``Neural processors`` -> ``NPU Compute Accelerator Device``.


.. _install-bundled:

*************************
Install Ryzen AI Software
*************************

- Download the RyzenAI Software installer :download:`ryzen-ai-1.4.0.exe <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=ryzen-ai-1.4.0-us.exe>`.

- Launch the MSI installer and follow the instructions on the installation wizard:

  - Accept the terms of the Licence agreement
  - Provide the destination folder for Ryzen AI installation (default: ``C:\Program Files\RyzenAI\1.4.0``)
  - Specify the name for the conda environment (default: ``ryzen-ai-1.4.0``)


The Ryzen AI Software packages are now installed in the conda environment created by the installer. 


.. _quicktest:


*********************
Test the Installation
*********************

The Ryzen AI Software installation folder contains test to verify that the software is correctly installed. This installation test can be found in the ``quicktest`` subfolder.

- Open a Conda command prompt (search for "Anaconda Prompt" in the Windows start menu)

- Activate the Conda environment created by the Ryzen AI installer:

.. code-block::

   conda activate <env_name>

- Run the test:

.. code-block::

   cd %RYZEN_AI_INSTALLATION_PATH%/quicktest
   python quicktest.py


- The quicktest.py script sets up the environment and runs a simple CNN model. On a successful run, you will see an output similar to the one shown below. This indicates that the model is running on the NPU and that the installation of the Ryzen AI Software was successful:

.. code-block::

   [Vitis AI EP] No. of Operators :   CPU     2    NPU   398
   [Vitis AI EP] No. of Subgraphs :   NPU     1 Actually running on NPU     1
   ...
   Test Passed
   ...


.. note::

    The full path to the Ryzen AI Software installation folder is stored in the ``RYZEN_AI_INSTALLATION_PATH`` environment variable.


*****************************
Additional Ryzen AI Installer
*****************************

Linux Installer
~~~~~~~~~~~~~~~

BF16 models (CNN or Transformer) require processing power in terms of core count and memory, depending on model size. If a larger model cannot be compiled on a Windows machine due to hardware limitations (e.g., insufficient RAM), an alternative Linux-based compilation flow is supported. More details can be found here: :doc:`rai_linux`



Lightweight Installer
~~~~~~~~~~~~~~~~~~~~~

A lightweight installer is available with reduced features. It cannot be used for compiling BF16 models but fully supports compiling and running INT8 models and running LLM models.

- Download the RyzenAI Software Runtime MSI installer :download:`ryzen-ai-rt-1.4.0-ea.msi <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=ryzen-ai-rt-1.4.0-ea.msi>`.

- Launch the MSI installer and follow the instructions on the installation wizard:

  - Accept the terms of the Licence agreement
  - Provide the destination folder for Ryzen AI installation (default: ``C:\Program Files\RyzenAI\1.4.0-rt``)
  - Specify the name for the conda environment (default: ``ryzen-ai-rt-1.4.0``)



.. _driver-compatibility:


*************************************
VitisAI EP / NPU Driver Compatibility
*************************************

The VitisAI EP requires a compatible version of the NPU drivers. For each version of the VitisAI EP, compatible drivers are bounded by a minimum version and a maximum release date. NPU drivers are backward compatible with VitisAI EP released up to 3 years before. The maximum driver release date is therefore set to 3 years after the release date of the corresponding VitisAI EP.

The table below summarizes the driver requirements for the different versions of the VitisAI EP.

.. list-table:: 
   :header-rows: 1

   * - VitisAI EP version
     - Minimum NPU Driver version
     - Maximum NPU Driver release date
   * - 1.4
     - 32.0.203.257
     - March 25th, 2028
   * - 1.3.1
     - 32.0.201.242
     - January 17th, 2028
   * - 1.3
     - 32.0.201.237
     - November 26th, 2027
   * - 1.2
     - 32.0.201.204
     - July 30th, 2027

.. _apu-types:

*****************
APU Types
*****************

The Ryzen AI Software supports different types of NPU-enabled APUs. These APU types are referred to as PHX, HPT, STX and KRK. 

To programmatically determine the type of the local APU, it is possible to enumerate the PCI devices and check for an instance with a matching Hardware ID.

.. list-table:: 
   :header-rows: 1

   * - Vendor
     - Device
     - Revision
     - APU Type
   * - 0x1022
     - 0x1502
     - 0x00
     - PHX or HPT 
   * - 0x1022
     - 0x17F0
     - 0x00
     - STX 
   * - 0x1022
     - 0x17F0
     - 0x10
     - STX 
   * - 0x1022
     - 0x17F0
     - 0x11
     - STX 
   * - 0x1022
     - 0x17F0
     - 0x20
     - KRK


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
