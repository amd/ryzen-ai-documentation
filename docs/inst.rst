.. include:: icons.txt

#########################
Installation Instructions
#########################

.. note::
   An update was made the the RyzenAI 1.3 release package. AMD recommends downloading and installing this newer version (ref: ryzen-ai-rt-1.3.0-20241204.msi) and replacing any installation based on the previous package (ref: ryzen-ai-rt-1.3.0-20241126.msi)

************************
Supported Configurations
************************

The Ryzen AI Software supports the following processors running Windows 11 (Win 11 build>=22621.3527 is required for Ryzen AI Software 1.3.) 

- Phoenix (PHX): AMD Ryzen™ 7940HS, 7840HS, 7640HS, 7840U, 7640U.
- Hawk (HPT): AMD Ryzen™ 8640U, 8640HS, 8645H, 8840U, 8840HS, 8845H, 8945H.
- Strix (STX): AMD Ryzen™ Ryzen AI 9 HX375, Ryzen AI 9 HX370, Ryzen AI 9 365 

The rest of this document will refer to Phoenix as PHX, Hawk as HPT, and Strix as STX.


******************
Prerequisites
******************

To enable the development and deployment of applications leveraging the NPU, you must have the following software installed on the system.

.. list-table:: 
   :widths: 25 25 
   :header-rows: 1

   * - Dependencies
     - Version Requirement
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

- Download the NPU driver installation package :download:`NPU Driver <https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=NPU_RAI1.3.zip>`

- Install the NPU drivers by following these steps:

  - Extract the downloaded ``NPU_RAI1.3.zip`` zip file.
  - Open a terminal in administrator mode and execute the ``.\npu_sw_installer.exe`` exe file.

- Ensure that NPU MCDM driver (Version:32.0.203.237, Date:11/8/2024) is correctly installed by opening ``Device Manager`` -> ``Neural processors`` -> ``NPU Compute Accelerator Device``.




.. _install-bundled:

*****************************
Install the Ryzen AI Software
*****************************

- Download the RyzenAI Software MSI installer :download:`ryzen-ai-rt-1.3.0.1-20241217.msi <https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=ryzen-ai-rt-1.3.0.1-20241217.msi>`.

- Launch the MSI installer and follow the instructions on the installation wizard:

  - Accept the terms of the Licence agreement  
  - Provide the destination folder for Ryzen AI installation (default: ``C:\Program Files\RyzenAI\1.3.0``)  
  - Specify the name for the conda environment (default: ``ryzen-ai-1.3.0``)  

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
