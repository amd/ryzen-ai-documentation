.. include:: icons.txt

#########################
Installation Instructions
#########################

.. note::
   Version 1.3.1 (released on January 17th, 2025) is the latest update of the Ryzen AI Software. AMD recommends downloading and installing the newer version of driver (ref: RAI_1.3.1_242_WHQL.zip) and MSI installer (ref: ryzen-ai-1.3.1.msi) and replacing any installation based on the previous packages.


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

.. _install-npu-drivers:

*******************
Install NPU Drivers
*******************

- Download the NPU driver installation package :download:`NPU Driver 1.3.1_242 <https://account.amd.com/en/forms/downloads/amd-end-user-license-xef.html?filename=RAI_1.3.1_242_WHQL.zip>`
- Extract the downloaded zip file.
- Open a terminal in administrator mode and execute ``.\npu_sw_installer.exe``.
- Check the installation messages to ensure that NPU MCDM driver version 32.0.203.242 (12/31/2024) is correctly installed.

.. _install-bundled:

*****************************
Install the Ryzen AI Software
*****************************

- Download the RyzenAI Software MSI installer :download:`ryzen-ai-1.3.1.msi <https://account.amd.com/en/forms/downloads/amd-end-user-license-xef.html?filename=ryzen-ai-1.3.1.msi>`.

- Launch the MSI installer and follow the instructions on the installation wizard:

  - Accept the terms of the Licence agreement  
  - Provide the destination folder for Ryzen AI installation (default: ``C:\Program Files\RyzenAI\1.3.1``)  
  - Specify the name for the conda environment (default: ``ryzen-ai-1.3.1``)  

The Ryzen AI Software packages are now installed in the conda environment created by the installer. Refer to the :doc:`runtime_setup` page for more details about setting up the environment before running an inference session on the NPU.


|memo| **NOTE**: This installation is only for CNN models. The LLM models flow installation is hosted in the GitHub repo; for details, please check :doc:`llm_flow`


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


*************************
Additional Considerations
*************************

- The full path to the Ryzen AI Software installation folder is stored in the ``RYZEN_AI_INSTALLATION_PATH`` environment variable. 

- To install the Ryzen AI Software in a pre-existing conda environment, follow the :doc:`manual_installation` instructions.



..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
