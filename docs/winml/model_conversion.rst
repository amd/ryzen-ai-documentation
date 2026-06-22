##############################################
Model Conversion and Quantization (AI Toolkit)
##############################################

The **AI Toolkit (AITK)** for Visual Studio Code is the primary tool for model conversion and quantization when preparing models for Windows ML on Ryzen AI.

AITK supports:

- **Model conversion:** Export models from PyTorch, TensorFlow, and other frameworks to ONNX
- **Model quantization:** Convert to QDQ (Quantize-Dequantize) format for lower precision inference
- **Evaluation:** Run models on CPU, GPU, or NPU to validate accuracy and performance

********************
Quantization Options
********************

.. list-table::
   :widths: 25 40
   :header-rows: 1

   * - Option
     - Values
   * - Activation type
     - INT8, UINT8, INT16, UINT16, BF16
   * - Weight type
     - INT8, UINT8, INT16, UINT16, INT4, BF16

Recommended Precision Settings by Model Type:

- CNN Models: Use **A8W8** quantization (activation INT8/UINT8, weight INT8/UINT8)
- Transformer Models: Use **A16W8** quantization (activation INT16/UINT16, weight INT8/UINT8)
- LLM Models: BF16 and INT4 precision options are available

*****************
Device Evaluation
*****************

You can evaluate quantized models on CPU, GPU, or NPU to compare accuracy and performance before deployment.

*****************
Known Limitations
*****************

- **AMD GPU (ROCm) quantization on Windows:** Quantization running on the AMD GPU via ROCm on Windows is not currently supported (AMD Quark Windows GPU support). Use Windows + GPU (CUDA) or Windows + CPU for quantization instead. This does not affect running models on the GPU afterward.
- **LLM model conversion:** Model conversion can be performed on Windows with a CUDA GPU or on Windows with CPU. Conversion on Linux with AMD ROCm is planned for a future release. See the `Windows ML LLM examples <https://github.com/amd/RyzenAI-SW/tree/main/WinML/LLM>`_ for details.

***************
References
***************

- `VS Code AI Toolkit model conversion <https://code.visualstudio.com/docs/intelligentapps/modelconversion>`_
- :doc:`Model quantization <../model_quantization>` (Ryzen AI Quark flow for NPU-only path)
