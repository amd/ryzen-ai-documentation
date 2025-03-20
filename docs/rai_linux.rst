************************
Ryzen AI Linux Installer
************************

This guide provides instructions for using Ryzen AI 1.4 on Linux for model compilation and followed by running inference on windows.

Prerequisites
~~~~~~~~~~~~~
The following are the recommended system configuration for RyzenAI Linux installer

- Recommeded RAM 32GB or Higher
- Minimum 8 CPU cores or Higher
- Ubuntu 22.04
- Python 3.10 or Higher

Linux Installation
~~~~~~~~~~~~~~~~~~
- Download the RyzenAI Software Linux installer :download:`ryzen_ai-1.4.0.tgz <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=ryzen_ai-1.4.0-ea.tgz>`.

- Use the installation script as shown below:

.. code-block::

    tar -xvzf ryzen_ai-1.4.0.tgz -C <EXTRACT TO DIR>
    cd <TARGET DIR>
    ./install_ryzen_ai_1_4.sh -a yes -p <TARGET PATH TO VENV> -l
    source <TARGET PATH TO VENV>/bin/activate

- Use Docker to install the Ryzen AI Software :download:`ryzen_ai_docker-1.4.0-ea_2025_02_21_3914.tgz <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=ryzen_ai_docker-1.4.0-ea_2025_02_21_3914.tgz>`.

- Installation command:

.. code-block::

    gunzip -c ryzen_ai_docker-1.4.0-ea_2025_02_21_3914.tgz | docker load


Model Compilation
~~~~~~~~~~~~~~~~~

The input FP32/BF16 models are compiled for the NPU when an ONNX inference session is created using the Vitis AI Execution Provider (VAI EP):

.. code-block:: python

  providers = ['VitisAIExecutionProvider']
  session = ort.InferenceSession(model, sess_options = sess_opt,
                                            providers = providers,
                                            provider_options = provider_options)

.. note::
   Linux machines only support model compilation. They don't have the model runtime to run inference on the compiled model

Running Model on Windows system
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After successful model compilation on Linux machine, copy the entire working directory to a STX based Windows machine

Prerequisites
~~~~~~~~~~~~~

The following are the required system setting for runing the compiled model on RyzenAI windows system

- Strix Point AI PC, Windows 11 with latest NPU driver (Version:32.0.203.255, Date:02/20/2025) installed
- Ensure Anaconda is installed and Conda/Scripts is set to the windows System PATH variable
- LLVM/clang driver: https://github.com/llvm/llvm-project/releases/download/llvmorg-17.0.1/LLVM-17.0.1-win64.exe
  - Check "Add LLVM to the System PATH for all users"
  - Use the default installation: C:\Program Files\LLVM
- Visual Studio 2022 Community: Install "Desktop Development with C++"

Model Deployment
~~~~~~~~~~~~~~~~

The compiled model in the working directory is used by the ONNX runtime session and run inference using VitisAI Execution provider.

For more details about how to run BF16 model on NPU refer to: 
  - `Image Classification <https://github.com/amd/RyzenAI-SW/tree/main/example/image_classification>`_
  - `Finetuned DistilBERT for Text Classification <https://github.com/amd/RyzenAI-SW/tree/main/example/DistilBERT_text_classification_bf16>`_ 
  - `Text Embedding Model Alibaba-NLP/gte-large-en-v1.5  <https://github.com/amd/RyzenAI-SW/tree/main/example/GTE>`_ 

