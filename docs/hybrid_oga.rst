##############################################
Ryzen AI OGA Flow for Hybrid Execution of LLMs
##############################################

Introduction
~~~~~~~~~~~~

Starting with version 1.3, the Ryzen AI Software includes support for deploying quantized LLMs on Ryzen AI PCs using the ONNX Runtime generate() API (OGA).

Two different execution modes are supported:

- Hybrid mode: LLM generation flow that leverages both the NPU and GPU.
- NPU-only mode: LLM generation flow that leverage only NPU for compute intensive operations.

This user guide applies to the Hybrid execution mode only. This mode provides best performance in terms of time-to-first-token (TTFT) and tokens-per-second (TPS).

Supported Configurations
~~~~~~~~~~~~~~~~~~~~~~~~

The Ryzen AI OGA flow supports the following processors running Windows 11:

- Strix (STX): AMD Ryzen™ Ryzen AI 9 HX375, Ryzen AI 9 HX370, Ryzen AI 9 365

**NOTE**: Phoenix (PHX) and Hawk (HPT) processors are not supported.

Requirements
~~~~~~~~~~~~
- NPU Drivers (version .237)
- RyzenAI 1.3 MSI installer
- Hybrid LLM artifacts package: hybrid-llm-artifacts_1.3.0.zip  
- Linux machine with an AMD or Nvidia GPU (only required for the quantization process, when working with custom models)

Package Contents
~~~~~~~~~~~~~~~~

Hybrid LLM artifacts package contains the files required to build and run applications using the ONNX Runtime generate() API (OGA) to deploy LLMs using the Hybrid execution mode. The list below describes which files are needed for the different use cases:

- **Python flow**

  - onnx_utils\bin\onnx_custom_ops.dll
  - onnxruntime_genai\wheel\onnxruntime_genai_directml-0.4.0.dev0-cp310-cp310-win_amd64.whl
  - onnxruntime_genai\benchmark\DirectML.dll
- **C++ Runtime**

  - onnx_utils\bin\onnx_custom_ops.dll
  - onnxruntime_genai\benchmark\DirectML.dll
  - onnxruntime_genai\benchmark\D3D13Core.dll
  - onnxruntime_genai\benchmark\onnxruntime.dll
  - onnxruntime_genai\benchmark\ryzenai_onnx_utils.dll
- **C++ Dev headers**

  - onnx_utils
  - onnxruntime_genai
- **Examples**

Pre-optimized Models
~~~~~~~~~~~~~~~~~~~~

AMD provides a set of pre-optimized LLMs ready to be deployed with Ryzen AI Software and the supporting runtime for hybrid execution. These models can be found on Hugging Face in the following collection:

https://huggingface.co/collections/amd/quark-awq-g128-int4-asym-fp16-onnx-hybrid-674b307d2ffa21dd68fa41d5

- https://huggingface.co/amd/Phi-3-mini-4k-instruct-awq-g128-int4-asym-fp16-onnx-hybrid
- https://huggingface.co/amd/Phi-3.5-mini-instruct-awq-g128-int4-asym-fp16-onnx-hybrid
- https://huggingface.co/amd/Mistral-7B-Instruct-v0.3-awq-g128-int4-asym-fp16-onnx-hybrid
- https://huggingface.co/amd/Qwen1.5-7B-Chat-awq-g128-int4-asym-fp16-onnx-hybrid
- https://huggingface.co/amd/chatglm3-6b-awq-w-int4-asym-gs128-a-fp16-onnx-ryzen-strix-hybrid
- https://huggingface.co/amd/Llama-2-7b-hf-awq-g128-int4-asym-fp16-onnx-hybrid
- https://huggingface.co/amd/Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid
- https://huggingface.co/amd/Llama-3-8B-awq-g128-int4-asym-fp16-onnx-hybrid/tree/main
- https://huggingface.co/amd/Llama-3.1-8B-awq-g128-int4-asym-fp16-onnx-hybrid/tree/main
- https://huggingface.co/amd/Llama-3.2-1B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid
- https://huggingface.co/amd/Llama-3.2-3B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid

The steps for deploying the pre-optimized models using Python or C++ are described in the following sections.

Hybrid Execution of OGA Models using Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Setup
@@@@@

1. Install the NPU Drivers (version .237) and Ryzen AI 1.3 according to the instructions in the public documentation: https://ryzenai.docs.amd.com/en/latest/inst.html

2. Download and unzip the hybrid LLM artifacts package 

3. Activate the Ryzen AI 1.3 Conda environment:

.. code-block:: 
    
    conda activate ryzen-ai-1.3.0

4. Install the wheel file included in the hybrid-llm-artifacts package:  

.. code-block::
  
       cd path_to\\hybrid-llm-artifacts\onnxruntime_genai\wheel
       pip install onnxruntime_genai_directml-0.4.0.dev0-cp310-cp310-win_amd64.whl

Run Models
@@@@@@@@@@

1. Clone model from the Hugging Face repository and switch to the model directory

2. Open the genai_config.json file located in the in the folder of the downloaded model. Update the value of the "custom_ops_library"key with the full path to the onnx_custom_ops.dll,located in the hybrid-llm-artifacts\onnx_utils\bin folder:  

.. code-block::
  
      "session_options": {
                ...
                "custom_ops_library": "path_to\\hybrid-llm-artifacts\\onnx_utils\\bin\\onnx_custom_ops.dll",
                ...
      }

3. Copy the directml.dll file to the folder where the onnx_custom_ops.dll is located (note: this step is only required on some systems)

.. code-block::
  
       copy hybrid-llm-artifacts\onnxruntime_genai\lib\DirectML.dll hybrid-llm-artifacts\onnx_utils\bin

4. Run the LLM 

.. code-block::

     cd hybrid-llm-artifacts\scripts\llama3
     python run_model.py --model_dir path_to\Meta-Llama-3-8B-awq-w-int4-asym-gs128-a-fp16-onnx-ryzen-strix-hybrid

Hybrid Execution of OGA Models using C++
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Setup
@@@@@

1. Download and unzip the hybrid LLM artifacts package.

2. Copy everything from ``hybrid-llm-artifacts/onnxruntime-genai/lib`` to ``hybrid-llm-artifacts\examples\c\lib`` 

3. Copy ``hybrid-llm-artifacts/onnx_utils/bin/ryzenai_onnx_utils.dll``  to ``hybrid-llm-artifacts\examples\c\lib`` 

4. Copy everything from ``hybrid-llm-artifacts/onnxruntime-genai/include`` to ``hybrid-llm-artifacts\examples\c\include``

5. Build the model_benchmark.exe application

.. code-block::

     cd hybrid-llm-artifacts\examples\c
     cmake -G "Visual Studio 17 2022" -A x64 -S . -B build
     cd build
     cmake --build . --config Release

**Note**: The ``model_benchmark.exe`` executable is generated in the ``hybrid-llm-artifacts\examples\c\build\Release`` folder

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

 


Appendix: Preparing your own OGA model for hybrid execution (experimental)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The section below describes an LLM model-building recipe for deployment on a Ryzen AI PC using the hybrid flow. Currently, the flow supports only fine-tuned versions of LLMs for models already supported (as listed in "Pre-optimized Models" section of this guide) in the hybrid flow. For example, fine-tuned versions of LLaMA2 or LLaMA3 can be used. However, different model families with architectures not supported by the hybrid flow cannot be used.




Preparing a LLM for deployment on a Ryzen AI PC using the hybrid execution mode involves 3 steps:

1. Quantizing the model: The pretrained model is quantized to reduce memory footprint and better map to compute resources in the hardware accelerators
2. Generating the OGA model: A model suitable for use with the ONNX Runtime generate() API (OGA) is generated from the quantized model.
3. Generating the final model for Hybrid execution: A model specialized for the hybrid execution mode is generated from the OGA model.

Quantizing the model
@@@@@@@@@@@@@@@@@@@@

Prerequisites
*************
Linux machine with Nvidia/AMD GPUs

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

3. Download Quark 0.6.0 and unzip the archive

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
    >pip install ryzenai_dynamic_dispatch-1.1.0.dev0-cp310-cp310-win_amd64.whl
    >pip install ryzenai_onnx_utils-0.5.0-py3-none-any.whl
    >pip install onnxruntime

Generate the final model
************************

**NOTE**: The commands below use the ``Phi-3-mini-4k-instruct`` model (denoted as ``Phi-3-mini-4k`` for brevity) as an example to demonstrate the steps for generating the final model.

1. Generate the Raw model: 

.. code-block::

     cd <oga dml model folder>
     mkdir tmp
     onnx_utils --external-data-extension "onnx.data" partition model.onnx ./tmp hybrid_llm.yaml -v --save-as-external --model-name Phi-3-mini-4k_raw 

The command generates:
- `tmp/Phi-3-mini-4k_raw.onnx`
- `tmp/Phi-3-mini-4k_raw.onnx.data`

2. Post-process the raw model to generate the JIT model: 

.. code-block::
  
     onnx_utils postprocess .\tmp\Phi-3-mini-4k_raw.onnx .\tmp\Phi-3-mini-4k_jit.onnx hybrid_llm --script-options jit_npu

The command generates

- `Phi-3-mini-4k_jit.bin`
- `Phi-3-mini-4k_jit.onnx`
- `Phi-3-mini-4k_jit.onnx.data`
- `Phi-3-mini-4k_jit.pb.bin`

3. Move the files related to the JIT model (``.bin`` , ``.onnx`` , ``.onnx.data`` and ``.pb.bin``) to the original model directory and remove tmp

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





