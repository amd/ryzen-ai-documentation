############################
OnnxRuntime GenAI (OGA) Flow
############################

Ryzen AI Software supports deploying LLMs on Ryzen AI PCs using the native ONNX Runtime Generate (OGA) C++ or Python API. The OGA API is the lowest-level API available for building LLM applications on a Ryzen AI PC. It supports the following execution modes:

- Hybrid execution mode: This mode uses both the NPU and iGPU to achieve the best TTFT and TPS during the prefill and decode phases.
- NPU-only execution mode: This mode uses the NPU exclusively for both the prefill and decode phases.

************************
Supported Configurations
************************

The Ryzen AI OGA flow supports Strix and Krackan Point processors. Phoenix (PHX) and Hawk (HPT) processors are not supported.


************
Requirements
************

- Install NPU Drivers and Ryzen AI MSI installer. See :doc:`inst` for more details.
- Install GPU device driver: Ensure GPU device driver https://www.amd.com/en/support is installed
- Install Git for Windows (needed to download models from HF): https://git-scm.com/downloads

.. _pre_opt_model:

********************
Pre-optimized Models
********************


AMD provides a set of pre-optimized LLMs ready to be deployed with Ryzen AI Software and the supporting runtime for hybrid and/or NPU-only execution. These include popular architectures such as Llama-2, Llama-3, Mistral, DeepSeek Distill models, Qwen-2, Qwen-2.5, Qwen-3, Gemma-2, Gemma-3, GPT-OSS, Phi-3, Phi-3.5, and Phi-4. 

For the complete list of supported pre-optimized models and their available variants, see :doc:`llm_list`.
 
- Hugging Face collection of **NPU models**: https://huggingface.co/collections/amd/ryzen-ai-190-npu
- Hugging Face collection of **hybrid models**: https://huggingface.co/collections/amd/ryzen-ai-180-hybrid


************************************
Changes Compared to Previous Release
************************************

- OGA version is updated to v0.16.0 (Ryzen AI 1.9) from v0.14.0 (Ryzen AI 1.8).
- For the 1.9 release, a new set of NPU models has been published. NPU Models from earlier releases are not compatible with this version. Download the updated models.

*******************
Compatible OGA APIs
*******************

Pre-optimized hybrid or NPU LLMs can be executed using the official OGA C++ and Python APIs. The current release is compatible with OGA version 0.14.0.
For detailed documentation and examples, refer to the official OGA repository:
🔗 https://github.com/microsoft/onnxruntime-genai/tree/rel-0.16.0


***************************
LLMs Test Programs
***************************

The Ryzen AI installation includes test programs (in C++ and Python) that can be used to run LLMs and understand how to integrate them in your application.

The steps for deploying the pre-optimized models using the sample programs are described in the following sections.

Steps to run C++ program and sample python script.
==================================================

1. (Optional) Enable Performance Mode

To run LLMs in best performance mode, follow these steps:

- Go to ``Windows`` → ``Settings`` → ``System`` → ``Power``, and set the power mode to **Best Performance**.
- Open a terminal and run:

  .. code-block:: bat

     cd C:\Windows\System32\AMD
     xrt-smi configure --pmode performance

2. Activate the Ryzen AI Python Virtual Environment and install ``torch`` library.

Run the following commands:

.. code-block:: bash

   "C:\Program Files\RyzenAI\ryzen-ai-1.9.0\Scripts\activate.bat"

This step is required for running the python script.

.. note::

   For the C++ program, if you choose not to activate the Python virtual environment, open a Windows Command Prompt and manually set the environment variable before continuing:

   ``set RYZEN_AI_INSTALLATION_PATH=C:\\Program Files\\RyzenAI\\<version>``


C++ Program
===========
Use the ``model_benchmark.exe`` executable to test LLMs and identify DLL dependencies for C++ applications.

.. note::

   ``model_benchmark.exe`` is for **performance** measurement only. It feeds the model a raw or synthetic prompt without applying a chat template, so its generated text is often repetitive and is **not** meant to reflect output quality. For **instruct/chat models**, use the chat-template scripts to evaluate accuracy or produce coherent responses (see :ref:`Python Script (with Chat Template) <python-chat-template>`).

1. Set Up a working directory and copy required Files

.. code-block:: bat

   mkdir llm_run
   cd llm_run

   :: Copy the sample C++ executable
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\model_benchmark.exe" .

   :: Copy the sample prompt file
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\amd_genai_prompt.txt" .

   :: Copy required DLLs
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\." .

2. Download model from Hugging Face

.. code-block:: bash

   :: Install Git LFS if you haven't already: https://git-lfs.com
   git lfs install

   :: Clone the model repository
   git clone https://huggingface.co/amd/Llama-2-7b-chat-hf-onnx-ryzenai-hybrid

3. Run ``model_benchmark.exe``

Provide the prompt using **either** ``--prompt_file`` (a prompt text file) **or** ``-l`` (a synthetic prompt of the given token length). These options are mutually exclusive.

.. code-block:: bash

   :: Using a synthetic prompt length:
   .\model_benchmark.exe -i <path_to_model_dir> -l <prompt_length> -g <generation_length>
   :: Example:
   .\model_benchmark.exe -i Llama-2-7b-chat-hf-onnx-ryzenai-hybrid -l 1024 -g 128

   :: Using a prompt file:
   .\model_benchmark.exe -i <path_to_model_dir> --prompt_file <prompt_file> -g <generation_length>
   :: Example:
   .\model_benchmark.exe -i Llama-2-7b-chat-hf-onnx-ryzenai-hybrid --prompt_file amd_genai_prompt.txt -g 128

Key options: Run ``model_benchmark.exe --help`` for the complete list of options.


Long Context Support
====================

Ryzen AI supports long context (beyond 4096 tokens) for **Hybrid models** and **NPU models**.

NPU Models
----------

NPU models are pre-built with long context support. No additional configuration is required — simply download the model from Hugging Face and run it.

.. code-block:: bash
 
   :: Example: Clone a NPU model
   git clone https://huggingface.co/amd/Phi-3.5-mini-instruct-onnx-ryzenai-npu

   :: Run with long context (synthetic 16000-token prompt)
   .\model_benchmark.exe -i <path_to_model_dir> -l 16000 -g 128

.. note::

   The context length that can actually be used is not a fixed number. It is
   bounded by the model's own maximum sequence length, and beyond that by the
   memory available on the system. The KV cache grows linearly with context
   length, and its footprint depends on the model's layer count, number of
   key/value heads, head dimension, and KV cache data type. A larger model, or
   a model with a wider KV cache, will run out of memory at a shorter context
   than the examples shown here. If a run fails at a given ``-l`` value, reduce
   the prompt length or use a smaller model.

Hybrid Models
-------------

If the total number of tokens exceeds 4096 for a hybrid model, follow the steps below.

**Steps to run long context:**

1. Make the following changes in ``genai_config.json`` file.

   - Add ``"hybrid_opt_chunk_context": "1"`` under ``model.decoder.session_options.provider_options.RyzenAI``.

   .. code-block:: bash

      {
      "model": {
         "bos_token_id": 1,
         "context_length": 16384,
         "decoder": {
               "session_options": {
               "log_id": "onnxruntime-genai",
               "provider_options": [
               {
                  "RyzenAI": {
                     "external_data_file": "model_jit.pb.bin",
                     "hybrid_opt_free_after_prefill": "1",
                     "hybrid_opt_max_seq_length": "4096",
                                                   "hybrid_opt_chunk_context": "1"
                  }
               }
               ]
            },


   - Add ``"chunk_size":2048`` under ``search``.

   .. code-block:: bash
 
      "search": {
            "diversity_penalty": 0.0,
            "do_sample": false,
            "chunk_size": 2048,
            ...

2. Run the model using ``model_benchmark.exe`` with a synthetic long-context prompt.

.. code-block:: bash
 
    :: Generate a 16000-token prompt and 128 output tokens
    .\model_benchmark.exe -i <path_to_model_dir> -l 16000 -g 128

.. note::

   The sample test application ``model_benchmark.exe`` accepts ``-l`` for input token length and ``-g`` for output token length.

   - The combined number of input and output tokens must not exceed the model's ``context_length``. You can verify the ``context_length`` in the ``genai_config.json`` file. For example, if a model's ``context_length`` is 8,000, the total token count (input + output) must not exceed 8,000.


Python Script
=============

This section uses a basic ``run_model.py`` sample script.
 
.. note::
 
   ``run_model.py`` does not apply a chat template. If your model uses a chat template, use :ref:`Python Script (with Chat Template) <python-chat-template>` (``model_chat.py``) instead for more accurate output.

1. Navigate to your working directory and download model.

.. code-block:: bash

   :: Install Git LFS if you haven't already: https://git-lfs.com
   git lfs install

   :: Clone the model repository
   git clone https://huggingface.co/amd/Llama-2-7b-chat-hf-onnx-ryzenai-hybrid

2. Run sample python script

.. code-block::

     python "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\run_model.py" -m <model_folder> -l <max_length>

     :: Example command
     python "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\run_model.py" -m "Llama-2-7b-chat-hf-onnx-ryzenai-hybrid" -l 256


.. _python-chat-template:

Python Script (with Chat Template)
===================================

For models that use chat templates, the ``model_chat.py`` script provides better output quality by automatically loading and applying the chat template from the model folder during inference. The script also supports single-prompt, multi-turn context cache testing, and interactive chat with timing output.

The script is included in the Ryzen AI installation:

.. code-block:: bash

   :: Single prompt with timing
   python "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\model_chat.py" -m <model_folder> -pr amd_genai_prompt.txt --timings

   :: Long context support (increase context window to e.g. 16k)
   python "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\model_chat.py" -m <model_folder> -pr amd_genai_prompt_long.txt -mpt 16000

   :: Interactive chat
   python "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\model_chat.py" -m <model_folder>

For the full list of options including multi-turn JSON testing, guided generation, and advanced flags, refer to the `RyzenAI-SW repository <https://github.com/amd/RyzenAI-SW/blob/main/LLM-examples/oga_inference/README.md>`_.

It is highly recommended to use ``model_chat.py`` for the `GPT-OSS-20B NPU model <https://huggingface.co/amd/gpt-oss-20b-onnx-ryzenai-npu>`_.


**********************************
Vision Language Model (VLM)
**********************************

AMD provides a pre-optimized Gemma-3-4b-it multimodal model ready to be deployed with Ryzen AI Software. Support for this model is available starting with the Ryzen AI 1.7 release.

Model: `Gemma-3-4b-it-mm-onnx-ryzenai-npu <https://huggingface.co/amd/Gemma-3-4b-it-mm-onnx-ryzenai-npu>`_

VLM inference requires dedicated Python scripts, which are included in the Ryzen AI installation at ``%RYZEN_AI_INSTALLATION_PATH%\LLM\example\vlm``.

Quick Inference
===============

Use ``vlm_run.py`` to quickly test a model and see output:

.. code-block:: bash

   :: Basic inference
   python "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\vlm\vlm_run.py" -m <model_folder> -i <image_path>

   :: Custom prompt
   python "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\vlm\vlm_run.py" -m <model_folder> -i <image_path> -p "What's in this image?"

   :: Resize image before running
   python "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\vlm\vlm_run.py" -m <model_folder> -i <image_path> --image_size 1024 1024

For benchmarking scripts (``vlm_benchmark.py``, ``run_all_benchmarks.py``) and detailed options, refer to the README in the ``vlm`` directory or the `RyzenAI-SW repository <https://github.com/amd/RyzenAI-SW/blob/main/LLM-examples/VLM/README.md>`_.


**************************************
Building C++ Applications
**************************************

The RyzenAI-SW repository provides a complete C++ example demonstrating how to
load a pre-optimized OGA model, apply the chat template, and run inference using
the OGA C++ API. It includes the full source and CMake build instructions.

Repository: https://github.com/amd/RyzenAI-SW/tree/main/LLM-examples/oga_api


***********************
Using Fine-Tuned Models
***********************

It is also possible to run fine-tuned versions of the pre-optimized OGA models.

To do this, the fine-tuned models must first be prepared for execution with the OGA flow. For instructions on how to do this, refer to the page about :doc:`oga_model_prepare`.

After a fine-tuned model has been prepared for execution, it can be deployed by following the steps described previously in this page.


*****************************
Running LLM with pip install
*****************************

In addition to the full RyzenAI software stack, we also provide standalone wheel files for the users who prefer using their own environment. To prepare an environment for running the Hybrid and NPU-only LLM independently, perform the following steps:

1. Create a new python environment and activate it.

.. code-block:: bash

   py -3.12 -m venv <env_name>
   <env_name>\Scripts\activate.bat

2. Install onnxruntime-genai wheel file.

.. code-block:: bash

	pip install onnxruntime-genai-directml-ryzenai==0.14.0 --extra-index-url https://pypi.amd.com/ryzenai_llm/1.8.1/windows/simple/
	pip install model-generate==1.8.0 --extra-index-url https://pypi.amd.com/ryzenai_llm/1.8.0/windows/simple/

3. Navigate to your working directory and download the desired Hybrid/NPU model

.. code-block:: bash

   cd working_directory
   git clone <link_to_model>

4. Run the Hybrid or NPU model.

