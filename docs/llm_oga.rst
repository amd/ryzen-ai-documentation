############################
OnnxRuntime GenAI (OGA) Flow 
############################

Ryzen AI Software supports deploying LLMs on Ryzen AI PCs using the native ONNX Runtime Generate (OGA) C++ or Python API. The OGA API is the lowest-level API available for building LLM applications on a Ryzen AI PC. The two execution modes are supported

- Hybrid execution mode: This mode use both NPU and iGPU to get best TTFT and TPS in prefil and decode phase. 
- NPU only execution mode: This mode use NPU only for both prefil and decode phase.

************************
Supported Configurations
************************

The Ryzen AI OGA flow supports Strix and Krackan Point processors. Phoenix (PHX) and Hawk (HPT) processors are not supported.


************
Requirements
************

- Install NPU Drivers and Ryzen AI MSI installer according to the :doc:`inst`
- Install GPU device driver: Ensure GPU device driver https://www.amd.com/en/support is installed 
- Install Git for Windows (needed to download models from HF): https://git-scm.com/downloads

********************
Pre-optimized Models
********************

AMD provides a set of pre-optimized LLMs ready to be deployed with Ryzen AI Software and the supporting runtime for hybrid execution. A list of currently supported models are below

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


Hugging Face collection of hybrid models: 

Hugging Face collection of NPU models: 

The steps for deploying the pre-optimized models using Python or C++ are described in the following sections.

***************************
C++ Execution of OGA Models
***************************

Ryzen AI installer provides a sample C++ excutable which can be run to understand C++ DLL dependency. 

Setup
=====

Activate the Ryzen AI 1.4.1 Conda environment:

.. code-block:: 
    
    conda activate ryzen-ai-1.4.1

Copy the required files in a local folder to run the LLMs from:

.. code-block::
  
     mkdir hybrid_run
     cd hybrid_run
     xcopy /Y /E "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\onnxruntime_genai\benchmark" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\amd_genai_prompt.txt" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime-genai.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnx_custom_ops.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\ryzen_mm.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\ryzenai_onnx_utils.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\DirectML.dll" .

Download Models from HuggingFace
================================

Download the desired models from the list of pre-optimized models on Hugging Face:

.. code-block:: 
    
     # Make sure you have git-lfs installed (https://git-lfs.com) 
     git lfs install  
     git clone <link to hf model> 

For example, for Llama-2-7b-chat:

.. code-block:: 

     git lfs install  
     git clone https://huggingface.co/amd/Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid


Enabling Performance Mode (Optional)
====================================

To run the LLMs in the best performance mode, follow these steps:

- Go to ``Windows`` → ``Settings`` → ``System`` → ``Power`` and set the power mode to Best Performance.
- Execute the following commands in the terminal:

.. code-block::

   cd C:\Windows\System32\AMD
   xrt-smi configure --pmode performance


Sample C++ Program 
==================

The ``model_benchmark.exe`` test application provides a simple mechanism for running and evaluating Hybrid OGA models using the native OGA C++ APIs. The source code for this application can be used a reference implementation for how to integrate LLMs using the native OGA C++ APIs.
 
The ``model_benchmark.exe`` test application can be used as follows:

.. code-block::

     # To see available options and default settings
     .\model_benchmark.exe -h

     # To run with default settings
     .\model_benchmark.exe -i $path_to_model_dir  -f $prompt_file -l $list_of_prompt_lengths
 
     # To show more informational output
     .\model_benchmark.exe -i $path_to_model_dir  -f $prompt_file --verbose

     # To run with given number of generated tokens
     .\model_benchmark.exe -i $path_to_model_dir  -f $prompt_file -l $list_of_prompt_lengths -g $num_tokens

     # To run with given number of warmup iterations
     .\model_benchmark.exe -i $path_to_model_dir  -f $prompt_file -l $list_of_prompt_lengths -w $num_warmup

     # To run with given number of iterations
     .\model_benchmark.exe -i $path_to_model_dir  -f $prompt_file -l $list_of_prompt_lengths -r $num_iterations


For example, for Llama-2-7b-chat:

.. code-block::
  
     .\model_benchmark.exe -i Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid -f amd_genai_prompt.txt -l "1024" --verbose

|

**NOTE**: The C++ source code for the ``model_benchmark.exe`` executable can be found in the ``%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\c`` folder. This source code can be modified and recompiled if necessary using the commands below.

.. code-block::
  
     :: Copy project files
     xcopy /E /I "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\c" .\sources

     :: Build project
     cd sources
     cmake -G "Visual Studio 17 2022" -A x64 -S . -B build
     cmake --build build --config Release

     :: Copy runtime DLLs
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime.dll" .\build\Release
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime-genai.dll" .\build\Release
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnx_custom_ops.dll" .\build\Release
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\ryzen_mm.dll" .\build\Release
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\ryzenai_onnx_utils.dll" .\build\Release
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\DirectML.dll" .\build\Release

The compiled ``model_benchmark.exe`` and ``run_llm.exe`` will be saved in ``sources\build\Release``.


Sample Python Scripts
=====================

To run LLMs use the following command:

.. code-block:: 

     #To see available options and default setting:
     python "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\python\run_model.py" -h
     #sample command
     python "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\python\run_model.py" -m <model_folder> -l <max_token to be generated including prompt>

For example, for Llama-2-7b-chat:

.. code-block:: 

    python "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\python\run_model.py" -m "Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid" -l 128


****************
LLM Config Files
****************

Each OGA model folder contains a ``genai_config.json`` file. This file contains various configuration settings for the model. The ``session_option`` section is where information about specific runtime dependencies is specified. Within this section, the ``custom_ops_library`` option sets the path to the ``onnxruntime_vitis_ai_custom_ops.dll`` file. 

The sample below shows the defaults for the AMD pre-optimized Hybrid OGA LLMs:

.. code-block:: json

       "session_options": {
           "log_id": "onnxruntime-genai",
           "custom_ops_library": "onnx_custom_ops.dll",
           ...


The paths is relative to the folder where the program is run from. The model will error out if the ``onnxruntime_vitis_ai_custom_ops.dll`` file cannot be found at the specified location. Replacing the relative path with an absolute path to this file allows running the program from any location.


***********************
Using Fine-Tuned Models
***********************

It is also possible to run fine-tuned versions of the pre-optimized OGA models. 

To do this, the fine-tuned models must first be prepared for execution with the OGA Hybrid flow. For instructions on how to do this, refer to the page about :doc:`oga_model_prepare`.

Once a fine-tuned model has been prepared for Hybrid execution, it can be deployed by following the steps described above in this page.
