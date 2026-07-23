############
Installation
############

This page consolidates all requirements and installation steps for running Windows ML on Ryzen AI PCs.

*************
Prerequisites
*************

.. list-table::
   :widths: 30 40
   :header-rows: 1

   * - Requirement
     - Version or Notes
   * - Windows
     - Windows 11 24H2 (build 26100) or greater
   * - Ryzen AI NPU
     - Supported processor with NPU. See :ref:`supported configurations <ryzenai:supported-configurations>` in the release notes.
   * - Visual Studio (for C++)
     - Visual Studio 2022, latest version. Ensure *Desktop Development with C++* is installed.
   * - Visual Studio Code (optional)
     - For model conversion using AI Toolkit extension
   * - Python (for Python examples)
     - 3.10 to 3.12
   * - C++ (for C++ examples)
     - C++20 or later

For the complete list of supported Windows versions, refer to `Windows App SDK support <https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/support>`_.

************
Installation
************

Follow these steps in order:

1. **Install NPU drivers:** Follow the :doc:`RAI installation instructions <ryzenai:inst>`. Download and install the NPU driver (version 32.0.203.280 or newer) from the AMD Ryzen AI driver page.

2. **Install Windows App SDK:** Windows ML is included as part of the Windows App SDK. Install the version required by your branch/sample from `Windows App SDK downloads <https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/downloads>`_.

3. **Verify installation:** For Python, ensure the ``wasdk-microsoft-windows-ai-machinelearning`` package is installed (e.g., via ``pip install``) and matches the Windows App SDK version used by your sample branch. Run ``conda list | findstr wasdk`` to verify.


.. note::

   The Windows ML VitisAI Execution Provider (EP) NuGet packages are available for download:

   .. list-table::
      :widths: auto
      :header-rows: 1

      * - Version
        - Package Download
      * - **Release 2026.5D**
        - :download:`AMD.NPU.WinML.VitisAI.EP_2026_5D.nupkg <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=AMD.NPU.WinML.VitisAI.EP_2026_5D.nupkg>`
      * - **Release 2026.7D**
        - :download:`AMD.NPU.WinML.VitisAI.EP_2026_7D.nupkg <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=AMD.NPU.WinML.VitisAI.EP_2026_7D.nupkg>`


**************************
Key Features of Windows ML
**************************

- **Dynamically downloads latest EPs:** Compatible execution providers are downloaded from the Microsoft Store on demand
- **Shared Windows-wide ONNX Runtime:** Reduces application size; no need to bundle ORT
- **Smaller downloads and installs:** EPs are shared across applications
- **Broad hardware support:** Works across CPUs, GPUs, and NPUs from different vendors with ONNX Runtime

*****************************
Windows ML setup verification
*****************************

Install the required Python packages in the conda environment `winml_env`

.. code-block:: shell

    conda create -n winml_env python==3.11
    conda activate winml_env
    git clone https://github.com/amd/RyzenAI-SW.git
    cd <RyzenAI-SW>\WinML\CNN\ResNet
    pip install --pre -r .\requirements.txt

Check the installed wasdk Python version and install same version of `Windows App SDK <https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/downloads>`_:

.. code-block:: shell

    conda list | findstr wasdk

Download the Windows App SDK that matches the wasdk version to ensure the Windows ML execution providers work as expected.

.. code-block:: shell

    curl -L -o windowsappruntimeinstall-x64.exe "https://aka.ms/windowsappsdk/2.3/2.3.1/windowsappruntimeinstall-x64.exe"
    windowsappruntimeinstall-x64.exe --quiet

.. node::

    All stable 2.x runtimes share the `Microsoft.WindowsAppRuntime.2` package family.
    A newer runtime (e.g. 2.2.0) supersedes an older one (e.g. 2.1.3) in place and remains compatible with the `wasdk` pip package.

************************
Getting Started Examples
************************

The following examples provide step-by-step instructions to help you get started with Windows ML on AMD Ryzen AI PCs. These examples cover CNN, Transformer, and LLM model deployment using both C++ and Python APIs.

- `Getting Started Example for Windows ML <https://github.com/amd/RyzenAI-SW/tree/main/WinML/CNN/ResNet>`_ using ResNet model:

  -  Optional Model conversion to QDQ quantized ONNX model using `VS Code AI Toolkit <https://code.visualstudio.com/docs/intelligentapps/modelconversion>`_
  - `Deployment using Windows ML APIs and ONNX Runtime using C++ and Python <https://github.com/amd/RyzenAI-SW/tree/main/WinML/CNN/ResNet>`_

- Additional examples:

  - `Transformer based GoogleBERT example <https://github.com/amd/RyzenAI-SW/tree/main/WinML/Transformers/GoogleBERT>`_
  - `Running OpenAI CLIP model on NPU <https://github.com/amd/RyzenAI-SW/tree/main/WinML/Transformers/clip-vit-base-patch16>`_
  - `Running LLM models on NPU <https://github.com/amd/RyzenAI-SW/tree/main/WinML/LLM>`_

For more details about model deployment using Windows ML, see the :doc:`Model Deployment using Windows ML documentation <model_deployment>`.

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
