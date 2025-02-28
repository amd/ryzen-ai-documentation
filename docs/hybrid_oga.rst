##########################
OGA API for C++ and Python
##########################

.. note::
   
   Support for the OGA API is currently in the Early Access stage. Early Access features are features which are still undergoing some optimization and fine-tuning. These features are not in their final form and may change as we continue to work in order to mature them into full-fledged features.

Starting with version 1.3, the Ryzen AI Software includes support for deploying LLMs on Ryzen AI PCs using the ONNX Runtime generate() API (OGA). This documentation is for the Hybrid execution mode of LLMs, which leverages both the NPU and GPU.

Supported Configurations
~~~~~~~~~~~~~~~~~~~~~~~~

The OGA-based flow supports Strix (STX) and Krackan Point (KRK) processors running Windows 11. Phoenix (PHX) and HawkPoint (HPT) processors are not supported.

Requirements
~~~~~~~~~~~~
- NPU Drivers (version .242): Install according to the instructions https://ryzenai.docs.amd.com/en/latest/inst.html
- RyzenAI 1.3 MSI installer (NOTE: the installer is not required to run DeepSeek models)
- Latest AMD `GPU device driver <https://www.amd.com/en/support>`_ installed
- Hybrid LLM artifacts packages: 

  - For general LLMs: ``hybrid-llm-artifacts_1.3.0.zip`` from https://account.amd.com/en/member/ryzenai-sw-ea.html 
  - For DeepSeek-R1-Distill models: https://www.xilinx.com/bin/public/openDownload?filename=hybrid-llm-deepseek-Feb05.zip 

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

AMD provides a set of pre-optimized LLMs ready to be deployed with Ryzen AI Software and the supporting runtime for hybrid execution. These models can be found on Hugging Face in the following collections:

General models: https://huggingface.co/collections/amd/quark-awq-g128-int4-asym-fp16-onnx-hybrid-674b307d2ffa21dd68fa41d5

- https://huggingface.co/amd/Phi-3-mini-4k-instruct-awq-g128-int4-asym-fp16-onnx-hybrid
- https://huggingface.co/amd/Phi-3.5-mini-instruct-awq-g128-int4-asym-fp16-onnx-hybrid
- https://huggingface.co/amd/Mistral-7B-Instruct-v0.3-awq-g128-int4-asym-fp16-onnx-hybrid
- https://huggingface.co/amd/Qwen1.5-7B-Chat-awq-g128-int4-asym-fp16-onnx-hybrid
- https://huggingface.co/amd/chatglm3-6b-awq-g128-int4-asym-fp16-onnx-hybrid
- https://huggingface.co/amd/Llama-2-7b-hf-awq-g128-int4-asym-fp16-onnx-hybrid
- https://huggingface.co/amd/Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid
- https://huggingface.co/amd/Llama-3-8B-awq-g128-int4-asym-fp16-onnx-hybrid/tree/main
- https://huggingface.co/amd/Llama-3.1-8B-awq-g128-int4-asym-fp16-onnx-hybrid/tree/main
- https://huggingface.co/amd/Llama-3.2-1B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid
- https://huggingface.co/amd/Llama-3.2-3B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid

DeepSeek-R1-Distill models: https://huggingface.co/collections/amd/amd-ryzenai-deepseek-r1-distill-hybrid-67a53471e9d5f14bece775d2

- https://huggingface.co/amd/DeepSeek-R1-Distill-Llama-8B-awq-asym-uint4-g128-lmhead-onnx-hybrid
- https://huggingface.co/amd/DeepSeek-R1-Distill-Qwen-1.5B-awq-asym-uint4-g128-lmhead-onnx-hybrid
- https://huggingface.co/amd/DeepSeek-R1-Distill-Qwen-7B-awq-asym-uint4-g128-lmhead-onnx-hybrid


The steps for deploying the pre-optimized models using Python or C++ are described in the following sections.

Hybrid Execution of OGA Models using Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Setup for General Models
@@@@@@@@@@@@@@@@@@@@@@@@

.. note:: This section covers the setup required for hybrid execution of general LLMs. The setup steps for DeepSeek-R1-Distill models are covered in the :ref:`deepseek_setup` section.

1. Install Ryzen AI 1.3 according to the instructions: https://ryzenai.docs.amd.com/en/latest/inst.html

2. Download and unzip the hybrid LLM artifacts package 

3. Activate the Ryzen AI 1.3 Conda environment:

.. code-block:: 
    
    conda activate ryzen-ai-1.3.0

4. Install the wheel file included in the hybrid-llm-artifacts package:  

.. code-block::
  
       cd path_to\hybrid-llm-artifacts\onnxruntime_genai\wheel
       pip install onnxruntime_genai_directml-0.4.0.dev0-cp310-cp310-win_amd64.whl

.. _deepseek_setup:

Setup for DeepSeek Models
@@@@@@@@@@@@@@@@@@@@@@@@@

.. note:: This section covers the setup required for for hybrid execution of DeepSeek-R1-Distill models.

1. Download and unzip the hybrid LLM artifacts package 

2. Create conda environment with Python 3.10 using the below command 

.. code-block:: 
    
    conda create --name <env name> python=3.10

3. Activate the Conda environment:

.. code-block:: 
    
    conda activate <env name>

4. Install the wheel file included in the hybrid-llm-artifacts package:  

.. code-block::
  
       cd path_to\hybrid-llm-artifacts\onnxruntime_genai\wheel
       pip install onnxruntime_genai-0.4.0.dev0-cp310-cp310-win_amd64.whl

       cd path_to\hybrid-llm-artifacts\onnxruntime
       pip install onnxruntime_directml-1.20.1-cp310-cp310-win_amd64.whl
     


Run Models
@@@@@@@@@@

1. Clone model from the Hugging Face repository and switch to the model directory

2. Open the ``genai_config.json`` file located in the folder of the downloaded model. Update the value of the "custom_ops_library" key with the full path to the ``onnx_custom_ops.dll``,located in the ``hybrid-llm-artifacts\onnx_utils\bin`` folder:  

.. code-block::
  
      "session_options": {
                ...
                "custom_ops_library": "path_to\\hybrid-llm-artifacts\\onnx_utils\\bin\\onnx_custom_ops.dll",
                ...
      }

3. Copy the ``DirectML.dll`` file to the folder where the ``onnx_custom_ops.dll`` is located (note: this step is only required on some systems)

.. code-block::
  
       copy hybrid-llm-artifacts\onnxruntime_genai\lib\DirectML.dll hybrid-llm-artifacts\onnx_utils\bin

4. Run the LLM 

.. code-block::

     cd <path_to_hybrid-package>\examples\python\llama3
     python run_model.py --model_dir path_to\Meta-Llama-3-8B-awq-w-int4-asym-gs128-a-fp16-onnx-ryzen-strix-hybrid

.. note:: The ``run_model.py`` script included in the hybrid-llm-artefacts package is a **general-purpose inference script**. To optimize it for specific models, adjust the ``get_prompt()`` function in the inference script. For example for DeepSeek-R1 models, you can modify the chat template to include ``<think>\n`` at the start of the assistants response `(See: Usage Recommendations) <https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B#usage-recommendations>`_ as shown below:

.. code-block::

   def get_prompt():
      chat_template = f'<|user|>\n{{input}} <|end|>\n<|assistant|>\n<think>\n'
      ...

Hybrid Execution of OGA Models using C++
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Setup
@@@@@

1. Download and unzip the hybrid LLM artifacts package.

2. Copy required library files from ``onnxruntime-genai\lib`` to ``examples\c\lib`` 

.. code-block::

    copy onnxruntime_genai\lib\*.* examples\c\lib\

3. Copy ``onnx_utils\bin\ryzenai_onnx_utils.dll``  to ``examples\c\lib`` 

.. code-block::

    copy onnx_utils\bin\ryzenai_onnx_utils.dll examples\c\lib\

4. Copy required header files from ``onnxruntime-genai\include`` to ``examples\c\include``

.. code-block::

     copy onnxruntime_genai\include\*.* examples\c\include\

5. Build the ``model_benchmark.exe`` application

.. code-block::

     cd hybrid-llm-artifacts\examples\c
     cmake -G "Visual Studio 17 2022" -A x64 -S . -B build
     cd build
     cmake --build . --config Release

**Note**: The ``model_benchmark.exe`` executable is generated in the ``hybrid-llm-artifacts\examples\c\build\Release`` folder

6. Clone model from the Hugging Face repository and switch to the model directory

7. Open the ``genai_config.json`` file located in the folder of the downloaded model. Update the value of the "custom_ops_library" key with the full path to the ``onnx_custom_ops.dll``, located in the ``hybrid-llm-artifacts\onnx_utils\bin`` folder:  

.. code-block::

      "session_options": {
                ...
                "custom_ops_library": "path_to\\hybrid-llm-artifacts\\onnx_utils\\bin\\onnx_custom_ops.dll",
                ...
      }

Run Models
@@@@@@@@@@

The ``model_benchmark.exe`` test application serves two purposes:

- It provides a very simple mechanism for running and evaluating Hybrid OGA models
- The source code for this application provides a reference implementation for how to integrate Hybrid OGA models in custom C++ programs

To evaluate models using the ``model_benchmark.exe`` test application:

.. code-block::

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
  
     cd hybrid-llm-artifacts\examples\c\build\Release
     .\model_benchmark.exe -i <path_to>/Llama-3.2-1B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid -f <path_to>/prompt.txt -l "128, 256, 512, 1024, 2048" --verbose

 
**Note:** A sample prompt file is provided in the package at ``hybrid-llm-artifacts\examples\amd_genai_prompt.txt``

Preparing OGA Models for Hybrid Execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section describes the process for preparing LLMs for deployment on a Ryzen AI PC using the hybrid execution mode. Currently, the flow supports only fine-tuned versions of the models already supported (as listed in "Pre-optimized Models" section of this guide) in the hybrid flow. For example, fine-tuned versions of Llama2 or Llama3 can be used. However, different model families with architectures not supported by the hybrid flow cannot be used.

Preparing a LLM for deployment on a Ryzen AI PC using the hybrid execution mode involves 3 steps:

1. Quantizing the model: The pretrained model is quantized to reduce memory footprint and better map to compute resources in the hardware accelerators
2. Generating the OGA model: A model suitable for use with the ONNX Runtime generate() API (OGA) is generated from the quantized model.
3. Generating the final model for Hybrid execution: A model specialized for the hybrid execution mode is generated from the OGA model.

Quantizing the model
@@@@@@@@@@@@@@@@@@@@

Prerequisites
*************
Linux machine with AMD or Nvidia GPUs

Setup
*****

1. Create Conda Environment 

.. code-block::

    conda create --name <conda_env_name> python=3.11
    conda activate <conda_env_name>

2. If Using AMD GPUs, update PyTorch to use ROCm 

.. code-block:: 
  
     pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.1
     python -c "import torch; print(torch.cuda.is_available())" # Must return `True`

3. Download :download:`Quark 0.6.0 <https://www.xilinx.com/bin/public/openDownload?filename=quark-0.6.0.zip>` and unzip the archive

4. Install Quark: 

.. code-block::

     cd <extracted quark 0.6.0>
     pip install quark-0.6.0+<>.whl

Perform quantization
********************

The model is quantized using the following command and quantization settings:

.. code-block::

     cd examples/torch/language_modeling/llm_ptq/
     python3 quantize_quark.py 
        --model_dir "meta-llama/Llama-2-7b-chat-hf" 
        --output_dir <quantized safetensor output dir> 
        --quant_scheme w_uint4_per_group_asym 
        --num_calib_data 128 
        --quant_algo awq 
        --dataset pileval_for_awq_benchmark 
        --seq_len 512 
        --model_export quark_safetensors 
        --data_type float16 
        --exclude_layers []
        --custom_mode awq

The quantized model is generated in the <quantized safetensor output dir> folder.

Generating the OGA model
@@@@@@@@@@@@@@@@@@@@@@@@
  
Setup
*****

1. Clone the onnxruntime-genai repo:

.. code-block::

     git clone --branch v0.5.1 https://github.com/microsoft/onnxruntime-genai.git

2. Install the packages

.. code-block::

     conda create --name oga_051 python=3.11
     conda activate oga_051

     pip install numpy
     pip install onnxruntime-genai
     pip install onnx
     pip install transformers
     pip install torch
     pip install sentencepiece

Build the OGA Model
*******************

Run the OGA model builder utility as shown below:

.. code-block::

     cd onnxruntime-genai/src/python/py/models 

     python builder.py \
        -i <quantized safetensor model dir> \
        -o <oga model output dir> \
        -p int4 \
        -e dml

The OGA model is generated in the ``<oga model output dir>`` folder. 

Generating the final model
@@@@@@@@@@@@@@@@@@@@@@@@@@

Setup
*****

1. Create and activate postprocessing environment

.. code-block::

     conda create -n oga_to_hybrid python=3.10
     conda activate oga_to_hybrid

2. Install wheels 

.. code-block::

    cd <hybrid package>\preprocessing
    pip install ryzenai_dynamic_dispatch-1.1.0.dev0-cp310-cp310-win_amd64.whl
    pip install ryzenai_onnx_utils-0.5.0-py3-none-any.whl
    pip install onnxruntime

Generate the final model
************************

The commands below use the ``Phi-3-mini-4k-instruct`` model (denoted as ``Phi-3-mini-4k`` for brevity) as an example to demonstrate the steps for generating the final model.

1. Generate the Raw model: 

.. code-block::

     cd <oga dml model folder>
     mkdir tmp
     onnx_utils --external-data-extension "onnx.data" partition model.onnx ./tmp hybrid_llm.yaml -v --save-as-external --model-name Phi-3-mini-4k_raw 

The command generates:

- ``tmp/Phi-3-mini-4k_raw.onnx``
- ``tmp/Phi-3-mini-4k_raw.onnx.data``

2. Post-process the raw model to generate the JIT model: 

.. code-block::
  
     onnx_utils postprocess .\tmp\Phi-3-mini-4k_raw.onnx .\tmp\Phi-3-mini-4k_jit.onnx hybrid_llm --script-options jit_npu

The command generates

- ``Phi-3-mini-4k_jit.bin``
- ``Phi-3-mini-4k_jit.onnx``
- ``Phi-3-mini-4k_jit.onnx.data``
- ``Phi-3-mini-4k_jit.pb.bin``

3. Move the files related to the JIT model (``.bin`` , ``.onnx`` , ``.onnx.data`` and ``.pb.bin``) to the original model directory and remove ``tmp``

4. Remove original ``model.onnx`` and original ``model.onnx.data``

5. Open ``genai_config.json``  and change the contents of the file as show below:

**Before**

.. code-block::

   "session_options": {
         "log_id": "onnxruntime-genai",
         "provider_options": [
             {
               "dml": {}
             }
          ]
      },
   "filename": "model.onnx",

**Modified**

.. code-block::

     "session_options": {
        "log_id": "onnxruntime-genai",
        "custom_ops_library": "onnx_custom_ops.dll",
        "custom_allocator": "shared_d3d_xrt",
        "external_data_file": "Phi-3-mini-4k_jit.pb.bin",
        "provider_options": [
         ]
      },
      "filename": "Phi-3-mini-4k_jit.onnx",

6. The final model is now ready and can be tested with the ``model_benchmark.exe`` test application.





