.. include:: /icons.txt

#########################
Installation Instructions
#########################


This page covers Ryzen AI installation on Windows. For Linux installation, please refer to :doc:`linux`.


*************
Prerequisites
*************

The Ryzen AI Software supports AMD processors with a Neural Processing Unit (NPU). Refer to the release notes for the full list of :ref:`supported configurations <supported-configurations>`.

The following dependencies must be installed on the system before installing the Ryzen AI Software:

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
   * - Python distribution (Miniforge preferred)
     - Latest version

|

|warning| **IMPORTANT**:

- Visual Studio 2022 Community: ensure that `Desktop Development with C++` is installed

- Miniforge: ensure that the following path is set in the System PATH variable: ``path\to\miniforge3\condabin`` or ``path\to\miniforge3\Scripts\`` or ``path\to\miniforge3\`` (The System PATH variable should be set in the *System Variables* section of the *Environment Variables* window).

|

.. _install-driver:

*******************
Install NPU Drivers
*******************

- Download and Install the NPU driver version: 32.0.203.280 or newer using the following links: 

  - :download:`NPU Driver (Version 32.0.203.280) <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=NPU_RAI1.5_280_WHQL.zip>`
  - :download:`NPU Driver (Version 32.0.203.304) <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=NPU_RAI1.6_304_WHQL.zip>`

- Install the NPU drivers by following these steps:

  - Extract the downloaded ZIP file.
  - Open a terminal in administrator mode and execute the ``.\npu_sw_installer.exe`` file.

- Ensure that NPU MCDM driver (Version:32.0.203.280, Date:5/16/2025) or (Version:32.0.203.304, Date:10/07/2025) is correctly installed by opening Task Manager -> Performance -> NPU0.


.. _install-bundled:

*************************
Install Ryzen AI Software
*************************

- Download the Ryzen AI Software installer :download:`ryzenai-lt-1.7.0.exe <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=ryzenai-lt-1.7.0.exe>`.

- Launch the EXE installer and follow the instructions on the installation wizard:

  - Accept the terms of the Licence agreement
  - Provide the destination folder for Ryzen AI installation (default: ``C:\Program Files\RyzenAI\1.7.0``)
  - Specify the name for the conda environment (default: ``ryzen-ai-1.7.0``)

The Ryzen AI Software packages are now installed in the conda environment created by the installer.

.. note::
   NuGet package is available to download at :download:`ryzen-ai-1.7.0-nuget.zip <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=ryzen-ai-1.7.0-nuget.zip>`.

.. _quicktest:


*********************
Test the Installation
*********************

The Ryzen AI Software installation folder contains test to verify that the software is correctly installed. This installation test can be found in the ``quicktest`` subfolder.

- Open a Conda command prompt (search for "Miniforge Prompt" in the Windows start menu)

- Activate the Conda environment created by the Ryzen AI installer:

.. code-block::

   conda activate <env_name>

- Run the test:

.. code-block::

   cd %RYZEN_AI_INSTALLATION_PATH%/quicktest
   python quicktest.py 2>&1 | findstr /i "Operators Subgraphs VITIS_EP_CPU NPU Test"


- The quicktest.py script sets up the environment and runs a simple CNN model. On a successful run, you will see an output similar to the one shown below. This indicates that the model is running on the NPU and that the installation of the Ryzen AI Software was successful:

.. code-block::

  [Vitis AI EP] No. of Operators :
      NPU   398
  VITIS_EP_CPU     2
  [Vitis AI EP] No. of Subgraphs :
    NPU     1
  Test Passed



.. note::

    The full path to the Ryzen AI Software installation folder is stored in the ``RYZEN_AI_INSTALLATION_PATH`` environment variable.





..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
