############
Running LLMs
############

.. note::
   
   Support for LLMs is currently in the Early Access stage. Early Access features are features which are still undergoing some optimization and fine-tuning. These features are not in their final form and may change as we continue to work in order to mature them into full-fledged features.

**************
OGA-based Flow
**************

Starting with version 1.3, the Ryzen AI Software supports deploying quantized LLMs on Ryzen AI PCs using the ONNX Runtime generate() API (OGA).

Two different execution modes are supported:

- Hybrid mode: leverages both the NPU and GPU 

  - Detailed documentation: :doc:`hybrid_oga`
- NPU-only mode: leverages only the NPU.

  - Detailed documentation: :doc:`npu_oga`

The required libraries and the supporting documentation are available upon request on the AMD secure download site: https://account.amd.com/en/member/ryzenai-sw-ea.html 

The OGA-based flow currently supports the following models:

- microsoft/Phi-3-mini-4k-instruct
- microsoft/Phi-3.5-mini-instruct
- mistralai/Mistral-7B-Instruct-v0.3
- Qwen/Qwen1.5-7B-Chat	
- THUDM/chatglm3-6b
- meta-llama/Llama-2-7b-hf
- meta-llama/Llama-2-7b-chat-hf
- meta-llama/Meta-Llama-3-8B
- meta-llama/Llama-3.1-8B
- meta-llama/Llama-3.2-1B-Instruct
- meta-llama/Llama-3.2-3B-Instruct

Pre-optimized models are available on Hugging Face:

- Models for Hybrid execution: https://huggingface.co/collections/amd/quark-awq-g128-int4-asym-fp16-onnx-hybrid-674b307d2ffa21dd68fa41d5
- Models for NPU-only executions: https://huggingface.co/collections/amd/quark-awq-g128-int4-asym-bf16-onnx-npu-13-6759f510b8132db53e044aaf

The OGA-based flow is supported on STX platforms (and onwards)


******************
PyTorch-based Flow
******************

In addition to the OGA flow, a flow based on PyTorch is available here: https://github.com/amd/RyzenAI-SW/blob/main/example/transformers/models/llm/docs/README.md 

This flow provides functional support for a broad set of LLMs. It is intended for prototyping and experimental purposes only. It is not optimized for performance and it should not be used for benchmarking. 

The Pytorch-based flow is supported on PHX, HPT and STX platforms.


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
