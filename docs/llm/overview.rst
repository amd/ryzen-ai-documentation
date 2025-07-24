########
Overview
########

************************************
LLM Deployment on Ryzen AI
************************************

Large Language Models (LLMs) can be deployed on Ryzen AI PCs with NPU and GPU acceleration. NPU-only and Hybrid execution modes, which utilize both the NPU and integrated GPU (iGPU), are supported via ONNXRuntime GenAI (OGA). GPU-only acceleration is enabled through llama.cpp. See the :ref:`execution-modes-table` below for detailed information.


Execution Modes
===============

.. _execution-modes-table:
.. list-table:: LLM Execution Mode Comparison
   :header-rows: 1
   :widths: 15 20 25 25

   * - Mode
     - Framework(s)
     - Compute Allocation
     - Primary Use Case
   * - **NPU-Only**
     - OnnxRuntime GenAI (OGA)
     - Neural Processing Unit (NPU) exclusive
     - Maximum NPU utilization while preserving iGPU for parallel workloads
   * - **Hybrid**
     - OnnxRuntime GenAI (OGA)
     - Dynamic NPU + iGPU partitioning
     - Interactive inference with optimal prefill/decode performance
   * - **GPU**
     - llama.cpp
     - Dedicated GPU execution
     - High-throughput inference on discrete/integrated GPU
   * - **CPU**
     - OGA or llama.cpp
     - Traditional CPU-based inference
     - Baseline compatibility across all processor generations

Hardware Requirements
=====================

.. list-table:: Supported Processor Configurations
   :header-rows: 1
   :widths: 25 25 25 25

   * - Processor Series
     - NPU-Only
     - Hybrid
     - GPU/CPU
   * - Ryzen AI 300 (STX/KRK)
     - ✓
     - ✓
     - ✓
   * - Ryzen AI 7000/8000
     - ✗
     - ✗
     - ✓


*******************************
Development Interfaces
*******************************

The Ryzen AI LLM software stack is available through three development interfaces, each suited for specific use cases as outlined in the sections below. All three interfaces are built on top of native OnnxRuntime GenAI (OGA) libraries or llama.cpp libraries, as shown in the :ref:`llm-software-stack-table` diagram below.

The high-level Python APIs, as well as the Server Interface, also leverage the Lemonade SDK, which is multi-vendor open-source software that provides everything necessary for quickly getting started with LLMs on OGA or llama.cpp.

A key benefit of Lemonade is that software developed against their interfaces is portable to many other execution backends.

.. _llm-software-stack-table:

.. flat-table:: Ryzen AI Software Stack
   :header-rows: 1
   :class: center-table

   * - Your Python Application
     - Your LLM Stack
     - Your Native Application
   * - `Lemonade Python API* <#high-level-python-sdk>`_
     - `Lemonade Server Interface* <#server-interface-rest-api>`_
     - `OGA C++ Headers <../hybrid_oga.html>`_ **OR** `llama.cpp C++ Headers <https://github.com/ggml-org/llama.cpp>`_
   * - :cspan:`2` `Custom AMD OnnxRuntime GenAI (OGA) <https://github.com/microsoft/onnxruntime-genai>`_ **OR** `llama.cpp* <https://github.com/ggml-org/llama.cpp>`_
   * - :cspan:`2` `AMD Ryzen AI Driver and Hardware <https://www.amd.com/en/products/processors/consumer/ryzen-ai.html>`_

\* indicates open-source software (OSS).

Server Interface (REST API)
===========================

The Server Interface provides a convenient means to integrate with applications that:

- Already support an LLM server interface, such as the Ollama server or OpenAI API.
- Are written in any language (C++, C#, Javascript, etc.) that supports REST APIs.
- Benefits from process isolation for the LLM backend.

Lemonade Server is available in two ways:

- **Standalone Windows GUI installer**: Quick setup with a desktop shortcut for immediate use. (Recommended for end users, see :doc:`server_interface`)
- **Full Lemonade SDK**: Complete development toolkit with server interface included. (Recommended for developers, see :doc:`high_level_python` for Python SDK)

For example applications that have been tested with Lemonade Server, see the `Lemonade Server Examples <https://github.com/lemonade-sdk/lemonade/tree/main/docs/server/apps>`_.

High-Level Python SDK
=====================

The high-level Python SDK, Lemonade, allows you to get started using PyPI installation in approximately 5 minutes.

This SDK allows you to:

- Experiment with models in hybrid or NPU-only execution mode on Ryzen AI hardware.
- Validate inference speed and task performance.
- Integrate with Python apps using a high-level API.

To get started in Python, follow these instructions: :doc:`high_level_python`.

OGA APIs for C++ Libraries and Python
=====================================

Native C++ libraries for OGA are available to give full customizability for deployment into native applications. The Python bindings for OGA also provide a customizable interface for Python development.

To get started with the OGA APIs, follow these instructions: :doc:`../hybrid_oga`.


.. _featured-llms:

*******************************
Supported LLMs
*******************************

The comprehensive set of pre-optimized models for hybrid execution are available in the `AMD hybrid collection on Hugging Face <https://huggingface.co/collections/amd/ryzenai-15-llm-hybrid-models-6859a64b421b5c27e1e53899>`_ and the NPU-only examples are available in the `AMD NPU collection on Hugging Face <https://huggingface.co/collections/amd/ryzenai-15-llm-npu-models-6859846d7c13f81298990db0>`_. It is also possible to run fine-tuned versions of the models listed (for example, fine-tuned versions of Llama2 or Llama3). For instructions on how to prepare a fine-tuned OGA model, refer to :doc:`../oga_model_prepare`.


********************************
End to End OGA Validation
********************************

A Jupyter Notebook example is provided to demonstrate end-to-end validation of OGA hybrid and NPU-only execution. This notebook includes:

- Installation
- Command Syntax
- Benchmarking
- Subjective Evaluation
- Objective Evaluation

To run the notebook, visit the `Lemonade Tools Tutorial <https://github.com/lemonade-sdk/lemonade/blob/main/examples/notebooks/lemonade_model_validation.ipynb>`_.

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
