:orphan:

######################
OGA NPU Execution Mode
######################

Ryzen AI Software supports deploying LLMs on Ryzen AI PCs using the native ONNX Runtime Generate (OGA) C++ or Python API. The OGA API is the lowest-level API available for building LLM applications on a Ryzen AI PC. This documentation covers the NPU execution mode for LLMs, which utilizes only the NPU.  

**Note**: Refer to :doc:`hybrid_oga` for Hybrid NPU + GPU execution mode.



Supported Configurations
~~~~~~~~~~~~~~~~~~~~~~~~

The Ryzen AI OGA flow supports Strix and Krackan Point processors. Phoenix (PHX) and Hawk (HPT) processors are not supported.

Requirements
~~~~~~~~~~~~
- Install NPU Drivers and RyzenAI MSI installer according to the instructions https://ryzenai.docs.amd.com/en/latest/inst.html. 
- Install Git for Windows (needed to download models from HF): https://git-scm.com/downloads

Setting performance mode (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run the LLMs in the best performance mode, follow these steps:

- Go to ``Windows`` → ``Settings`` → ``System`` → ``Power`` and set the power mode to Best Performance.
- Execute the following commands in the terminal:

.. code-block::

   cd C:\Windows\System32\AMD
   xrt-smi configure --pmode performance


Pre-optimized Models
~~~~~~~~~~~~~~~~~~~~

AMD provides a set of pre-optimized LLMs ready to be deployed with Ryzen AI Software and the supporting runtime for NPU execution. These models can be found on Hugging Face in the following collection:

- https://huggingface.co/amd/Phi-3-mini-4k-instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Phi-3.5-mini-instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Mistral-7B-Instruct-v0.3-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Qwen1.5-7B-Chat-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/chatglm3-6b-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Llama2-7b-chat-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Llama-3-8B-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Llama-3.1-8B-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Llama-3.2-1B-Instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Llama-3.2-3B-Instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/DeepSeek-R1-Distill-Llama-8B-awq-g128-int4-asym-bf16-onnx-ryzen-strix	
- https://huggingface.co/amd/DeepSeek-R1-Distill-Qwen-1.5B-awq-g128-int4-asym-bf16-onnx-ryzen-strix	
- https://huggingface.co/amd/DeepSeek-R1-Distill-Qwen-7B-awq-g128-int4-asym-bf16-onnx-ryzen-strix	
- https://huggingface.co/amd/AMD-OLMo-1B-SFT-DPO-awq-g128-int4-asym-bf16-onnx-ryzen-strix

The steps for deploying the pre-optimized models using C++ and python are described in the following sections.

NPU Execution of OGA Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Setup
@@@@@

1. Install Ryzen AI 1.4 according to the instructions if not installed previously: https://ryzenai.docs.amd.com/en/latest/inst.html

2. Activate the Ryzen AI 1.4 Conda environment:

.. code-block:: 
    
    conda activate ryzen-ai-1.4.0

NOTE: pre-built versions of the ``run_llm.exe`` and ``model_generate.exe`` executables are already available in the ``%RYZEN_AI_INSTALLATION_PATH%/npu-llm/exe`` folder. If you choose to use them directly, you can skip to step 5 and copy the executables to ``%RYZEN_AI_INSTALLATION_PATH%/npu-llm/libs``. Otherwise follow the steps below to build the applications from source. 

3. Open command prompt and navigate to the ``%RYZEN_AI_INSTALLATION_PATH%/npu-llm/cpp`` folder 

.. code-block::

  # Switch to cpp folder 
  cd %RYZEN_AI_INSTALLATION_PATH%/npu-llm/cpp

4. Compile 

.. code-block::
 
   cmake -G "Visual Studio 17 2022" -A x64 -S . -B build 
   cd build 
   cmake --build . --config Release 

**Note**: The executable created ``run_llm.exe`` and ``model_generate.exe`` can be found in ``%RYZEN_AI_INSTALLATION_PATH%/npu-llm/cpp/build/Release`` folder 

 
5. Copy the executables ``run_llm.exe`` and ``model_generate.exe`` to the ``npu-llm/libs`` folder. The ``npu-llm/libs`` should contain both: ``run_llm.exe``, ``model_benchmark.exe`` along with the ``.dll`` files it contains. 
 
.. code-block::

   cd %RYZEN_AI_INSTALLATION_PATH%\npu-llm
   xcopy .\cpp\build\Release\model_benchmark.exe .\libs 
   xcopy .\cpp\build\Release\run_llm.exe .\libs 

Download Models from HuggingFace
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

1. Navigate to the ``npu-llm`` folder: 

.. code-block:: 
    
    cd %RYZEN_AI_INSTALLATION_PATH%\npu-llm

2. Download from Hugging Face the desired models (from the list of published models):

.. code-block:: 
    
     # Make sure you have git-lfs installed (https://git-lfs.com) 
     git lfs install  
     git clone <link to hf model> 

For example, for Llama-2-7b-chat:

.. code-block:: 

     git lfs install  
     git clone https://huggingface.co/amd/Llama2-7b-chat-awq-g128-int4-asym-bf16-onnx-ryzen-strix


Run the models using C++
@@@@@@@@@@@@@@@@@@@@@@@@

**Note**: Ensure the models are cloned in the ``%RYZEN_AI_INSTALLATION_PATH%/npu-llm`` folder.

Run manually
************

To run the models using the ``run_llm.exe`` file 

.. code-block::

   cd %RYZEN_AI_INSTALLATION_PATH%/npu-llm 
   # Help 
   .\libs\run_llm.exe -h 
 
   # To enter prompt through command prompt, and default max new tokens 
   .\libs\run_llm.exe -m <model_path> 

   # For example,  
   .\libs\run_llm.exe -m .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix 

   # To provide max new tokens value which is set to 32 by default 
   .\libs\run_llm.exe -m <model_path> -n <max_new_tokens>  

   # For example, 
   .\libs\run_llm.exe -m .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix -n 20 

   # To provide prompts through a prompt file 
   .\libs\run_llm.exe -m <model_path> -n <max_new_tokens> -f <model_path>\<prompts.txt> 

   # For example:  
   .\libs\run_llm.exe -m .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix -n 20 -f .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix\prompts.txt 

   # To use chat template 
   .\libs\run_llm.exe -m <model_path> -n <max_new_tokens> -f <model_path>\<prompts.txt> -c 

   # For example:  
   .\libs\run_llm.exe -m .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix -n 20 -f .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix\prompts.txt -c 

   # To specify prompt length 
   .\libs\run_llm.exe -m <model_path> -n <max_new_tokens> -f <model_path>\<prompts.txt> -t "list_prompt_lengths" 

   # For example,  

   .\libs\run_llm.exe -m .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix -n 20 -f .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix\prompts.txt -t "2048,1024,512,256,128" 

 
Run Benchmark
@@@@@@@@@@@@@

To run the models using the ``model_benchmark.exe`` file 
 
.. code-block::

   cd %RYZEN_AI_INSTALLATION_PATH%\npu-llm 
   # Help 
   .\libs\model_benchmark.exe -h 
   
   # Run with default settings 
   .\libs\model_benchmark.exe -i <model_path> -p <model_path>\<prompts.txt> -l "list_of_prompt_lengths" 
   
   # For example:  
   .\libs\model_benchmark.exe -i .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix -p .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix\prompts.txt -l "2048,1024,512,256,128" 

   # To specify number of tokens to generate, default 128 
   .\libs\model_benchmark.exe -i <model_path> -p <model_path>\<prompts.txt> -l "list_of_prompt_lengths" -g num_tokens 

   # For example:  
   .\libs\model_benchmark.exe -i .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix -g 20 -p .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix\prompts.txt -l "2048,1024,512,256,128" 

   # To specify number of warmup iterations before benchmarking, default: 1 
   .\libs\model_benchmark.exe -i <model_path> -p <model_path>\<prompts.txt> -l "list_of_prompt_lengths" -w num_warmup 

   # To specify number of times to repeat the benchmark, default: 5 
   .\libs\model_benchmark.exe -i <model_path> -p <model_path>\<prompts.txt> -l "list_of_prompt_lengths" -r num_iterations 

   # To specify sampling time interval for peak cpu utilization calculation, in milliseconds. Default: 250 
   .\libs\model_benchmark.exe -i <model_path> -p <model_path>\<prompts.txt> -l "list_of_prompt_lengths" -t time_in_milliseconds 

   # To show more informational output 
   .\libs\model_benchmark.exe -i <model_path> -p <model_path>\<prompts.txt> --verbose 

Run the models using Python
@@@@@@@@@@@@@@@@@@@@@@@@@@@

1. In the model directory, open the ``genai_config.json`` file located in the folder of the downloaded model. Update the value of the "custom_ops_library" key with the full path to the ``onnxruntime_vitis_ai_custom_ops.dll``, located in the ``%RYZEN_AI_INSTALLATION_PATH%\npu-llm\libs`` folder:  

.. code-block::
  
      "session_options": {
                ...
                "custom_ops_library": "C:\\Program Files\\RyzenAI\\1.4.0\\npu-llm\\libs\\onnxruntime_vitis_ai_custom_ops.dll",
                ...
      }

2. To run using the native OGA Python APIs, use the following commands. 

.. code-block::

   (ryzen-ai-1.4.0) cd %RYZEN_AI_INSTALLATION_PATH%/npu-llm
   

- To run any model other than chatglm: 

.. code-block:: 

     (ryzen-ai-1.4.0)python "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\python\llama3\run_model.py" --model_dir <model folder>  

- To run chatglm: 

.. code-block:: 

     #chatglm needs transformers 4.44.0 
     (ryzen-ai-1.4.0)pip install transformers==4.44.0  
     (ryzen-ai-1.4.0)python "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\python\chatglm\run_model.py" --model_dir <model folder>  

 
Preparing OGA Models for NPU-only Execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To prepare the OGA model for NPU-only execution please refer :doc:`oga_model_prepare` 
