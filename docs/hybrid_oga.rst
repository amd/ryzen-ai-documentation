############################
OnnxRuntime GenAI (OGA) Flow
############################

Ryzen AI Software supports deploying LLMs on Ryzen AI PCs using the native ONNX Runtime Generate (OGA) C++ or Python API. The OGA API is the lowest-level API available for building LLM applications on a Ryzen AI PC. It supports the following execution modes:

- Hybrid execution mode: This mode uses both the NPU and iGPU to achieve the best TTFT and TPS during the prefill and decode phases.
- NPU-only execution mode: This mode uses the NPU exclusively for both the prefill and decode phases.

.. _software-stack-table:

.. flat-table:: Ryzen AI Software Stack
   :header-rows: 1
   :class: center-table

   * - Your Python Application
     - Your LLM Stack
     - Your Native Application
   * - `Lemonade Python API* <#high-level-python-sdk>`_
     - `Lemonade Server Interface* <#server-interface-rest-api>`_
     - :rspan:`1` `OGA C++ Headers <../hybrid_oga.html>`_
   * - :cspan:`1` `OGA Python API* <https://onnxruntime.ai/docs/genai/api/python.html>`_
   * - :cspan:`2` `Custom AMD OnnxRuntime GenAI (OGA) <https://github.com/microsoft/onnxruntime-genai>`_
   * - :cspan:`2` `AMD Ryzen AI Driver and Hardware <https://www.amd.com/en/products/processors/consumer/ryzen-ai.html>`_

\* indicates open-source software (OSS).


************************
Supported Configurations
************************

The Ryzen AI OGA flow supports Strix and Krackan Point processors. Phoenix (PHX) and Hawk (HPT) processors are not supported.


************
Requirements
************

- Install NPU Drivers and Ryzen AI MSI installer. See :doc:`inst` for more details.
- Install GPU device driver: Ensure GPU device driver https://www.amd.com/en/support is installed
- Install Git for Windows (needed to download models from HF): https://git-scm.com/downloads

********************
Pre-optimized Models
********************

AMD provides a set of pre-optimized LLMs ready to be deployed with Ryzen AI Software and the supporting runtime for hybrid and/or NPU only execution.

- Phi-3-mini-4k-instruct
- Phi-3.5-mini-instruct
- Mistral-7B-Instruct-v0.3
- Qwen1.5-7B-Chat
- chatglm3-6b
- Llama-2-7b-hf
- Llama-2-7b-chat-hf
- Llama-3-8B
- Llama-3.1-8B
- Llama-3.2-1B-Instruct
- Llama-3.2-3B-Instruct
- Mistral-7B-Instruct-v0.1
- Mistral-7B-Instruct-v0.2
- Mistral-7B-v0.3
- Llama-3.1-8B-Instruct
- CodeLlama-7b-instruct-g128
- DeepSeek-R1-Distill-Llama-8B
- DeepSeek-R1-Distill-Qwen-1.5B
- DeepSeek-R1-Distill-Qwen-7B
- AMD-OLMo-1B-SFT-DPO
- Qwen2-7B
- Qwen2-1.5B
- gemma-2-2b
- Qwen2.5-1.5B-Instruct
- Qwen2.5-3B-Instruct
- Qwen2.5-7B-Instruct


Hugging Face collection of hybrid models: https://huggingface.co/collections/amd/ryzenai-15-llm-hybrid-models-6859a64b421b5c27e1e53899

Hugging Face collection of NPU models: https://huggingface.co/collections/amd/ryzenai-15-llm-npu-models-6859846d7c13f81298990db0

*******************
Compatible OGA APIs
*******************

Pre-optimized hybrid or NPU LLMs can be executed using the official OGA C++ and Python APIs. The current release is compatible with OGA version 0.7.0.
For detailed documentation and examples, refer to the official OGA repository:
🔗 https://github.com/microsoft/onnxruntime-genai/tree/rel-0.7.0


***************************
LLMs Test Programs
***************************

The Ryzen AI installation includes test programs (in C++ and Python) that can be used to run LLMs and understand how to integrate them in your application.

The steps for deploying the pre-optimized models using the sample programs are described in the following sections.


C++ Program
===========
Use the ``model_benchmark.exe`` executable to test LLMs and identify DLL dependencies for C++ applications.

1. (Optional) Enable Performance Mode

To run LLMs in best performance mode, follow these steps:

- Go to ``Windows`` → ``Settings`` → ``System`` → ``Power``, and set the power mode to **Best Performance**.
- Open a terminal and run:

  .. code-block:: bat

     cd C:\Windows\System32\AMD
     xrt-smi configure --pmode performance

2. Activate the Ryzen AI 1.5.0 Conda Environment

Run the following command:

.. code-block:: bash

   conda activate ryzen-ai-1.5.0

3. Set Up a Working Directory and Copy Required Files

Create a folder and copy the required files into it:

.. code-block:: bat

   mkdir llm_run
   cd llm_run

   :: Copy the sample C++ executable
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\model_benchmark.exe" .

   :: Copy the sample prompt file
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\amd_genai_prompt.txt" .

   :: Copy common DLLs
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime-genai.dll" .
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime.dll" .
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\ryzen_mm.dll" .

   :: Copy DLLs for Hybrid models (skip if using an NPU-only model)
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnx_custom_ops.dll" .
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\libutf8_validity.dll" .
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\abseil_dll.dll" .
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\DirectML.dll" .

   :: Copy DLLs for NPU-only models (skip if using a Hybrid model)
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime_providers_shared.dll" .
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime_providers_vitisai.dll" .
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime_vitis_ai_custom_ops.dll" .
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\dyn_dispatch_core.dll" .
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\xaiengine.dll" .
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime_vitisai_ep.dll" .

4. Download a Pre-Optimized Model from Hugging Face

Use Git LFS to download the model:

.. code-block:: bash

   :: Install Git LFS if you haven't already: https://git-lfs.com
   git lfs install

   :: Clone the model repository
   git clone https://huggingface.co/amd/Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid

5. Run ``model_benchmark.exe``

Run the benchmark using the following command:

.. code-block:: bash

   .\model_benchmark.exe -i <path_to_model_dir> -f <prompt_file> -l <list_of_prompt_lengths>

   :: Example:
   .\model_benchmark.exe -i Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid -f amd_genai_prompt.txt -l "1024"


Python Script
=============

Run sample python script

.. code-block::

     python "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\run_model.py" -m <model_folder> -l <max_length>

     :: Example command
     python "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\run_model.py" -m "Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid" -l 256


**************************************
Building C++ Applications
**************************************

A complete example including C++ source and build instructions is available in the RyzenAI-SW repository: https://github.com/amd/RyzenAI-SW/tree/main/example/llm/oga_api

****************
LLM Config Files
****************

Each OGA model folder contains a ``genai_config.json`` file. This file contains various configuration settings for the model. The ``session_option`` section is where information about specific runtime dependencies is specified. Within this section, the ``custom_ops_library`` option sets the path to the ``onnx_custom_ops.dll`` file for Hybrid models and ``onnxruntime_vitis_ai_custom_ops.dll`` file for NPU models.

The following sample shows the defaults for the AMD pre-optimized Hybrid OGA LLMs:

.. code-block:: json

       "session_options": {
           "log_id": "onnxruntime-genai",
           "custom_ops_library": "onnx_custom_ops.dll",
           ...


The paths is relative to the folder where the program is run from. The model throws an error if the ``onnx_custom_ops.dll`` file cannot be found at the specified location. Replacing the relative path with an absolute path to this file allows running the program from any location.


***********************
Using Fine-Tuned Models
***********************

It is also possible to run fine-tuned versions of the pre-optimized OGA models.

To do this, the fine-tuned models must first be prepared for execution with the OGA Hybrid flow. For instructions on how to do this, refer to the page about :doc:`oga_model_prepare`.

After a fine-tuned model has been prepared for Hybrid execution, it can be deployed by following the steps described previously in this page.

*****************************
Running LLM via pip install
*****************************

In addition to the full RyzenAI software stack, we also provide standalone wheel files for the users who prefer using their own environment. To prepare an environment for running the Hybrid and NPU-only LLM independently, perform the following steps:

1. Create a new python environment and activate it.

.. code-block:: bash

   conda create -n <env_name> python=3.10 -y
   conda activate <env_name>

2. Install onnxruntime-genai wheel file.

.. code-block:: bash

   pip install onnxruntime-genai-directml-ryzenai==0.7.0.2 --extra-index-url=https://pypi.amd.com/simple

3. Navigate to your working directory and download the desired Hybrid/NPU model

.. code-block:: bash

   cd working_directory
   git clone <link_to_model>

4. Copy the required DLLs from the current environment folder.

.. code-block:: bat

   :: Copy DLLs for Hybrid models (skip if using an NPU-only model)
   xcopy "%CONDA_PREFIX%\Lib\site-packages\onnxruntime_genai\onnx_custom_ops.dll" .
   xcopy "%CONDA_PREFIX%\Lib\site-packages\onnxruntime_genai\libutf8_validity.dll" .
   xcopy "%CONDA_PREFIX%\Lib\site-packages\onnxruntime_genai\abseil_dll.dll" .
  
   :: Copy DLLs for NPU-only models (skip if using a Hybrid model)
   xcopy "%CONDA_PREFIX%\Lib\site-packages\onnxruntime\capi\onnxruntime_vitis_ai_custom_ops.dll" .
   xcopy "%CONDA_PREFIX%\Lib\site-packages\onnxruntime\capi\dyn_dispatch_core.dll" .
   xcopy "%CONDA_PREFIX%\Lib\site-packages\onnxruntime\capi\xaiengine.dll" .

5. Run the Hybrid or NPU model.
