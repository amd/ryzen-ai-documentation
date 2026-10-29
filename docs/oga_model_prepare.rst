####################
Preparing OGA Models
####################

This section describes the process for preparing LLMs for deployment on a Ryzen AI PC using the hybrid or NPU-only execution mode. Currently, the flow supports only fine-tuned versions of the models already supported (as listed in :doc:`hybrid_oga` page). For example, fine-tuned versions of Llama2 or Llama3 can be used. However, different model families with architectures not supported by the hybrid flow cannot be used.

For fine-tuned models that introduce architectural changes requiring new operator shapes not available in the Ryzen AI runtime, refer to the :doc:`oga_op_prepare`

Preparing a LLM for deployment on a Ryzen AI PC involves 2 steps:

1. **Quantization**: The pretrained model is quantized to reduce memory footprint and better map to compute resources in the hardware accelerators
2. **Postprocessing**: During the postprocessing the model is exported to OGA followed by NPU-only or Hybrid execution mode specific postprocess to obtain the final deployable model.


.. _llm_quantization:

************
Quantization
************

Prerequisites
=============
A Linux machine with AMD (e.g., AMD Instinct MI Series) or Nvidia GPUs

Setup
=====

1. Create and activate a Python virtual environment 

.. code-block::

    python3.12 -m venv <env_name>
    source <env_name>/bin/activate

2. If Using AMD GPUs, update PyTorch to use ROCm 

.. code-block:: 
  
     pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.1
     python -c "import torch; print(torch.cuda.is_available())" # Must return `True`

3. Download :download:`AMD Quark 0.11 <https://download.amd.com/opendownload/Quark/amd_quark-0.11.zip>` and unzip the archive


4. Install Quark: 

.. code-block::

     cd <extracted amd quark-version>
     pip install amd_quark-<version>+<>.whl

5. Install other dependencies

.. code-block::

   pip install datasets
   pip install transformers==4.57.6
   pip install accelerate
   pip install evaluate
   pip install nltk


Generate Quantized Model
========================

Use following command to run Quantization. In a GPU equipped Linux machine the quantization can take about 30-60 minutes.

.. code-block::

     cd examples/torch/language_modeling/llm_ptq/

     python quantize_quark.py \
          --no_trust_remote_code \
          --model_dir "meta-llama/Llama-2-7b-chat-hf"  \
          --output_dir <quantized safetensor output dir>  \
          --quant_scheme uint4_wo_128 \
          --num_calib_data 128 \
          --seq_len 512 \
          --quant_algo awq \
          --dataset pileval_for_awq_benchmark \
          --model_export hf_format \
          --data_type <datatype> \
          --exclude_layers []


- Use ``--data_type bfloat16`` for bf16 pretrained model. For fp32/fp16 pretrained model use ``--datatype float16``
- Quark natively supports AWQ quantization for popular architectures. If AWQ is not supported by default, you must create an AWQ configuration file and pass it to the ``quantize_quark.py`` script using the ``--quant_algo_config_file awq <custom awq config json>`` option. For details on creating an AWQ config file, see the Quark documentation AWQ example: https://quark.docs.amd.com/latest/tutorials/torch/example_awq.html
- Not using ``--exclude_layers``  parameter may result in model-specific defaults which may exclude certain layers like output layers.
- To specify a group size other than 128, such as 32, use ``--quant_scheme uint4_wo_32`` instead of ``--quant_scheme uint4_wo_128``. Available group sizes are 32, 64, and 128 (e.g., uint4_wo_32, uint4_wo_64, uint4_wo_128)
- Quark supports quantizing layers with different group sizes, use ``--layer_quant_scheme lm_head uint4_wo_32`` to quantize the model with 32 group size for lm_head

The quantized model is generated in the <quantized safetensor output dir> folder.

**Note:** For the Phi-4 model, the following quantization recipe is recommended for better accuracy:

- Use ``--quant_algo gptq``
- Add ``--layer_quant_scheme lm_head uint4_wo_32``

**Note:**: Currently the following files are not copied into the quantized model folder and must be copied manually:

- For Phi-4 models: ``configuration_phi3.py``
- For ChatGLM-6b models: ``tokenizer.json``

Importing INT4 Quantized Models from QAT
========================================

In addition to the existing Post-Training Quantization (PTQ) workflow using
AMD Quark, Ryzen AI supports importing pre-quantized INT4 PyTorch models
generated through Quantization-Aware Training (QAT), provided the checkpoint
follows a supported format.

The ONNX Runtime GenAI Model Builder supports the ``quant_auto`` checkpoint
format, allowing quantized weights to be converted into the ONNX INT4
representation while preserving the original quantization scales and zero
points. ``quant_auto`` is an **asymmetric** INT4 format: the trained zero
points carry real information and are retained through export rather than
being replaced by a symmetric scheme.

Supported checkpoint format
---------------------------

For the authoritative tensor layout, see the ONNX Runtime GenAI
`quant_auto format specification
<https://github.com/microsoft/onnxruntime-genai/blob/main/src/python/py/models/loaders/quant-auto.md>`_.

Configuration and naming conventions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The checkpoint must set ``quant_method: quant_auto`` in
``quantize_config.json``.

A few conventions are specific to this format and are load-breaking if not
followed:

- **bits and group_size are not declared in the config.** The loader defaults
  ``bits`` to 4 and infers ``group_size`` from the tensor shapes
  (``in_features / num_groups``, where ``num_groups`` is derived from the
  scales shape). Do not rely on these fields being present.
- **Zero-point tensors use the .zeros suffix** (for example
  ``model.embed_tokens.zeros``), not ``.qzeros``. The loader normalizes
  ``.zeros`` to ``.qzeros`` on read.
- **Fused projections** (``qkv_proj``, ``gate_up_proj``) are stored in
  ``(out, in)`` order and split along dim=0 using group-size-aware boundaries.

Compilation flow
----------------

Once exported to ONNX, the model can follow the existing Ryzen AI NPU or
hybrid compilation flow, subject to model architecture and execution-mode
support.

**Note:** This capability applies to checkpoints compatible with the documented ``quant_auto`` format. Other QAT checkpoint formats may require conversion or additional loader support.

**************
Postprocessing
**************

Copy the quantized model to the Windows PC with Ryzen AI installed, and activate the Ryzen AI Python virtual environment.

.. code-block::

    "C:\Program Files\RyzenAI\ryzen-ai-1.9.0\Scripts\activate.bat"

Hybrid Execution Mode
=====================

Generate the final model for Hybrid execution mode (NPU prefill phase + GPU token phase):

.. code-block::

   model_generate --hybrid --input <quantized_model_path> --output <output_dir>

NPU Execution Mode
===================

Several NPU optimization levels are available depending on model support and performance requirements. To check which variants (full fusion, token fusion, hybrid) are supported for a given model architecture, see :doc:`llm_list`.

**Full Fusion** (**Best performance**, recommended for `supported models <https://huggingface.co/collections/amd/ryzen-ai-180-npu-4k>`_):

.. code-block::

   model_generate --npu --full_fusion --input <quantized_model_path> --output <output_dir>

**Token Fusion** (**long-context** supportted):

.. code-block::

   :: 16K context
   model_generate --npu --token_fusion --input <quantized_model_path> --output <output_dir> --extra_options max_seq_len=16384

**Basic** (safe default for new or untested models):

.. code-block::

   model_generate --npu --basic --input <quantized_model_path> --output <output_dir>

**Eager**:

.. code-block::

   model_generate --npu --eager --input <quantized_model_path> --output <output_dir>

OGA Export Only
===============

To export the quantized model to OGA format without performing any NPU or Hybrid postprocessing:

.. code-block::

   model_generate --oga_only --input <quantized_model_path> --output <output_dir>

Memory Optimization
===================

Add ``--mem_optimize`` to any recipe to optimize for 16 GB laptop configurations:

.. code-block::

   model_generate --hybrid --mem_optimize --input <quantized_model_path> --output <output_dir>

.. code-block::

   model_generate --npu --token_fusion --mem_optimize --input <quantized_model_path> --output <output_dir>

**Note**: During the ``model_generate`` step, the quantized model is first converted to an OGA model using ONNX Runtime GenAI Model Builder (version 0.14.0). It is possible to use a standalone environment for exporting an OGA model, refer to the official `ONNX Runtime GenAI Model Builder documentation <https://github.com/microsoft/onnxruntime-genai/tree/main/src/python/py/models>`_. Once you have an exported OGA model, you can pass it directly to the ``model_generate`` command with ``--input``, which will skip the export step and perform only the post-processing.

Here are simple commands to export an OGA model from a quantized model using a standalone environment:

.. code-block::

    py -3.12 -m venv oga_builder_env
    oga_builder_env\Scripts\activate.bat


    pip install onnxruntime-genai==0.14.0
    # pip install other necessary packages
    pip install ....


    python3 -m onnxruntime_genai.models.builder -m <input quantized model> -o <output OGA model> -p int4 -e dml 




..
  ------------

  #####################################
  License
  #####################################

  Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
