####################
Preparing OGA Models
####################

This section describes the process for preparing LLMs for deployment on a Ryzen AI PC using the hybrid or NPU-only execution mode. Currently, the flow supports only fine-tuned versions of the models already supported (as listed in :doc:`hybrid_oga` page). For example, fine-tuned versions of Llama2 or Llama3 can be used. However, different model families with architectures not supported by the hybrid flow cannot be used.

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

3. Download :download:`AMD Quark 0.9 <https://download.amd.com/opendownload/Quark/amd_quark-0.9.zip>` and unzip the archive


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
          --model_dir "meta-llama/Llama-2-7b-chat-hf"  \
          --output_dir <quantized safetensor output dir>  \
          --quant_scheme w_uint4_per_group_asym \
          --num_calib_data 128 \
          --quant_algo awq \
          --dataset pileval_for_awq_benchmark \
          --model_export hf_format \
          --data_type <datatype> \
          --exclude_layers


- For a full-precision pretrained model, to generate NPU-only LLM use ``--datatype float32``
- For a full-precision pretrained model, to generate Hybrid LLM use ``--datatype float16``
- For a BF16 pretrained model, use ``--data_type bfloat16``.

The quantized model is generated in the <quantized safetensor output dir> folder.

**************
Postprocessing
**************

Copy the quantized model to the Windows PC with Ryzen AI installed, activate the Ryzen AI Conda environment, and execute ``model_generate`` command to generate the final model.

Generate the final model for Hybrid execution mode:

.. code-block::

   conda activate ryzen-ai-<version>

   model_generate --hybrid <output_dir> <quantized_model_path>  

 
Generate the final model for NPU execution mode:

.. code-block::

   conda activate ryzen-ai-<version>

   model_generate --npu <output_dir> <quantized_model_path>  


Known Issue: In the current version, Mistral-7B-Instruct-v0.1 has a known issue during OGA model conversion in the postprocessing stage.


New in 1.5.1:
============


In Release 1.5.1, a new option has been added to generate a prefill fused version of the Hybrid Model. Currently, it is tested for `Phi-3.5-mini-instruct`, `Llama-2-7b-chat-hf`, and `Llama-3.1-8B-Instruct`. 

.. code-block::

    conda activate ryzen-ai-<version>

    #For Phi-3.5-mini-instruct/Llama-2-7b-chat-hf
    model_generate --hybrid <output_dir> <quantized_model_path> --optimize prefill --mode bfp16

    #For Llama-3.1-8B-Instruct
    model_generate --hybrid <output_dir> <input_quantized_model_path> --optimize prefill_llama3 --mode bfp16

After the model is generated, locate the ``genai_config.json`` file inside the model folder. Edit it as follows:

1. Set ``"custom_ops_library"`` to ``"C:\\Program Files\\RyzenAI\\<release version>\\deployment\\onnx_custom_ops.dll"``
2. Delete ``"compile_fusion_rt"`` entry from ``"amd_options"``
3. Set ``dd_cache`` to ``<output_dir>\\.cache``, for example ``"dd_cache": "C:\\Users\\user\\<generated model folder>\\.cache"``
4. For ``Phi-3.5-mini-instruct``, ``Llama-2-7b-chat-hf model``


   - Set ``"hybrid_opt_disable_npu_ops": "1"`` inside ``"amd_options"``.
   - Set ``"fusion_opt_io_bind_kv_cache": "1"`` inside ``"amd_options"``.
   - Set ``"flattened_kv": true`` inside ``"search"``.


..
  ------------

  #####################################
  License
  #####################################

  Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
