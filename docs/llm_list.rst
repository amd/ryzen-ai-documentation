.. _supported-llms-table:

###############################
Supported LLMs (Ryzen AI 1.7.1)
###############################

This page is the single source of truth for the pre-optimized LLMs that AMD provides
for deployment with Ryzen AI Software. It supersedes the previous standalone "Model
Table". For instructions on deploying these models, see the
:doc:`OnnxRuntime GenAI (OGA) Flow <hybrid_oga>`. To run a fine-tuned variant of one of
these models, see :doc:`Preparing OGA Models <oga_model_prepare>`.

**********************
How to read this table
**********************

Each model is published in one or more variants. The columns below indicate which
variants are available:

- **Hybrid** — runs on NPU + iGPU together (best interactive latency). Requires a
  Ryzen AI 300 Series (STX/KRK) processor.
- **NPU High-throughput** — NPU-only, optimized for maximum performance; total context
  (input + output) up to 4096 tokens. *(Built with the "Full Fusion" recipe; the
  download collection is named* ``npu-4k`` *and the* ``model_generate`` *flag is*
  ``--full_fusion``\ *.)*
- **NPU Long-context** — NPU-only, supports up to 16K tokens and is ready to run with no
  extra configuration. *(Built with the "Token Fusion" recipe; the download collection is
  named* ``npu-16k`` *and the* ``model_generate`` *flag is* ``--token_fusion``\ *.)*

``Y`` indicates the variant is available; a blank cell indicates it is not published for
this release. For the underlying download links, see the Hugging Face collections linked
from the :ref:`Pre-optimized Models <pre_opt_model>` section.

.. note::

   Model display names follow the Hugging Face repository naming. Pre-optimized model
   repos encode their target, e.g.
   ``amd/Llama-3.2-1B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid`` denotes an
   AWQ-quantized, INT4, ONNX, **hybrid** build of Llama-3.2-1B-Instruct.

******************
Model Availability
******************

.. list-table:: Ryzen AI 1.7.1 LLM availability
   :header-rows: 1
   :widths: 40 15 20 20

   * - Model
     - Hybrid
     - NPU High-throughput (4K)
     - NPU Long-context (16K)
   * - CodeLlama-7b-Instruct-hf
     - Y
     - Y
     - Y
   * - DeepSeek-R1-Distill-Llama-8B
     - Y
     - Y
     - Y
   * - DeepSeek-R1-Distill-Qwen-1.5B
     - Y
     - Y
     - Y
   * - DeepSeek-R1-Distill-Qwen-7B
     - Y
     - Y
     - Y
   * - Llama-3.1-8B
     - Y
     - Y
     - Y
   * - Llama-3.2-1B
     - Y
     - Y
     - Y
   * - Llama-3.2-1B-Instruct
     - Y
     - Y
     - Y
   * - Llama-3.2-3B
     - Y
     - Y
     - Y
   * - Llama-3.2-3B-Instruct
     - Y
     - Y
     - Y
   * - Meta-Llama-3.1-8B-Instruct
     - Y
     - Y
     - Y
   * - Mistral-7B-Instruct-v0.1
     - Y
     - Y
     - Y
   * - Mistral-7B-Instruct-v0.2
     - Y
     - Y
     - Y
   * - Mistral-7B-Instruct-v0.3
     - Y
     - Y
     - Y
   * - Mistral-7B-v0.3
     - Y
     - Y
     - Y
   * - Phi-3-mini-128k-instruct
     - Y
     - Y
     - Y
   * - Phi-3.5-mini-instruct
     - Y
     - Y
     - Y
   * - Phi-4-mini-instruct
     - Y
     - Y
     - Y
   * - Phi-4-mini-reasoning
     - Y
     - Y
     - Y
   * - Qwen-2.5-1.5B-Instruct
     - Y
     - Y
     - Y
   * - Qwen2-1.5B
     - Y
     - Y
     - Y
   * - Qwen2-7B
     - Y
     - Y
     - Y
   * - Qwen2.5-0.5B-Instruct
     - Y
     - Y
     - Y
   * - Qwen2.5-7B-Instruct
     - Y
     - Y
     - Y
   * - Qwen2.5-Coder-0.5B-Instruct
     - Y
     - Y
     - Y
   * - Qwen2.5-Coder-1.5B-Instruct
     - Y
     - Y
     - Y
   * - Qwen2.5-Coder-7B-Instruct
     - Y
     - Y
     - Y
   * - Qwen2.5-3B-Instruct
     - Y
     - Y
     - Y
   * - Llama-2-7b-chat-hf
     - Y
     - Y
     -
   * - Llama-2-7b-hf
     - Y
     - Y
     -
   * - Meta-Llama-3-8B
     - Y
     - Y
     -
   * - Phi-3-mini-4k-instruct
     - Y
     - Y
     -
   * - SmolLM-135M-Instruct
     - Y
     - Y
     -
   * - SmolLM2-135M-Instruct
     - Y
     - Y
     -
   * - gemma-3-4b-it
     -
     - Y
     -
   * - gpt-oss-20b
     -
     - Y
     -
   * - **TOTAL**
     - **33**
     - **35**
     - **27**

.. note::

   The Vision Language Model **gemma-3-4b-it** (multimodal) and the sparse
   **gpt-oss-20b** model are NPU-only. For ``gpt-oss-20b`` it is highly recommended to
   use the ``model_chat.py`` script. See the :doc:`OGA Flow <hybrid_oga>` page for
   details.
