#####################################
OGA Flow for Hybrid Execution of LLMs
#####################################

.. note::
   
   Support for LLMs is currently in the Early Access stage. Early Access features are features which are still undergoing some optimization and fine-tuning. These features are not in their final form and may change as we continue to work in order to mature them into full-fledged features.

Ryzen AI Software includes support for deploying LLMs on Ryzen AI PCs using the ONNX Runtime generate() API (OGA). This documentation is for the Hybrid execution mode of LLMs, which leverages both the NPU and GPU.

Supported Configurations
~~~~~~~~~~~~~~~~~~~~~~~~

The Ryzen AI OGA flow supports the following processors running Windows 11:

- Strix (STX): AMD Ryzen™ Ryzen AI 9 HX375, Ryzen AI 9 HX370, Ryzen AI 9 365
- Kracken (KRK)

**Note**: Phoenix (PHX) and Hawk (HPT) processors are not supported.

Requirements
~~~~~~~~~~~~
- NPU Drivers (version .255): Install according to the instructions https://ryzenai.docs.amd.com/en/latest/inst.html
- RyzenAI 1.4 MSI installer
- GPU device driver: Ensure GPU device driver https://www.amd.com/en/support is installed 
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

AMD provides a set of pre-optimized LLMs ready to be deployed with Ryzen AI Software and the supporting runtime for hybrid execution. These models can be found on Hugging Face: 

Published models: 

https://huggingface.co/amd/DeepSeek-R1-Distill-Llama-8B-awq-asym-uint4-g128-lmhead-onnx-hybrid 

https://huggingface.co/amd/Phi-3-mini-4k-instruct-awq-g128-int4-asym-fp16-onnx-hybrid 

https://huggingface.co/amd/Phi-3.5-mini-instruct-awq-g128-int4-asym-fp16-onnx-hybrid 

https://huggingface.co/amd/Mistral-7B-Instruct-v0.3-awq-g128-int4-asym-fp16-onnx-hybrid 

https://huggingface.co/amd/Qwen1.5-7B-Chat-awq-g128-int4-asym-fp16-onnx-hybrid 

https://huggingface.co/amd/chatglm3-6b-awq-g128-int4-asym-fp16-onnx-hybrid 

https://huggingface.co/amd/Llama-2-7b-hf-awq-g128-int4-asym-fp16-onnx-hybrid 

https://huggingface.co/amd/Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid 

https://huggingface.co/amd/Llama-3-8B-awq-g128-int4-asym-fp16-onnx-hybrid/tree/main 

https://huggingface.co/amd/Llama-3.1-8B-awq-g128-int4-asym-fp16-onnx-hybrid/tree/main 

https://huggingface.co/amd/Llama-3.2-1B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid 

https://huggingface.co/amd/Llama-3.2-3B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid 

https://huggingface.co/uday610/Mistral-7B-Instruct-v0.1-hybrid 

https://huggingface.co/uday610/Mistral-7B-Instruct-v0.2-hybrid 

https://huggingface.co/uday610/Mistral-7B-v0.3-hybrid 

https://huggingface.co/uday610/Llama-3.1-8B-Instruct-hybrid 

https://huggingface.co/amd/CodeLlama-7b-instruct-g128-hybrid 

DeepSeek-R1-Distill-Qwen-1.5B (will be enabled)

DeepSeek-R1-Distill-Qwen-7B (will be enabled)

Gemma2-2B (will be enabled)

The steps for deploying the pre-optimized models using Python or C++ are described in the following sections.

Hybrid Execution of OGA Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Setup
@@@@@

1. Install Ryzen AI 1.4 according to the instructions if not installed previously: https://ryzenai.docs.amd.com/en/latest/inst.html

2. Activate the Ryzen AI 1.4 Conda environment:

.. code-block:: 
    
    conda activate ryzen-ai-1.4.0

3. Create a folder to run the LLMs from, and copy the required files:

.. code-block::
  
       xcopy "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\onnxruntime_genai\benchmark" .\run_folder /e /i  
       xcopy "%RYZEN_AI_INSTALLATION_PATH%\onnxruntime\bin\onnxruntime.dll" run_folder\. 
       xcopy "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\amd_genai_prompt.txt" run_folder\. 
       xcopy "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\onnx_utils\bin\onnx_custom_ops.dll" run_folder\.
       xcopy "%RYZEN_AI_INSTALLATION_PATH%\onnxruntime\bin\DirectML.dll run_folder\.

Download Models from HuggingFace
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

1. Navigate to the newly created run folder: 

.. code-block:: 
    
    cd \path\to\run_folder

2. Download from Hugging Face the desired models (from the list of published models):

.. code-block:: 
    
     # Make sure you have git-lfs installed (https://git-lfs.com) 
     git lfs install  
     git clone <link to hf model> 

For example, for Llama-2-7b-chat:

.. code-block:: 

     git lfs install  
     git clone https://huggingface.co/amd/Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid


Run Models with OGA python APIs
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

1. To run from the run folder using the native OGA Python APIs, use the following commands. 

- To run any model other than chatglm: 

.. code-block:: 

     (ryzen-ai-1.4.0)python "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\python\llama3\run_model.py" --model_dir <model folder>  

- To run chatglm: 


.. code-block:: 

     (ryzen-ai-1.4.0)python "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\python\chatglm\run_model.py" --model_dir <model folder>  



Run Models with OGA C++ APIs 
@@@@@@@@@@@@@@@@@@@@@@@@@@@@

The ``model_benchmark.exe`` test application serves two purposes:

- It provides a very simple mechanism for running and evaluating Hybrid OGA models using the native OGA C++ APIs
- The source code for this application provides a reference implementation for how to integrate Hybrid OGA models in custom C++ programs

To evaluate models using the ``model_benchmark.exe`` test application:

.. code-block::

     # Switch to the run folder
     cd run_folder

     # To see settings info
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


For example:

.. code-block::
  
     cd run_folder
     .\model_benchmark.exe -i <path_to>/Llama-3.2-1B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid -f amd_genai_prompt.txt -l "128, 256, 512, 1024, 2048" --verbose


Preparing OGA Models for Hybrid Execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To prepare the OGA model for hybrid execution please refer :doc:`oga_model_prepare`


