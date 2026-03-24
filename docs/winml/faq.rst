##########################
Frequently Asked Questions
##########################

This page addresses common questions about Windows ML, Windows AI APIs, and Foundry Local on Ryzen AI PCs.

.. contents:: Topics
   :local:
   :depth: 1

************************
Windows AI APIs
************************

**Q: Do Windows AI APIs run on AMD NPUs?**

**A:** Most Windows AI APIs have model options that run on CPU or GPU. A few support NPU. Check the `Windows AI APIs documentation <https://learn.microsoft.com/en-us/windows/ai/apis/>`_ for the latest capability matrix per API.

**Q: When should I use Windows AI APIs vs Windows ML?**

**A:** Use **Windows AI APIs** when built-in capabilities cover your scenario:

- OCR (Optical Character Recognition)
- Image description
- Super resolution
- Object erase
- Background blur

Use **Windows ML** when you need to run custom ONNX models that are not covered by the built-in APIs.

***************
Foundry Local
***************

**Q: Which models run with the Foundry Local CLI?**

**A:** Run ``foundry model list`` to see supported models. The list is updated as new models are added.

**Q: Does Foundry Local support Hybrid (NPU + iGPU) or NPU-only?**

**A:** Currently: **NPU-only**. Hybrid execution is on the roadmap.

**Q: Is there an API for Foundry Local?**

**A:** The Foundry Local CLI and service provide an OpenAI-compatible API. See the `Foundry Local documentation <https://learn.microsoft.com/en-us/windows/ai/foundry-local/get-started>`_ and `microsoft/Foundry-Local <https://github.com/microsoft/Foundry-Local>`_ for integration details.

***************
Windows ML
***************

**Q: Can developers control or select EP versions?**

**A:** No. Windows ML manages EP versions automatically; the latest compatible version is downloaded from the Microsoft Store on demand.

**Q: Can developers pass EP provider options?**

**A:** Yes. When using a specific EP (e.g., VitisAI EP), you can pass provider options via the session configuration. See :doc:`model_deployment` for examples. For VitisAI EP options, see :doc:`Model compilation and deployment <../modelrun>`.

**Q: Is there performance overhead when using Windows ML vs native Ryzen AI?**

**A:** Windows ML uses the same VitisAI EP and underlying ONNX Runtime as the native Ryzen AI flow. The main difference is EP management (Windows ML downloads and registers EPs automatically). For performance-critical scenarios, benchmark both paths on your specific hardware and workload.

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
