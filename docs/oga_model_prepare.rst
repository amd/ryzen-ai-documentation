####################
Preparing OGA Models
####################

This section describes the process for preparing LLMs for deployment on a Ryzen AI PC using the hybrid or NPU-only execution mode. Currently, the flow supports only fine-tuned versions of the models already supported (as listed in :doc:`llm_flow` page). For example, fine-tuned versions of Llama2 or Llama3 can be used. However, different model families with architectures not supported by the hybrid flow cannot be used.

Preparing a LLM for deployment on a Ryzen AI PC involves 2 steps:

1. Quantizing the model: The pretrained model is quantized to reduce memory footprint and better map to compute resources in the hardware accelerators
2. Generating the final model: A model specialized for the hybrid or NPU only execution mode is generated from the OGA model.

Quantizing the model
~~~~~~~~~~~~~~~~~~~~

Prerequisites
*************
Linux machine with AMD or Nvidia GPUs

Setup
*****

1. Create and activate Conda Environment 

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

Generate quantized Model
************************

Use following command to run Quantization. In a GPU equipped Linux machine the quantization can take about 30-60 minutes. 

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


- To generate OGA model for NPU only execution mode use `--datatype float32`
- To generate OGA model for Hybrid execution mode use `--datatype float16`

The quantized model is generated in the <quantized safetensor output dir> folder.

Generating the final model
~~~~~~~~~~~~~~~~~~~~~~~~~~

Setup
*****

1. Create and activate Conda environment

.. code-block:: 

    conda create -n oga-model-gen python==3.10
    conda activate oga-model-gen

2. Install necessary wheels

.. code-block::

    pip install model_generate-1.0.0-py3-none-any.whl
    pip install ryzenai_dynamic_dispatch-1.1.0.dev0-cp310-cp310-win_amd64.whl
    pip install ryzenai_onnx_utils-0.5.0-py3-none-any.whl


Generate final model
********************

To generate final model use the command below

.. code-block::

   # Generate NPU model
   model_generate --npu <output_dir> <quantized_model_path>

   # Generate OGA model
   model_generate --hybrid <output_dir> <quantized_model_path>



