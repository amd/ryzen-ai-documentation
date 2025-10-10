.. include:: /icons.txt

#################################
Windows Installation Instructions
#################################



*************
Prerequisites
*************

The Ryzen AI Software supports AMD processors with a Neural Processing Unit (NPU). For a list of supported hardware configurations, refer to :ref:`hardware-support`.

The following dependencies must be installed on the system before installing the Ryzen AI Software:

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Dependencies
     - Version Requirement
   * - Windows 11
     - >= 22621.3527
   * - `Visual Studio Community <https://apps.microsoft.com/detail/xpdcfjdklzjlp8?hl=en-US&gl=US>`_
     - 2022 with `Desktop Development with C++` checked
   * - `cmake <https://cmake.org/download/>`_
     - >= 3.26
   * - `Python (Miniforge preferred) <https://conda-forge.org/download/>`_
     - >= 3.10
   * - :ref:`install-driver` 
     - >= 32.0.203.280

|

|warning| **IMPORTANT**:

- Miniforge: Ensure that the proper miniforge paths are set in the System PATH variable. Open Windows PowerShell by right clicking and "Run as administrator" to set system path environment varibles. After opening a command prompt, you can use the following code to add the appropriate environment variables, substituting your actual paths:
.. code-block:: powershell

  $existingPath = [System.Environment]::GetEnvironmentVariable('Path', 'Machine')

.. code-block:: powershell

  $newPaths = "C:\Users\<user>\miniforge3\Scripts;C:\Users\<user>\miniforge3\condabin"

.. code-block:: powershell

  [System.Environment]::SetEnvironmentVariable('Path', "$existingPath;$newPaths", 'Machine')

|

.. _install-driver:

*******************
Install NPU Drivers
*******************

- Under "Task Manager" in Windows, go to Performance -> NPU0 to check the driver version. 
- If needed, download the NPU driver version: 32.0.203.280 or the latest 32.0.203.304 here:

  - :download:`NPU Driver (Version 32.0.203.280) <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=NPU_RAI1.5_280_WHQL.zip>`
  - :download:`NPU Driver (Version 32.0.203.304) <https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=NPU_RAI1.6_304_WHQL.zip>`
- Extract the downloaded ZIP file.
- Right click and "Run as administrator" on ``npu_sw_installer.exe``.
- Check that the NPU driver (Version:32.0.203.280, Date:5/16/2025) or (Version:32.0.203.304, Date:10/07/2025) was correctly installed by opening Task Manager -> Performance -> NPU0.


.. _install-bundled:

*************************
Install Ryzen AI Software
*************************

- Download the Ryzen AI Software installer :download:`ryzen-ai-lt-1.6.0-GA.exe <https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=ryzen-ai-lt-1.6.0-GA.exe>`.

- Launch the EXE installer and follow the instructions on the installation wizard:

  - Accept the terms of the Licence agreement
  - Provide the destination folder for Ryzen AI installation (default: ``C:\Program Files\RyzenAI\1.6.0``)
  - Specify the name for the conda environment (default: ``ryzen-ai-1.6.0``)

The Ryzen AI Software packages should now installed in the conda environment created by the installer.

.. note::
   **The LLM flow requires an additional patch installation.** See the next section (:ref:`apply-patch`) for instructions.

.. _apply-patch:

*************************
Apply RyzenAI 1.6.0 Patch
*************************

This mandatory patch updates ``onnx_custom_ops.dll`` in the Ryzen AI installation.

**Steps:**

- Download and extract the patch :download:`ryzenai-1.6.0-patch.zip <https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=ryzenai-1.6.0-patch.zip>`
- Open an **Administrator** Command Prompt or PowerShell in the extracted folder.
- Run:

  .. code-block:: bash

     python ryzenai-1.6.0-patch.py --install-path "C:\Program Files\RyzenAI\1.6.0"

.. note::
   The script creates a timestamped backup before replacing the DLL.


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
   python quicktest.py


- The quicktest.py script sets up the environment and runs a simple CNN model. On a successful run, you will see an output similar to the one shown below. This indicates that the model is running on the NPU and that the installation of the Ryzen AI Software was successful:

.. code-block::

    [Vitis AI EP] No. of Operators :   NPU   398 VITIS_EP_CPU     2
    [Vitis AI EP] No. of Subgraphs :   NPU     1 Actually running on NPU     1
    Test Passed



.. note::

    The full path to the Ryzen AI Software installation folder is stored in the ``RYZEN_AI_INSTALLATION_PATH`` environment variable.





..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
