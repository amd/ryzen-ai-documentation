##################
Model Quantization
##################

**Model quantization** is the process of mapping high-precision weights/activations to a lower precision format, such as BF16/INT8, while maintaining model accuracy. This technique enhances the computational and memory efficiency of the model for deployment on NPU devices. It can be applied post-training, allowing existing models to be optimized without the need for retraining.

The Ryzen AI compiler supports input models in original floating-point precision (FP32) or quantized to INT8 format:

- CNN models: INT8, FP32 (with automatic conversion to BF16)
- Transformer models: FP32 (with automatic conversion to BF16)


FP32 to BF16 Examples
=====================
Ryzen AI provides default configurations that support original floating-point (FP32) models for conversion to BFLOAT16 (BF16) to deploy on NPU. BF16 is a 16-bit floating-point format designed to have same exponent size as FP32, allowing a wide dynamic range, but with reduced precision to save memory and speed up computations. This feature enables developers to deploy models in their native format while leveraging the Ryzen AI automatic conversion for efficient execution on NPU.

For more details
~~~~~~~~~~~~~~~~
- `Image Classification <https://github.com/amd/RyzenAI-SW/tree/main/example/image_classification>`_ using ResNet50 model on NPU
- `Finetuned DistilBERT for Text Classification <https://github.com/amd/RyzenAI-SW/tree/main/example/DistilBERT_text_classification_bf16>`_ 
- `Text Embedding Model Alibaba-NLP/gte-large-en-v1.5  <https://github.com/amd/RyzenAI-SW/tree/main/example/gte-large-en-v1.5-bf16>`_ 
- Advanced quantization techniques `Fast Finetuning <https://quark.docs.amd.com/latest/supported_accelerators/ryzenai/tutorial_convert_fp32_or_fp16_to_bf16.html>`_ for BF16 models.


INT8 Examples
=============

Quantization introduces several challenges, primarily revolving around the potential drop in model accuracy. Choosing the right quantization parameters—such as data type, bit-width, scaling factors, and the decision between per-channel or per-tensor quantization—adds layers of complexity to the design process.
The list of operations supported for different quantization types can be found in :doc:`Supported Operations <ops_support>`.

AMD Quark
~~~~~~~~~

**AMD Quark** is a comprehensive cross-platform deep learning toolkit designed to simplify and enhance the quantization of deep learning models. Supporting both PyTorch and ONNX models, Quark empowers developers to optimize their models for deployment on a wide range of hardware backends, achieving significant performance gains without compromising accuracy.

**AMD Quark** provides default configurations that support INT8 quantization. For example, `XINT8` uses symmetric INT8 activation and weights quantization with power-of-two scales using the MinMSE calibration method. 

For more challenging model quantization needs, **AMD Quark** supports different quantization configurations such as `A8W8`, `A16W8`, and advanced quantization techniques. For more details, refer to `AMD Quark for Ryzen AI <https://quark.docs.amd.com/latest/supported_accelerators/ryzenai/index.html>`_

The quantization configuration can be customized using the `QuantizationConfig` class. The following example shows how to set up the quantization configuration for INT8 quantization:

.. code-block::

   quant_config = QuantizationConfig(calibrate_method=PowerOfTwoMethod.MinMSE,
                                     activation_type=QuantType.QUInt8,
                                     weight_type=QuantType.QInt8,
                                     enable_npu_cnn=True,
                                     extra_options={'ActivationSymmetric': True})
   config = Config(global_quant_config=quant_config)
   print("The configuration of the quantization is {}".format(config))

The user can use the `get_default_config('XINT8')` function to get the default configuration for INT8 quantization.

For more details
~~~~~~~~~~~~~~~~
- `AMD Quark Tutorial <https://github.com/amd/RyzenAI-SW/tree/main/tutorial/quark_quantization>`_ for Ryzen AI Deployment
- Running INT8 model on NPU using :doc:`Getting Started Tutorial <getstartex>`
- Advanced quantization techniques `Fast Finetuning and Cross Layer Equalization <https://gitenterprise.xilinx.com/VitisAI/RyzenAI-SW/blob/dev/tutorial/quark_quantization/docs/advanced_quant_readme.md>`_ for INT8 model


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
