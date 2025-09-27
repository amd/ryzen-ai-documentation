####################
Preparing OGA Models
####################

This section describes the process for preparing LLMs for deployment on a Ryzen AI PC using the hybrid or NPU-only execution mode. Currently, the flow supports only fine-tuned versions of the models already supported (as listed in :doc:`hybrid_oga` page). For example, fine-tuned versions of Llama2 or Llama3 can be used. However, different model families with architectures not supported by the hybrid flow cannot be used.

For fine-tuned models that introduce architectural changes requiring new operator shapes not available in the Ryzen AI runtime, refer to the :doc:`oga_op_prepare`

Preparing a LLM for deployment on a Ryzen AI PC involves 2 steps:

1. **Quantization**: The pretrained model is quantized to reduce memory footprint and better map to compute resources in the hardware accelerators
2. **Postprocessing**: During the postprocessing the model is exported to OGA followed by NPU-only or Hybrid execution mode specific postprocess to obtain the final deployable model.

************
Quantization
************

Prerequisites
=============
Linux machine with AMD (e.g., AMD Instinct MI Series) or Nvidia GPUs

Setup
=====

1. Create and activate Conda Environment 

.. code-block::

    conda create --name <conda_env_name> python=3.11
    conda activate <conda_env_name>

2. If Using AMD GPUs, update PyTorch to use ROCm 

.. code-block:: 
  
     pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.1
     python -c "import torch; print(torch.cuda.is_available())" # Must return `True`

3. Download :download:`AMD Quark 0.10 <https://download.amd.com/opendownload/Quark/amd_quark-0.10.zip>` and unzip the archive


4. Install Quark: 

.. code-block::

     cd <extracted amd quark-version>
     pip install amd_quark-<version>+<>.whl

5. Install other dependencies

.. code-block::

   pip install datasets
   pip install transformers
   pip install accelerate
   pip install evaluate


Some models may require a specific version of ``transformers``. For example, ChatGLM3 requires version 4.44.0.   

Generate Quantized Model
========================

Use following command to run Quantization. In a GPU equipped Linux machine the quantization can take about 30-60 minutes. 

.. code-block::

     cd examples/torch/language_modeling/llm_ptq/
     
     python quantize_quark.py \
          --no_trust_remote_code \
          --model_dir "meta-llama/Llama-2-7b-chat-hf"  \
          --output_dir <quantized safetensor output dir>  \
          --quant_scheme w_uint4_per_group_asym \
          --group_size 128 \
          --num_calib_data 128 \
          --seq_len 512 \
          --quant_algo awq \
          --dataset pileval_for_awq_benchmark \
          --model_export hf_format \
          --data_type <datatype> \
          --exclude_layers []

    
- Use ``--data_type bfloat16`` for bf16 pretrained model. For fp32/fp16 pretrained model use ``--datatype float16``

The quantized model is generated in the <quantized safetensor output dir> folder.

**Note:** For the Phi-4 model, the following quantization recipe is recommended for better accuracy:

- Use ``--quant_algo gptq``
- Add ``--group_size_per_layer lm_head 32`` 

**Note:**: Currently the following files are not copied into the quantized model folder and must be copied manually:

- For Phi-4 models: ``configuration_phi3.py``
- For ChatGLM-6b models: ``tokenizer.json``

**************
Postprocessing
**************

Copy the quantized model to the Windows PC with Ryzen AI installed, activate the Ryzen AI Conda environment. 

.. code-block::

    conda activate ryzen-ai-<version>
    pip install onnx_ir
    pip install torch==2.7.1

Generate the final model for Hybrid execution mode:

.. code-block::

   conda activate ryzen-ai-<version>

   model_generate --hybrid <output_dir> <quantized_model_path>  

Generate the final model for NPU execution mode:

.. code-block::

   conda activate ryzen-ai-<version>

   model_generate --npu <output_dir> <quantized_model_path>  --optimize decode


**Note**: During the ``model_generate`` step, the quantized model is first converted to an OGA model using ONNX Runtime GenAI Model Builder (version 0.9.2). It is possible to use a standalone environment for exporting an OGA model, refer to the official `ONNX Runtime GenAI Model Builder documentation <https://github.com/microsoft/onnxruntime-genai/tree/main/src/python/py/models>`_. Once you have an exported OGA model, you can pass it directly to the ``model_generate`` command, which will skip the export step and perform only the post-processing.

Here are simple commands to export OGA model from quantized model using a standalone environment

.. code-block::

    conda create --name oga_builder_env python=3.10
    conda activate oga_buider_env

    pip install onnxruntime-genai==0.7.0
    pip install onnx==1.18.0
    pip install onnxruntime==1.21.1
    pip install torch
    pip install transformers
    pip install numpy==1.26.4

    python3 -m onnxruntime_genai.models.builder -m <input quantized model> -o <output OGA model> -p int4 -e dml 




..
  ------------

  #####################################
  License
  #####################################

  Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
