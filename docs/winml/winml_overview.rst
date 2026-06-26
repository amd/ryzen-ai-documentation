###################
Windows ML Overview
###################

This section describes how to use **Windows ML on AMD Ryzen AI PCs** and complements the official `Microsoft Windows AI documentation <https://learn.microsoft.com/en-us/windows/ai/overview>`_. It bridges Microsoft's local AI platform with Ryzen AI hardware and software.

Microsoft provides a comprehensive AI platform for Windows spanning three pillars:

- **Windows AI APIs:** Built-in system APIs (OCR, image description, super resolution, object erase, etc.) for Copilot+ PCs. Use when your scenario is covered by these APIs.
- **Foundry Local:** On-device runtime for LLMs and generative AI; auto-detects hardware and downloads compatible models. Use for LLM scenarios with minimal setup.
- **Windows ML:** Runtime for custom ONNX models with automatic execution provider (EP) management across CPU, GPU, and NPU. Use when you need to run your own models.

On **Ryzen AI PCs**, Windows ML can leverage the NPU via the VitisAI EP (Execution Provider).

**********************
When to Use Windows ML
**********************

Choose Windows ML when you:

- Need to run **custom ONNX models** (CNN, Transformer, or LLM) on Windows
- Want **automatic EP management** Windows downloads and registers compatible execution providers (VitisAI EP, MIGraphX EP, DirectML EP) on demand
- Prefer **C#, C++, or Python** with a shared Windows-wide ONNX Runtime (smaller app size)
- Need **hardware flexibility** select CPU, GPU, or NPU via execution policy

Use **Windows AI APIs** when built-in capabilities (OCR, image description, etc.) cover your scenario. Use **Foundry Local** when you want LLMs with minimal model preparation. Use the **Ryzen AI NPU-only flow** (:doc:`../modelrun`) when you need full control over ONNX Runtime without the Windows ML stack.

*******************
Current Limitations
*******************

The Windows ML flow on Ryzen AI is evolving. Keep the following limitations in mind when deciding whether it fits your use case. Details are spread across the pages linked below.

- **No EP version control.** Windows ML always downloads and registers the latest compatible execution provider from the Microsoft Store; you cannot select or pin a specific EP version. If you need to pin a version (for reproducibility or to control exactly what ships with your app), use the native :doc:`Ryzen AI flow <../modelrun>` instead. See :doc:`faq`.
- **Foundry Local is preview and NPU-only.** The zero-setup LLM path (Foundry Local) is in preview and currently supports **NPU-only** execution; Hybrid (NPU + iGPU) is on the roadmap. For Hybrid LLM execution today, use the native :doc:`OGA flow <../hybrid_oga>` or Lemonade. See :doc:`faq`.
- **Custom LLM deployment is manual.** Running a custom (non-Foundry-Local) LLM uses Windows ML together with the OGA APIs and requires manually managing dependencies and model optimization. See :doc:`model_deployment`.
- **AMD GPU (ROCm) quantization on Windows is unsupported.** Quantization running on the AMD GPU via ROCm on Windows is not currently supported; use Windows + GPU (CUDA) or Windows + CPU for quantization instead (Linux + ROCm is planned for a future release). This does not affect running models on the GPU. See :doc:`model_conversion`.
- **Windows App SDK version sensitivity.** The installed Windows App SDK runtime must match the ``wasdk`` Python package version, or EPs fail to load. See :doc:`installation` and :doc:`troubleshooting`.
- **Performance vs. native is not guaranteed.** Windows ML uses the same VitisAI EP and ONNX Runtime as the native flow, but parity is not documented. For performance-critical workloads, benchmark both paths. See :doc:`faq`.

***********
Quick Links
***********

.. list-table::
   :widths: 50 30
   :header-rows: 1

   * - Topic
     - Page
   * - Prerequisites and installation
     - :doc:`installation`
   * - VitisAI EP model support (CNN, Transformer, LLM)
     - :doc:`model_support`
   * - Model deployment
     - :doc:`model_deployment`
   * - Model conversion and quantization (AI Toolkit)
     - :doc:`model_conversion`
   * - Execution providers (registration, EP policy, compilation)
     - :doc:`winml_ep`
   * - Windows ML examples (CNN, Transformer, LLM)
     - :doc:`winml_example`
   * - Frequently asked questions
     - :doc:`faq`
   * - Troubleshooting
     - :doc:`troubleshooting`

******************
External Resources
******************

- `Windows AI Developer Portal <https://developer.microsoft.com/en-us/windows/ai/>`_
- `Windows ML official documentation <https://learn.microsoft.com/en-us/windows/ai/new-windows-ml/overview>`_
- `AI on Windows samples (Microsoft Learn) <https://learn.microsoft.com/en-us/windows/ai/samples/>`_
- `WindowsAppSDK-Samples — WindowsML <https://github.com/microsoft/WindowsAppSDK-Samples/tree/main/Samples/WindowsML>`_
- `RyzenAI-SW Windows ML examples <https://github.com/amd/RyzenAI-SW/tree/main/WinML>`_

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
