############################
OnnxRuntime GenAI (OGA) Flow 
############################

Ryzen AI Software supports deploying LLMs on Ryzen AI PCs using the native ONNX Runtime Generate (OGA) C++ or Python API. The OGA API is the lowest-level API available for building LLM applications on a Ryzen AI PC. Two execution modes are supported:

- Hybrid execution mode: This mode uses both the NPU and iGPU to achieve the best TTFT and TPS during the prefill and decode phases.
- NPU-only execution mode: This mode uses the NPU exclusively for both the prefill and decode phases.


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


Hugging Face collection of hybrid models: https://huggingface.co/collections/amd/ryzenai-14-llm-hybrid-models-67da31231bba0f733750a99c

Hugging Face collection of NPU models: https://huggingface.co/collections/amd/ryzenai-14-llm-npu-models-67da3494ec327bd3aa3c83d7


*******************
Compatible OGA APIs
*******************

Pre-optimized hybrid or NPU LLMs can be executed using the official OGA C++ and Python APIs. The current release is compatible with OGA version 0.7.0.
For detailed documentation and examples, refer to the official OGA repository:
🔗 https://github.com/microsoft/onnxruntime-genai/tree/rel-0.7.0


The steps for deploying the pre-optimized models using Python or C++ are described in the following sections.

***************************
C++ Execution of OGA Models
***************************

The Ryzen AI installer provides a test C++ executable ``model_benchmark.exe`` that can be run to understand the C++ DLL dependencies.

1. Enabling Performance Mode (Optional): To run the LLMs in the best performance mode, follow these steps:

- Go to ``Windows`` → ``Settings`` → ``System`` → ``Power`` and set the power mode to Best Performance.
- Execute the following commands in the terminal:

.. code-block::

   cd C:\Windows\System32\AMD
   xrt-smi configure --pmode performance

2. Activate the Ryzen AI 1.5.0 Conda environment:

.. code-block:: 
    
    conda activate ryzen-ai-1.5.0

3. Copy necessary DLLs

Create a folder to run the LLM from, and copy the required files:

.. code-block::
  
     mkdir llm_run
     cd llm_run

     #Copy sample C++ executable 
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\model_benchmark.exe" .

     #Copy sample prompt file
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\amd_genai_prompt.txt" .

     #Common DLL
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime-genai.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\libprotobuf.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\dyn_dispatch_core.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\xaiengine.dll" .


     ## Hybrid DLL
     # Copy DLLs required to run Hybrid, you may skip if running NPU-only model
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\ryzen_mm.dll" . 
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnx_custom_ops.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\ryzenai_onnx_utils.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\DirectML.dll" .

     ## NPU-only DLL
     # Copy DLLs required to run NPU-only, you may skip if running Hybrid model
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime_providers_shared.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime_providers_vitisai.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime_vitis_ai_custom_ops.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime_vitisai_ep.dll" .


4. Download the desired models from the list of pre-optimized models on Hugging Face:


.. code-block:: 
    
     # Make sure you have git-lfs installed (https://git-lfs.com) 
     git lfs install  
     
     #git clone <link to hf model> 
     git clone https://huggingface.co/amd/Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid


5. Run test ``model_benchmark.exe``


.. code-block::

     # Example command
     #.\model_benchmark.exe -i $path_to_model_dir  -f $prompt_file -l $list_of_prompt_lengths

     .\model_benchmark.exe -i Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid -f amd_genai_prompt.txt -l "1024" 


******************************
Python Execution of OGA Models
******************************

Run sample python script 

.. code-block:: 

     #Example command
     #python "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\run_model.py" -m <model_folder> -l <max_length>

     python "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\run_model.py" -m "Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid" -l 256


**************************************
Build C++ application from OGA C++ API
**************************************

To see a sample C++ code and build process visit RyzenAI-SW repo: https://github.com/amd/RyzenAI-SW/tree/main/example/llm/oga_api

**Testing note:** Currently the script is present in https://gitenterprise.xilinx.com/VitisAI/RyzenAI-SW/tree/dev/example/llm/oga_api . It will be merged with amd/RyzenAI-SW post testing.




****************
LLM Config Files
****************

Each OGA model folder contains a ``genai_config.json`` file. This file contains various configuration settings for the model. The ``session_option`` section is where information about specific runtime dependencies is specified. Within this section, the ``custom_ops_library`` option sets the path to the ``onnxruntime_custom_ops.dll`` file. 

The sample below shows the defaults for the AMD pre-optimized Hybrid OGA LLMs:

.. code-block:: json

       "session_options": {
           "log_id": "onnxruntime-genai",
           "custom_ops_library": "onnx_custom_ops.dll",
           ...


The paths is relative to the folder where the program is run from. The model will error out if the ``onnxruntime_custom_ops.dll`` file cannot be found at the specified location. Replacing the relative path with an absolute path to this file allows running the program from any location.


***********************
Using Fine-Tuned Models
***********************

It is also possible to run fine-tuned versions of the pre-optimized OGA models. 

To do this, the fine-tuned models must first be prepared for execution with the OGA Hybrid flow. For instructions on how to do this, refer to the page about :doc:`oga_model_prepare`.

Once a fine-tuned model has been prepared for Hybrid execution, it can be deployed by following the steps described above in this page.
