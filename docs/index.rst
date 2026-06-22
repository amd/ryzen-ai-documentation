##########################
Ryzen AI Software
##########################

AMD Ryzen™ AI Software includes the tools and runtime libraries for optimizing and deploying AI inference on AMD Ryzen™ AI powered PCs. Ryzen AI software enables applications to run on the neural processing unit (NPU) built in the AMD XDNA™ architecture, as well as on the integrated GPU. This allows developers to build and deploy models trained in PyTorch or TensorFlow and run them directly on laptops powered by Ryzen AI using ONNX Runtime and the Vitis™ AI Execution Provider (EP).

.. image:: images/rai-sw.png
   :align: center

***********
Quick Start
***********

- :ref:`Supported Configurations <supported-configurations>`
- :doc:`inst`
- :doc:`examples`

.. _choose-your-flow:

*****************
Choose Your Flow
*****************

Ryzen AI Software offers several deployment paths ("flows"). Use the guide below to find
the one that matches what you are building, then jump to its documentation.

.. list-table:: Which flow should I use?
   :header-rows: 1
   :widths: 28 24 28 20

   * - I want to run...
     - on...
     - using...
     - Start here
   * - A **CNN / Transformer / vision** model (ResNet, BERT, YOLO, etc.)
     - NPU
     - ONNX Runtime + VitisAI EP (with AMD Quark for quantization)
     - :doc:`Model Quantization <model_quantization>` then :doc:`Compilation & Deployment <modelrun>`
   * - An **LLM**, fastest path, minimal setup
     - NPU + iGPU (Hybrid) or NPU-only
     - Lemonade (Server or Python SDK)
     - :doc:`LLM Deployment Overview <llm/overview>`
   * - An **LLM**, full native control
     - NPU + iGPU (Hybrid) or NPU-only
     - OnnxRuntime GenAI (OGA) C++ / Python API
     - :doc:`OGA Flow <hybrid_oga>`
   * - Any **custom ONNX model** through Microsoft's Windows-wide runtime
     - CPU / GPU / NPU (auto-selected)
     - Windows ML (VitisAI EP managed automatically) or Foundry Local for LLMs
     - :doc:`Windows ML Overview <winml/winml_overview>`
   * - A model on the **integrated GPU**
     - iGPU
     - DirectML (ONNX Runtime DmlExecutionProvider)
     - :doc:`DirectML Flow <gpu/ryzenai_gpu>`

.. note::

   **Native Ryzen AI flow vs. Windows ML.** Both run NPU models through the *same*
   VitisAI EP and ONNX Runtime. The difference is execution-provider management: the
   native flow ships and configures the EP yourself (maximum control), while Windows ML
   downloads and registers the EP automatically from the Microsoft Store (least setup).
   Choose the native flow when you need full control over ORT; choose Windows ML when you
   want the system to manage EPs for you.

.. _hardware-support-matrix:

***********************
Will My Processor Work?
***********************

NPU acceleration requires a supported AMD processor. Hybrid and NPU-only LLM execution
require a **Ryzen AI 300 Series** part. Check your processor before choosing a flow.

.. list-table:: Flow support by processor
   :header-rows: 1
   :widths: 34 22 22 22

   * - Processor Series (codename)
     - CNN/Transformer on NPU
     - LLM Hybrid / NPU-only
     - GPU / CPU
   * - Ryzen AI 300 Series — Strix, Strix Halo, Krackan Point (STX/KRK)
     - ✓
     - ✓
     - ✓
   * - Ryzen 7040 / 8040 Series — Phoenix, Hawk Point (PHX/HPT)
     - ✓ (INT8 only)
     - ✗
     - ✓
   * - Ryzen 7000 / 8000 (no NPU)
     - ✗
     - ✗
     - ✓

For the authoritative device list and the model-compatibility matrix, see the
:ref:`Supported Configurations <supported-configurations>` section of the Release Notes.

.. _glossary:

********
Glossary
********

A few terms recur throughout this documentation and are easy to confuse:

- **Flow** — a top-level deployment path (e.g., the CNN/Transformer NPU flow, the LLM/OGA
  flow, the DirectML flow, the Windows ML flow).
- **Execution mode** — *how* an LLM is split across hardware: **Hybrid** (NPU + iGPU),
  **NPU-only**, **GPU** (via llama.cpp), or **CPU**.
- **Ryzen AI Software** — this overall AMD product (tools + runtime).
- **Lemonade / Lemonade SDK** — multi-vendor open-source software that layers on top of
  OGA (or llama.cpp) for quick LLM setup. The "High-Level Python SDK" *is* Lemonade.
- **OGA** — OnnxRuntime GenAI, the lowest-level LLM API on Ryzen AI.
- **VitisAI EP** — the Vitis AI Execution Provider for ONNX Runtime; the component that
  targets the NPU. (Also seen as "VAI EP" and the code identifier
  ``VitisAIExecutionProvider``.)
- **NPU vs. IPU** — the same hardware. Prose uses "NPU"; some tool output and provider
  options still say "IPU." They are interchangeable.
- **Codenames** — STX = Strix / Strix Halo, KRK = Krackan Point, PHX = Phoenix,
  HPT = Hawk Point.

.. _choosing-overlapping-flows:

**********************************
Choosing Between Overlapping Flows
**********************************

Several flows can run the *same* model on the *same* hardware. This overlap is by design —
it lets you trade control for convenience. Use the guidance below when more than one flow
could do the job.

A useful mental model is two phases:

- **Phase 1 — Model preparation** (offline): converting and optionally quantizing a model
  to ONNX, using AMD Quark, the VS Code AI Toolkit, or Olive. The output is an ONNX file.
- **Phase 2 — Runtime**: loading the model, selecting the execution provider/device,
  compiling for the target, and running inference.

The flows differ mainly in how much of these two phases *you* own versus how much is done
for you.

Running an LLM: control vs. convenience
========================================

For LLMs there is a spectrum from full control to zero setup. **All of these run on the
same Ryzen AI NPU** — they differ in who prepares the model and who manages execution.

.. list-table::
   :header-rows: 1
   :widths: 26 22 22 30

   * - Option
     - Model prep
     - Execution control
     - Pick this when…
   * - **OGA API** (:doc:`OGA Flow <hybrid_oga>`)
     - Pre-optimized or self-prepared OGA models
     - Full — native C++/Python
     - Building a native app needing the lowest-level access.
   * - **Lemonade** (:doc:`Server <llm/server_interface>` / :doc:`Python SDK <llm/high_level_python>`)
     - None — pre-optimized models
     - High-level API or OpenAI-compatible server
     - Fastest AMD-native path; supports **Hybrid and NPU-only**.
   * - **Foundry Local** (:doc:`via Windows ML <winml/model_deployment>`)
     - None — Microsoft ships the models
     - Automatic — auto-detects the NPU
     - Minimum setup on Windows; OpenAI-compatible API.
   * - **Custom LLM via Windows ML** (:doc:`Windows ML <winml/model_deployment>`)
     - You bring a custom ONNX/OGA LLM
     - Windows manages the EP
     - Custom/fine-tuned model, but let Windows manage EPs.

.. note::

   **Lemonade vs. Foundry Local** — these are the two "easy button" LLM options and are the
   closest competitors. Lemonade is AMD's open-source layer over OGA/llama.cpp and supports
   both **Hybrid and NPU-only** execution today. Foundry Local is Microsoft's runtime and is
   currently **NPU-only and in preview** (Hybrid is on the roadmap). If you need Hybrid
   (NPU + iGPU) execution, choose Lemonade or the OGA flow, not Foundry Local.

Running a CNN / Transformer / vision model: native flow vs. Windows ML
======================================================================

For non-LLM models there are two NPU paths, and **both use the same VitisAI EP under the
hood** — they share Phase 1 (you prepare the ONNX model) and differ only in Phase 2:

- **Native Ryzen AI flow** (:doc:`Compilation & Deployment <modelrun>`) — you ship and
  configure the VitisAI EP yourself. Choose this for maximum control over ONNX Runtime,
  packaging, and provider options, or for non-Windows-ML deployment.
- **Windows ML** (:doc:`Windows ML <winml/winml_overview>`) — Windows downloads and
  registers the EP automatically from the Microsoft Store, and you steer it with an
  execution policy (e.g. ``PREFER_NPU``). Choose this for the smallest app footprint
  (shared, Windows-wide ONNX Runtime) and automatic EP management.
- **DirectML flow** (:doc:`DirectML Flow <gpu/ryzenai_gpu>`) — runs on the **iGPU** rather
  than the NPU. Choose this when you specifically want GPU execution.

Because the native flow and Windows ML use the same EP, you can prepare a model once and
deploy it either way; the choice is purely about how much of execution you want to manage.

*************************
Development Flow Overview
*************************

The Ryzen AI development flow does not require any modifications to the existing model training processes and methods. The pre-trained model can be used as the starting point of the Ryzen AI flow.

Quantization
============

Quantization involves converting the AI model’s parameters from floating-point to lower-precision representations, such as 8-bit integer. Quantized models are more power-efficient, utilize less memory, and offer better performance. Ryzen AI Software also supports CNN and Transformer models in floating-point 32 format as input models without quantization. These models are internally converted to bfloat16 and compiled using the bfloat16 compilation flow.


**AMD Quark** is a comprehensive cross-platform deep learning toolkit designed to simplify and enhance the quantization of deep learning models. Supporting both PyTorch and ONNX models, Quark empowers developers to optimize their models for deployment on a wide range of hardware backends, achieving significant performance gains without compromising accuracy.

For more details, refer to the :doc:`model_quantization` page.

CNN/Transformer Compilation and Deployment
==========================================
The AI model is deployed using the ONNX Runtime with either C++ or Python APIs. The Vitis AI Execution Provider included in the ONNX Runtime intelligently determines what portions of the AI model should run on the NPU, optimizing workloads to ensure optimal performance with lower power consumption.

For more details, refer to the :doc:`modelrun` page.

*****************
LLM Flow Overview
*****************

The Ryzen AI LLM software stack is available through three development interfaces, each suited for specific use cases as outlined in the sections below. All three interfaces are built on top of native OnnxRuntime GenAI (OGA) libraries or llama.cpp libraries, as shown in the :ref:`llm-software-stack-table` diagram below.

The **high-level Python APIs**, as well as the **Server Interface**, also leverage the **Lemonade SDK**, which is multi-vendor open-source software that provides everything necessary for quickly getting started with LLMs on OGA or llama.cpp.

At the bottom, **OnnxRuntime GenAI (OGA)** or llama.cpp (only supported for iGPU)  API is the lowest-level API available for building LLM applications on a Ryzen AI PC.

.. _llm-software-stack-table:

.. flat-table:: Ryzen AI Software Stack
   :header-rows: 1
   :class: center-table

   * - Your Python Application
     - Your LLM Stack
     - Your Native Application
   * - `Lemonade Python API* <#high-level-python-sdk>`_
     - `Lemonade Server Interface* <#server-interface-rest-api>`_
     - `OGA C++ Headers <hybrid_oga.html>`_ **OR** `llama.cpp C++ Headers <https://github.com/ggml-org/llama.cpp>`_
   * - :cspan:`2` `Custom AMD OnnxRuntime GenAI (OGA) <https://github.com/microsoft/onnxruntime-genai>`_ **OR** `llama.cpp* <https://github.com/ggml-org/llama.cpp>`_
   * - :cspan:`2` `AMD Ryzen AI Driver and Hardware <https://www.amd.com/en/products/processors/consumer/ryzen-ai.html>`_

For more details, refer to the :doc:`llm/overview` page. For the list of pre-optimized
models, see :doc:`Supported LLMs <llm_list>`.


|
|


.. toctree::
   :maxdepth: 1
   :hidden:

   relnotes.rst


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Getting Started on the NPU

   inst.rst
   examples.rst
   linux.rst

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Running Models on the NPU

   model_quantization.rst
   modelrun.rst
   app_development.rst
   whisper_cpp.rst

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Running LLMs on the NPU

   llm/overview.rst
   llm/server_interface.rst
   llm/high_level_python.rst
   hybrid_oga.rst
   oga_model_prepare.rst
   Supported LLMs <llm_list.rst>

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Running Models on the GPU

   gpu/ryzenai_gpu.rst

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Windows ML on AMD Ryzen AI

   winml/winml_overview.rst
   winml/installation.rst
   winml/model_support.rst
   winml/model_deployment.rst
   winml/model_conversion.rst
   winml/winml_ep.rst
   winml/winml_example.rst
   winml/faq.rst
   winml/troubleshooting.rst

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Additional Topics

   NPU Management <xrt_smi.rst>
   ai_analyzer.rst
   sd_demo.rst
   ryzen_ai_libraries.rst
   Supported Operators <ops_support.rst>
   Licensing Information <licenses.rst>
