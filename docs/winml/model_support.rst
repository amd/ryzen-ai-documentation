#################################
VitisAI EP Model Support
#################################

The VitisAI EP (Execution Provider) within Windows ML supports input models in the following formats.

*******************
Model Support Table
*******************

.. list-table::
   :widths: 25 55
   :header-rows: 1

   * - Model Type
     - Support
   * - **CNN Models**
     - - Original float (FP32) model with automatic BF16 conversion during compilation
       - Quantized QDQ model using A8W8 configuration
   * - **Transformer Models**
     - - Original float (FP32) model with automatic BF16 conversion during compilation
       - Quantized QDQ model using A16W8 configuration
   * - **LLM Models (via Foundry Local)**
     - - Quantized and pre-compiled LLM models
       - Support for custom models through Olive recipe

Note
~~~~

- For CNN and Transformer models, you can use either the original float model (with automatic BF16 conversion) or a quantized QDQ model. Quantization can reduce model size and improve inference performance.
- For LLMs, Foundry Local provides pre-built models that auto-detect the NPU. Custom LLM deployment may require model preparation using the Olive recipe or Ryzen AI OGA workflow. See `Windows ML LLM examples <https://github.com/amd/RyzenAI-SW/tree/main/WinML/LLM>`_ for details.
- For model conversion and quantization options, see :doc:`model_conversion`.
