########
Overview
########

************************************
OGA-based Flow with Hybrid Execution
************************************

Ryzen AI Software is the best way to deploy quantized 4-bit LLMs on Ryzen AI 300-series PCs. This solution uses a hybrid execution mode, which leverages both the NPU and integrated GPU (iGPU), and is built on the OnnxRuntime GenAI (OGA) framework. 

Hybrid execution mode optimally partitions the model such that different operations are scheduled on NPU vs. iGPU. This minimizes time-to-first-token (TTFT) in the prefill-phase and maximizes token generation (tokens per second, TPS) in the decode phase.

OGA is a multi-vendor generative AI framework from Microsoft that provides a convenient LLM interface for execution backends such as Ryzen AI. 

Supported Configurations
========================

- Only Ryzen AI 300-series Strix Point (STX) and Krackan Point (KRK) processors support OGA-based hybrid execution.
- Developers with Ryzen AI 7000- and 8000-series processors can get started using the CPU-based examples linked in the :ref:`supported-llms` table.
- Windows 11 is the required operating system.


*******************************
Development Interfaces
*******************************

.. note:: Only the OGA APIs interface provides support for DeepSeek-R1-Distill models at this time.

The Ryzen AI LLM software stack is available through three development interfaces, each suited for specific use cases as outlined in the sections below. All three interfaces are built on top of native OnnxRuntime GenAI (OGA) libraries, as shown in the :ref:`software-stack-table` diagram below. 

The high-level Python APIs, as well as the Server Interface, also leverage the ``lemonade`` SDK, which is multi-vendor open-source software that provides everything necessary for quickly getting started with LLMs on OGA.

A key benefit of both OGA and ``lemonade`` is that software developed against their interfaces is portable to many other execution backends.

.. _software-stack-table:

.. flat-table:: Ryzen AI Software Stack
   :header-rows: 1
   :class: center-table

   * - Your Python Application
     - Your LLM Stack
     - Your Native Application
   * - `Lemonade Python API* <#high-level-python-sdk>`_
     - `Lemonade Server Interface* <#server-interface-rest-api>`_
     - `OGA C++ Headers <../hybrid_oga.html>`_
   * - :cspan:`2` `AMD VitisAI build of OnnxRuntime GenAI (OGA) <https://github.com/microsoft/onnxruntime-genai>`_
   * - :cspan:`2` `AMD Ryzen AI Driver and Hardware <https://www.amd.com/en/products/processors/consumer/ryzen-ai.html>`_

\* indicates open-source software (OSS).

High-Level Python SDK
=====================

The high-level Python SDK, ``lemonade``, can get you started in under 5 minutes with PyPI installation.

This SDK is the fastest way to:

- Experiment with models in hybrid execution mode on Ryzen AI hardware.
- Validate inference speed and task performance.
- Integrate with Python apps using a high-level API.

To get started in Python, follow these instructions: :doc:`high_level_python`.


Server Interface (REST API)
===========================

The Server Interface provides a convenient means to integrate with applications that:

- Already support an LLM server interface, such as the ollama server or OpenAI API.
- Are written in any language (C++, C#, Javascript, etc.) that supports REST APIs.
- Benefits from process isolation for the LLM backend.

To get started with the server interface, follow these instructions: :doc:`server_interface`.


OGA APIs for C++ Libraries and Python
=====================================

Native C++ libraries for OGA are available to give full customizability for deployment into native applications.

The Python bindings for OGA also provide a customizable interface for Python development.

To get started with the OGA APIs, follow these instructions :doc:`../hybrid_oga`.


.. _supported-llms:

*******************************
Supported LLMs
*******************************

The following tables contain a comprehensive list of all LLMs that have been validated on Ryzen AI hybrid execution mode. The hybrid examples are built on top of OnnxRuntime GenAI (OGA).

The pre-optimized models for hybrid execution used in these examples are available in the `AMD hybrid collection on Hugging Face <https://huggingface.co/collections/amd/quark-awq-g128-int4-asym-fp16-onnx-hybrid-674b307d2ffa21dd68fa41d5>`_. It is also possible to run fine-tuned versions of the models listed (for example, fine-tuned versions of Llama2 or Llama3). For instructions on how to prepare a fine-tuned OGA model for hybrid execution, refer to :ref:`Preparing Models <hybrid-prepare-models>`.

.. flat-table:: OGA API DeepSeek Supported LLMs
  :header-rows: 2
  :class: deepseek-table
  
  * -
    - :cspan:`3` Ryzen AI Hybrid (OGA int4, ISL = 1024)
  * - Model
    - Instructions
    - TTFT [s]
    - TPS [tok/s]
    - Validation
  * - `DeepSeek-R1-Distill-Qwen-1.5B <https://huggingface.co/amd/DeepSeek-R1-Distill-Qwen-1.5B-awq-asym-uint4-g128-lmhead-onnx-hybrid>`_
    - :rspan:`2` :doc:`../hybrid_oga`
    - 0.68
    - 60.0
    - 🟢
  * - `DeepSeek-R1-Distill-Qwen-7B <https://huggingface.co/amd/DeepSeek-R1-Distill-Qwen-7B-awq-asym-uint4-g128-lmhead-onnx-hybrid>`_
    - 2.64
    - 20.1
    - 🟢
  * - `DeepSeek-R1-Distill-Llama-8B <https://huggingface.co/amd/DeepSeek-R1-Distill-Llama-8B-awq-asym-uint4-g128-lmhead-onnx-hybrid>`_
    - 2.68
    - 19.2
    - 🟢



.. flat-table:: Lemonade SDK Supported LLMs
   :header-rows: 2
   :class: llm-table

   * - 
     - :cspan:`1` CPU Baseline (HF bfloat16)
     - :cspan:`3` Ryzen AI Hybrid (OGA int4)
   * - Model
     - Example
     - Validation
     - Example
     - TTFT Speedup
     - Tokens/S Speedup
     - Validation
     
   * - `Llama-3.2-1B-Instruct <https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct>`_
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/cpu/Llama_3_2_1B_Instruct.md>`__
     - 🟢
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/hybrid/Llama_3_2_1B_Instruct.md>`__
     - 1.8x
     - 5.6x
     - 🟢
   * - `Llama-3.2-3B-Instruct <https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct>`_
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/cpu/Llama_3_2_3B_Instruct.md>`__
     - 🟢
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/hybrid/Llama_3_2_3B_Instruct.md>`__
     - 2.7x
     - 8.9x
     - 🟢
   * - `Phi-3-mini-4k-instruct <https://huggingface.co/microsoft/Phi-3-mini-4k-instruct>`_
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/cpu/Phi_3_mini_4k_instruct.md>`__
     - 🟢
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/hybrid/Phi_3_mini_4k_instruct.md>`__
     - 2.8x
     - 9.1x
     - 🟢
   * - `Phi-3.5-mini-instruct <https://huggingface.co/microsoft/Phi-3.5-mini-instruct>`_
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/cpu/Phi_3_5_mini_instruct.md>`__
     - 🟢
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/hybrid/Phi_3_5_mini_instruct.md>`__
     - 2.6x
     - 7.8x
     - 🟢
   * - `Mistral-7B-Instruct-v0.3 <https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3>`_
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/cpu/Mistral_7B_Instruct_v0_3.md>`__
     - 🟢
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/hybrid/Mistral_7B_Instruct_v0_3.md>`__
     - 4.8x
     - 9.7x
     - 🟢
   * - `Qwen1.5-7B-Chat <https://huggingface.co/Qwen/Qwen1.5-7B-Chat>`_
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/cpu/Qwen1_5_7B_Chat.md>`__
     - 🟢
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/hybrid/Qwen1_5_7B_Chat.md>`__
     - 3.5x
     - 8.6x
     - 🟢
   * - `Llama-2-7b-hf <https://huggingface.co/meta-llama/Llama-2-7b-hf>`_
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/cpu/Llama_2_7b_hf.md>`__
     - 🟢
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/hybrid/Llama_2_7b_hf.md>`__
     - 4.6x
     - 8.3x
     - 🟢
   * - `Llama-2-7b-chat-hf <https://huggingface.co/meta-llama/Llama-2-7b-chat-hf>`_
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/cpu/Llama_2_7b_chat_hf.md>`__
     - 🟢
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/hybrid/Llama_2_7b_chat_hf.md>`__
     - 4.7x
     - 9.0x
     - 🟢
   * - `Meta-Llama-3-8B <https://huggingface.co/meta-llama/Meta-Llama-3-8B>`_
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/cpu/Meta_Llama_3_8B.md>`__
     - 🟢
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/hybrid/Meta_Llama_3_8B.md>`__
     - 4.9x
     - 8.7x
     - 🟢
   * - `Llama-3.1-8B <https://huggingface.co/meta-llama/Llama-3.1-8B>`_
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/cpu/Llama_3_1_8B.md>`__
     - 🟢
     - `Link <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/hybrid/Llama_3_1_8B.md>`__
     - 4.1x
     - 9.1x
     - 🟢


The lemonade SDK table was compiled using validation, benchmarking, and accuracy metrics as measured by the `ONNX TurnkeyML v6.0.0 <https://pypi.org/project/turnkeyml/6.0.0/>`_ ``lemonade`` commands in each example link.

Data collection details:

* All validation, performance, and accuracy metrics are collected on the same system configuration:
  
  * System: HP OmniBook Ultra Laptop 14z
  * Processor: AMD Ryzen AI 9 HX 375 W/ Radeon 890M
  * Memory: 32GB of RAM

* The Hugging Face ``transformers`` framework is used as the baseline implementation for speedup and accuracy comparisons. 

  * The baseline checkpoint is the original ``safetensors`` Hugging Face checkpoint linked in each table row, in the ``bfloat16`` data type.
  
* All speedup numbers are the measured performance of the model with input sequence length (ISL) of ``1024`` and output sequence length (OSL) of ``64``, on the specified backend, divided by the measured performance of the baseline.
* We assign the 🟢 validation score based on this criteria: all commands in the example guide ran successfully.


******************
Alternate Flows
******************

.. note::
   
   The alternate flows for LLMs described below are currently in the Early Access stage. Early Access features are features which are still undergoing some optimization and fine-tuning. These features are not in their final form and may change as we continue to work in order to mature them into full-fledged features.


OGA-based Flow with NPU-only Execution
======================================

The primary OGA-based flow for LLMs employs an hybrid execution mode which leverages both the NPU and iGPU. AMD also provides support for an OGA-based flow where the iGPU is not sollicited and where the compute-intensive operations are exclusively offloaded to the NPU.

The OGA-based NPU-only execution mode is supported on STX and KRK platforms.

To get started with the OGA-based NPU-only execution mode, follow these instructions :doc:`../npu_oga`.


PyTorch-based Flow
==================

An experimental flow based on PyTorch is available here: https://github.com/amd/RyzenAI-SW/blob/main/example/transformers/models/llm/docs/README.md 

This flow provides functional support for a broad set of LLMs. It is intended for prototyping and experimental purposes only. It is not optimized for performance and it should not be used for benchmarking. 

The Pytorch-based flow is supported on PHX, HPT and STX platforms.


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
