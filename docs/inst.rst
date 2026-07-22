.. include:: /icons.txt

#########################
Installation Instructions
#########################


This page covers Ryzen AI installation on Windows.

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

- Visual Studio 2022 Community (Optional for AMD Quark, to support custom op flow): ensure that `Desktop Development with C++` is installed

- Miniforge: ensure that the following path is set in the System PATH variable: ``path\to\miniforge3\condabin`` or ``path\to\miniforge3\Scripts\`` or ``path\to\miniforge3\`` (The System PATH variable should be set in the *System Variables* section of the *Environment Variables* window).

|

.. _install-driver:

*******************
Install NPU Drivers
*******************

- Download and Install the NPU driver version: 32.0.203.280 or newer using the following links:

  - :download:`NPU Driver (Version 32.0.203.280) <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=NPU_RAI1.5_280_WHQL.zip>`

    - NPU driver 32.0.203.376 is production driver for Phoenix, Hawk Point, Strix, Strix Halo, and Krackan Point.
  - :download:`NPU Driver (Version 32.0.203.376) <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=NPU_RAI_376_WHQL.zip>`

- Install the NPU drivers by following these steps:

  - Extract the downloaded ZIP file.
  - Open a terminal in administrator mode and execute the ``.\npu_sw_installer.exe`` file.

- Ensure that NPU driver (Version:32.0.203.280, Date:5/16/2025) is correctly installed by opening Task Manager -> Performance -> NPU0. 


.. _install-bundled:

*************************
Install Ryzen AI Software
*************************

- Download the Ryzen AI Software installer :download:`ryzen-ai-1.8.0.exe <https://account.amd.com/en/forms/downloads/xef.html?filename=ryzen-ai-1.8.0.exe>`.

- Launch the EXE installer and follow the instructions on the installation wizard:

  - Accept the terms of the Licence agreement
  - Provide the destination folder for Ryzen AI installation (default: ``C:\Program Files\RyzenAI\1.8.0``)
  - Specify the name for the conda environment (default: ``ryzen-ai-1.8.0``)

The Ryzen AI Software packages are now installed in the conda environment created by the installer.

.. note::
   NuGet package is available to download at :download:`ryzen_ai_nuget_1.8.0.zip <https://account.amd.com/en/forms/downloads/xef.html?filename=ryzen_ai_nuget_1.8.0.zip>`.



.. _quicktest:


*********************
Test the Installation
*********************

The Ryzen AI Software installation folder contains test to verify that the software is correctly installed. This installation test can be found in the ``quicktest`` subfolder which is expected to work for Strix (STX) or newer devices.

- Open a Conda command prompt (search for "Miniforge Prompt" in the Windows start menu)

- Activate the Conda environment created by the Ryzen AI installer:

.. code-block::

   conda activate ryzen-ai-<version>

- Run the test:

.. code-block::

   cd %RYZEN_AI_INSTALLATION_PATH%/quicktest
   python quicktest.py

.. code-block::

  [I:onnxruntime:, session_state_utils.cc:243 onnxruntime::session_state_utils::SaveInitializedTensors] Saving initialized tensors.
  [I:onnxruntime:, session_state_utils.cc:438 onnxruntime::session_state_utils::SaveInitializedTensors] Done saving initialized tensors
  [I:onnxruntime:, inference_session.cc:2532 onnxruntime::InferenceSession::Initialize] Session successfully initialized.
  Test Finished

- Verify NPU activity by opening **Task Manager → Performance → NPU** while the test is running. You should see NPU utilization increase during model inference.

To enable NPU offloading logs using :ref:`ONNX Runtime session options <enabling-onnx-runtime-logs>`, modify the ``quicktest.py`` script to include session options that control logging verbosity. The following code snippet demonstrates how to set up the session options for detailed logging:

.. code-block:: python

   # Create session options
   session_options = ort.SessionOptions()
   session_options.log_severity_level = 0  # 0=Verbose, 1=Info, 2=Warning, 3=Error, 4=Fatal

   try:
       session = ort.InferenceSession(model,
                                sess_options=session_options,
                                providers=providers,
                                provider_options=provider_options)
   except Exception as e:
       print(f"Failed to create an InferenceSession: {e}")
       sys.exit(1)  # Exit the program with a non-zero status to indicate an error


- Run the updated ``quicktest.py`` script with logs filter:

.. code-block::

   cd %RYZEN_AI_INSTALLATION_PATH%/quicktest
   python quicktest.py 2>&1 | findstr /i "Vitis | NPU | Test"


- On a successful run, the output will look ssimilar to the one shown below. This indicates that the model is running on the NPU and that the installation of the Ryzen AI Software was successful:

.. code-block::

    [I:onnxruntime:, stat.cpp:198 stat.cpp] [Vitis AI EP] No. of Operators :
    [I:onnxruntime:, stat.cpp:198 stat.cpp]    NPU   398
    [I:onnxruntime:, stat.cpp:198 stat.cpp] VITIS_EP_CPU     2
    [I:onnxruntime:, stat.cpp:198 stat.cpp] [Vitis AI EP] No. of Subgraphs :
    [I:onnxruntime:, stat.cpp:198 stat.cpp]    NPU     1
    [I:onnxruntime:, stat.cpp:198 stat.cpp] Actually running on NPU      1
    [I:onnxruntime:, vitisai_compile_model.cpp:1488 vitisai_compile_model.cpp] AVG CPU Usage 4.93969%
    [I:onnxruntime:, vitisai_compile_model.cpp:1489 vitisai_compile_model.cpp] Peak Working Set size 565.277 MB
    [V:onnxruntime:, session_state.cc:1350 onnxruntime::VerifyEachNodeIsAssignedToAnEp]  All nodes placed on [VitisAIExecutionProvider]. Number of nodes: 3
    [I:onnxruntime:, unzip.hpp:18 unzip.hpp] inflateInit successful, available input: 137827
    Test finished

.. note::

    - The full path to the Ryzen AI Software installation folder is stored in the ``RYZEN_AI_INSTALLATION_PATH`` environment variable.



..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
