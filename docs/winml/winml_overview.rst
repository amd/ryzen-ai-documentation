###################
Windows ML Overview
###################

Microsoft provides a comprehensive AI platform for Windows that enables developers to build intelligent applications running locally on the device. The platform spans three key pillars: **Windows AI APIs**, **Foundry Local**, and **Windows ML**. For more details, refer to the official documentation, see: `Windows AI Developer Portal <https://developer.microsoft.com/en-us/windows/ai/>`_

.. image:: ../images/winml-sw.png
   :align: center

**************************
Windows Foundry Components
**************************

.. list-table::
   :widths: 20 55 25
   :header-rows: 1

   * - Component
     - Description
     - Documentation
   * - Windows AI APIs
     - Built-in system APIs that provide access to pre-trained AI models shipped with Windows. These APIs enable AI capabilities without bundling models, and run entirely on-device for privacy and low-latency inference. Key capabilities include `Text Recognition (OCR) <https://learn.microsoft.com/en-us/windows/ai/apis/text-recognition>`_, `Object Detection <https://learn.microsoft.com/en-us/windows/ai/apis/object-detection>`_, `Image Segmentation <https://learn.microsoft.com/en-us/windows/ai/apis/image-segmentation>`_, `Description <https://learn.microsoft.com/en-us/windows/ai/apis/image-description>`_, and `Language Detection <https://learn.microsoft.com/en-us/windows/ai/apis/language-detection>`_.
     - `Windows AI APIs documentation <https://learn.microsoft.com/en-us/windows/ai/apis/>`_
   * - Foundry Local
     - Microsoft's on-device AI inference runtime for running large language models (LLMs) and other generative AI models locally on Windows PCs. It automatically detects available hardware accelerators (CPU, GPU, NPU) and downloads the most compatible model variant.
     - `Foundry Local documentation <https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-local/get-started>`_
   * - Windows ML
     - Runtime layer that manages ONNX Runtime execution providers and hardware acceleration. It works alongside Windows AI APIs and Foundry Local to provide a unified deployment path for ONNX AI models across CPUs, GPUs, and NPUs.
     - `Windows ML official documentation <https://learn.microsoft.com/en-us/windows/ai/new-windows-ml/overview>`_


***********************
Windows ML Installation
***********************

Windows Machine Learning (WinML) enables C#, C++, and Python developers to run ONNX AI models locally on Windows PCs through ONNX Runtime, with automatic execution provider management across hardware targets including CPUs, GPUs, and NPUs. You can use models from PyTorch, TensorFlow/Keras, TensorFlow Lite (TFLite), scikit-learn, and other frameworks by converting them to ONNX for ONNX Runtime.

In short, Windows ML provides a shared, Windows-wide ONNX Runtime along with support for dynamically downloading execution providers (EPs).

For more details, see the `Windows ML official documentation <https://learn.microsoft.com/en-us/windows/ai/new-windows-ml/overview>`_.


Prerequisites
=============

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Dependency
     - Version Requirement
   * - Windows 11
     - 24H2 (build 26100) or greater
   * - Visual Studio 2022 (for building the C++ application)
     - Latest version
   * - Visual Studio Code with AI Toolkit extension (for AI model conversion)
     - Latest version
   * - C++
     - C++20 or later
   * - Python
     - 3.10 to 3.12

For the complete list of Windows OS that are supported refer to `Windows App SDK support <https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/support>`_

Key Features
============

Windows ML handles the complexity of package management and hardware selection, automatically downloading the latest execution providers compatible with your device's hardware.

- Dynamically gets latest EPs for different hardware
- Shared Windows-wide ONNX Runtime, which reduces application size
- Broad hardware support across different vendors through ONNX Runtime

Installation
============

- Install the latest NPU drivers following :doc:`RAI installation instructions <../inst>`
- Windows ML runtime is included as part of the Windows App SDK, so installing it will also install Windows ML and its dependencies. Download and install a compatible version of the `Windows App SDK 1.8.5 <https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/downloads>`_ or later version.


*****************************
Windows ML setup verification
*****************************

Install the required python packages in the conda environment `winml_env`

.. code-block:: shell

    conda create -n winml_env python==3.11
    conda activate winml_env
    cd <RyzenAI-SW>\WinML\CNN\ResNet
    pip install --pre -r .\requirements.txt

Check installed wasdk python version and install same version of `Windows App SDK <https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/downloads>`_:

.. code-block:: shell

    conda list | findstr wasdk

Download the Windows App SDK corresponding to the wasdk version (e.g., 2.0.0.dev4) or latest and install it to ensure the WinML execution providers work correctly.

.. code-block:: shell

    curl -L -o windowsappruntimeinstall-x86.exe "https://aka.ms/windowsappsdk/2.0/2.0.0-experimental4/windowsappruntimeinstall-x86.exe"
    windowsappruntimeinstall-x86.exe --quiet

After completing the installation, run the `check_winml_setup.py` script from the `RyzenAI-SW` repository to verify the Windows ML installation. The script is available at: https://github.com/amd/RyzenAI-SW/blob/main/WinML/check_winml_setup.py

.. code-block:: shell

    cd <RyzenAI-SW>\WinML
    python check_winml_setup.py

The script will produce output similar to the following:

.. code-block:: text

    ============================================================
    WinML Setup Checker
    ============================================================
    Python: 3.11.0 (<path_to_python_installation>\python.exe)
    WASDK Python Packages:
    ----------------------------------------
      [✓] wasdk-ML: 2.0.0.dev4
      [✓] wasdk-Bootstrap: 2.0.0.dev4
    Windows App SDK Runtime:
    ----------------------------------------
    [✓] Windows App SDK: 2.0-experimental5 (internal: 0.770.2319.0)
    Installed runtimes (newest first):
        * 2.0-experimental5 (internal: 0.770.2319.0)
        - 2.0-experimental4 (internal: 0.738.2207.0)
        - 1.8 (internal: 8000.642.119.0)
        - 1.8 (internal: 8000.675.1142.0)
        - 1.8-experimental (internal: 8000.589.1529.0)
        - 1.8-preview (internal: 8000.591.1127.0)
        * Active runtime used by this checker
    Expected SDK: 2.0.0-experimental4
    ============================================================
    Status: All components installed. Please, ensure matching Windows App SDK version is Installed.

Windows App SDK version should match the wasdk python package version. If there is a mismatch, please install the correct Windows App SDK version. After installation, re-run the setup checker to verify that the correct version of Windows App SDK is installed and active.

**************************
Getting Started Tutorials
**************************

The following tutorials provide step-by-step instructions to help you get started with Windows ML on AMD Ryzen AI PCs. These examples cover CNN, Transformer, and LLM model deployment using both C++ and Python APIs.

- :doc:`Getting Started Tutorial for Windows ML <winml_example>` - Using ResNet model:

  -  Optional Model conversion to QDQ quantized ONNX model using `VS Code AI Toolkit <https://code.visualstudio.com/docs/intelligentapps/modelconversion>`_
  - :doc:`Deployment using Windows ML APIs and ONNX Runtime using C++ and Python <winml_example>`

- Additional examples:

  - `Transformer based GoogleBERT example <https://github.com/amd/RyzenAI-SW/tree/main/WinML/Transformers/GoogleBERT>`_
  - `Running OpenAI CLIP model on NPU <https://github.com/amd/RyzenAI-SW/tree/main/WinML/Transformers/clip-vit-base-path16>`_
  - `Running LLM models on NPU <https://github.com/amd/RyzenAI-SW/tree/main/WinML/LLM>`_

For more details about model deployment using Windows ML, see the :doc:`Model Deployment using Windows ML documentation <model_deployment>`.

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
