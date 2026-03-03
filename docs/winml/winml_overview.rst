==============================
Windows ML
==============================

Microsoft provides a comprehensive AI platform for Windows that enables developers to build intelligent applications running locally on the device. The platform spans three key pillars: **Windows AI APIs**, **Foundry Local**, and **Windows ML**. For more details, refer to the official documentation, see: `Windows AI Developer Portal <https://developer.microsoft.com/en-us/windows/ai/>`_

.. image:: ../images/winml-sw.png
   :align: center

Windows Foundry Components
~~~~~~~~~~~~~~~~~~~~~~~~~~

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


************************************
Model Deployment using Windows ML
************************************

Windows Machine Learning (WinML) enables C#, C++, and Python developers to run ONNX AI models locally on Windows PCs through ONNX Runtime, with automatic execution provider management across hardware targets including CPUs, GPUs, and NPUs. You can use models from PyTorch, TensorFlow/Keras, TensorFlow Lite (TFLite), scikit-learn, and other frameworks by converting them to ONNX for ONNX Runtime.

In short, Windows ML provides a shared, Windows-wide ONNX Runtime along with support for dynamically downloading execution providers (EPs).

For more details, see the `Windows ML official documentation <https://learn.microsoft.com/en-us/windows/ai/new-windows-ml/overview>`_.

*************
Prerequisites
*************

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

*************
Installation
*************

- Install the latest NPU drivers following `RAI installation instructions <../inst.rst>`_
- Windows ML is included as part of the Windows App SDK, so installing it will also install Windows ML and its dependencies. Download and install a compatabile version of the `Windows App SDK 1.8.5 <https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/downloads>`_ or later version.


Key Features
~~~~~~~~~~~~

Windows ML handles the complexity of package management and hardware selection, automatically downloading the latest execution providers compatabile with your device's hardware.

- Dynamically gets latest EPs for different hardware
- Shared Windows-wide ONNX Runtime, which reduces application size
- Broad hardware support across different vendors through ONNX Runtime


***************************************
Running CNN / Transformer models on NPU
***************************************

Windows ML provides a streamlined workflow for deploying CNN and Transformer models on Ryzen AI PCs. Users can either use the original float model with automatic BF16 conversion, or use AI Toolkit for model quantization (QDQ format).

Workflow Overview
~~~~~~~~~~~~~~~~~

.. image:: ../images/winml-workflow.png
   :align: center

**Step 1: Download the Original Float Model**

Start with your pre-trained ONNX model in FP32 format. Models can be exported from PyTorch, TensorFlow, or obtained from model repositories.

**Step 2: (Optional) Model Quantization using VS AI Toolkit**

For improved inference performance, quantize your model using VS AI Toolkit or Olive recipe:

- **A8W8 quantization**: Recommended for CNN models (ResNet, MobileNet, etc.)
- **A16W8 quantization**: Recommended for Transformer models (BERT, CLIP etc.)

**Step 3: Automatic Execution Provider Registration**

Windows ML automatically downloads and registers the appropriate execution providers based on available hardware:

.. list-table::
   :widths: 35 65
   :header-rows: 1

   * - Execution Provider
     - Hardware Target
   * - VitisAIExecutionProvider
     - AMD Ryzen AI NPU
   * - MIGraphXExecutionProvider
     - AMD GPU (ROCm)
   * - DmlExecutionProvider
     - DirectML (GPU/NPU)

**Step 4: Model Compilation**

The model is compiled for the target hardware:

- **Float models**: VAIML performs automatic BF16 conversion for NPU execution
- **Quantized models**: A8W8/A16W8 models are compiled using X2/X1 compiler

For more details refer to `model compilation and deployment <../modelrun.rst>`_ documentation.

**Step 5: Hardware Selection and Execution**

Select the preferred execution target using the execution policy:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Execution Policy
     - First Preference EP
   * - PREFER_CPU
     - CPUExecutionProvider
   * - PREFER_GPU
     - DmlExecutionProvider
   * - PREFER_NPU
     - VitisAIExecutionProvider

For details of the API walkthrough, see the `Model Deployment with Windows ML <model_deployment.rst>`_ documentation. 


*************************
Running LLM models on NPU
*************************

Windows ML enables support for Foundry Local models for on-device AI inference solutions that provide privacy and performance. Currently, Foundry Local is available in preview mode. It automatically detects NPU and downloads the compatible model for the NPU device.

Prerequisites
~~~~~~~~~~~~~

Make sure the following requirements are met before proceeding:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Requirement
     - Details
   * - Operating System
     - Windows 10 (x64), Windows 11 (x64/ARM), Windows Server 2025, macOS
   * - Hardware (Minimum)
     - 8 GB RAM, 3 GB free disk space
   * - Hardware (Recommended)
     - 16 GB RAM, 15 GB free disk space
   * - Network
     - Internet connection to download the initial model (optional for offline use)
   * - Acceleration (Optional)
     - AMD GPU (6000 series or newer) or AMD NPU

Running LLM on AMD NPU
~~~~~~~~~~~~~~~~~~~~~~

LLM models can be run on AMD NPU using Foundry Local or Windows ML APIs. Foundry Local provides an easy-to-use interface for running LLM models on AMD NPU, while Windows ML APIs allow for more customization and control over the inference process.

**Option 1: Running LLM using Foundry Local**

This is the recommended option for most users as it provides a simple and efficient way to run LLM models on AMD NPU without needing to manage dependencies or optimize the model manually.

**Option 2: Running Custom LLM model using Foundry Local**

This option allows users to run their custom LLM models on AMD NPU using Foundry Local. Users can use the Olive ``auto-opt`` command to download, convert, quantize, and optimize their custom LLM models for AMD NPU.

**(TBD) Option 3: Run pre-quantized LLM model from AMD using Foundry Local**

This option allows users to run pre-quantized and performance-optimized LLM models from AMD on AMD NPU using Foundry Local.

**(TBD)Option 4: Running LLM model using Windows ML APIs**

This option allows users to run LLM models on AMD NPU using Windows ML APIs. This option is suitable for users who want more control over the inference process and are comfortable managing dependencies and model optimization manually.

For detailed instructions on each option, see the `Running LLM Models on NPU <https://github.com/amd/RyzenAI-SW/tree/main/WinML/LLM>`_ documentation.


******************************
Getting Started Tutorials
******************************

- `Getting Started Tutorial for Windows ML <winml_example.rst>`_ - Using ResNet model:

  -  Optional Model conversion to QDQ quantized ONNX model using `VS Code AI Toolkit <https://code.visualstudio.com/docs/intelligentapps/modelconversion>`_
  - `Deployment using Windows ML APIs and ONNX Runtime using C++ and Python <winml_example.rst>`_

- Additional examples:

  - `Transformer based GoogleBERT example <https://github.com/amd/RyzenAI-SW/tree/main/WinML/Transformers/GoogleBERT>`_
  - `Running LLM models on NPU <https://github.com/amd/RyzenAI-SW/tree/main/WinML/LLM>`_

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
