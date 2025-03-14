##################
Model Quantization
##################

**Model quantization** is the process of mapping high-precision weights/activations to a lower precision format, such as BF16/INT8, while maintaining model accuracy. This technique enhances the computational and memory efficiency of the model for deployment on NPU devices. It can be applied post-training, allowing existing models to be optimized without the need for retraining.

The Ryzen AI compiler supports input models quantized to either INT8 or BF16 format:

- CNN models: INT8 or BF16
- Transformer models: BF16

Quantization introduces several challenges, primarily revolving around the potential drop in model accuracy. Choosing the right quantization parameters—such as data type, bit-width, scaling factors, and the decision between per-channel or per-tensor quantization—adds layers of complexity to the design process.

**AMD Quark** is a comprehensive cross-platform deep learning toolkit designed to simplify and enhance the quantization of deep learning models. Supporting both PyTorch and ONNX models, Quark empowers developers to optimize their models for deployment on a wide range of hardware backends, achieving significant performance gains without compromising accuracy.

Examples/Tutorial:

- `AMD Quark Tutorial <https://github.com/amd/RyzenAI-SW/tree/main/tutorial/quark_quantization>`_ for Ryzen AI Deployment
- Running INT8 model on NPU using :doc:`Getting Started Tutorial <getstartex>`
- Running BF16 model on NPU using `Image Classification <https://github.com/amd/RyzenAI-SW/tree/main/example/image_classification>`_ 


For comprehensive Quark Documentation for Ryzen AI please refer to https://quark.docs.amd.com/latest/supported_accelerators/ryzenai/index.html

.. note::
   The Vitis AI Quantizer has been deprecated as of the Ryzen AI 1.3 release. AMD strongly recommends using the new AMD Quark Quantizer instead.

Legacy documentation for the deprecated Vitis AI Quantizer : :doc:`vai_quant/vai_q_quantizer`

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
