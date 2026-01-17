##################
Model Quantization
##################

**Model quantization** is the process of mapping high-precision weights/activations to a lower precision format, such as BF16/INT8, while maintaining model accuracy. This technique enhances the computational and memory efficiency of the model for deployment on NPU devices. It can be applied post-training, allowing existing models to be optimized without the need for retraining.

The Ryzen AI compiler supports input models in the following formats: 

- CNN Models

  - INT8 (quantized)
  - FP32 (automatically converted to BF16 during compilation)

- Transformer Models: 

  - FP32 (automatically converted to BF16 during compilation)

Ryzen AI Software natively supports both CNN and Transformer models in floating-point (FP32) format. When FP32 models are provided as input, the VitisAI EP automatically converts them to bfloat16 (BF16) precision and processes them through the optimized BF16 compilation pipeline. 

For CNN models, AMD Quark quantization enables conversion to INT8 format, delivering improved inference performance compared to higher precision alternatives. This quantization pathway provides an additional optimization option for CNN workloads requiring maximum efficiency.

The complete list of operations supported for different quantization types can be found in :doc:`Supported Operations <ops_support>`.

***********************
FP32 to BF16 Conversion
***********************
Ryzen AI provides seamless support for deploying original floating-point (FP32) models on NPU hardware through automatic conversion to BFLOAT16 (BF16) format. The conversion from FP32 to BF16 is performed when the model is compiled by the VitisAI EP. BF16 is a 16-bit floating-point format designed to have the same exponent size as FP32, allowing a wide dynamic range, but with reduced precision to save memory and speed up computations. This feature enables developers to deploy models in their native format while leveraging the Ryzen AI automatic conversion for efficient execution on NPU.

FP32 to BF16 Examples
~~~~~~~~~~~~~~~~~~~~~
Explore these practical examples demonstrating FP32 to BF16 conversion across different CNN, NLP model types:

- `Image Classification <https://github.com/amd/RyzenAI-SW/tree/main/CNN-examples/image_classification>`_ using ResNet50 model on NPU
- `Text Embedding Model Alibaba-NLP/gte-large-en-v1.5  <https://github.com/amd/RyzenAI-SW/tree/main/Transformer-examples/gte-large-en-v1.5-bf16>`_ 
- `Finetuned DistilBERT for Text Classification <https://github.com/amd/RyzenAI-SW/tree/main/Transformer-examples/DistilBERT_text_classification_bf16>`_ 
- Advanced quantization techniques `Fast Finetuning <https://quark.docs.amd.com/latest/supported_accelerators/ryzenai/tutorial_convert_fp32_or_fp16_to_bf16.html>`_ for BF16 models.

***********************
FP32 to INT8 Conversion 
***********************

Quantization to INT8 format introduces several challenges, primarily revolving around the potential drop in model accuracy. Choosing the right quantization parameters—such as data type, bit-width, scaling factors, and the decision between per-channel or per-tensor quantization—adds layers of complexity to the design process. These decisions significantly impact both model accuracy and performance. While **AMD Quark** is the recommended quantization tool, third-party tools that support QDQ (Quantize-Dequantize) operations can also be used for model quantization.

RyzenAI supports the following INT8 datatypes:

- XINT8: uses symmetric INT8 activation and weights quantization with power-of-two scales
- A8W8: uses symmetric INT8 activation and weights quantization with float scales
- A16W8: uses symmetric INT16 activation and symmetric INT8 weights quantization with float scales

`AMD Quark <https://quark.docs.amd.com/latest/supported_accelerators/ryzenai/index.html>`_ is the recommended quantization tool to convert FP32 models to INT8. But third-party tools that support QDQ (Quantize-Dequantize) operations can also be used for model quantization to A8W8 and A16W8.

AMD Quark
~~~~~~~~~

`AMD Quark <https://quark.docs.amd.com/latest/supported_accelerators/ryzenai/index.html>`_ is a comprehensive cross-platform deep learning toolkit designed to simplify and enhance the quantization of deep learning models. Supporting both PyTorch and ONNX models, Quark empowers developers to optimize their models for deployment on a wide range of hardware backends, achieving significant performance gains without compromising accuracy.

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

FP32 to INT8 Examples
~~~~~~~~~~~~~~~~~~~~~
Explore practical INT8 quantization examples:

- Running INT8 model on NPU using :doc:`Getting Started Tutorial <getstartex>`
- `AMD Quark Tutorial <https://github.com/amd/RyzenAI-SW/tree/main/CNN-examples/quark_quantization>`_ for Ryzen AI Deployment
- Advanced quantization techniques `Fast Finetuning and Cross Layer Equalization <https://github.com/amd/RyzenAI-SW/blob/main/CNN-examples/quark_quantization/docs/advanced_quant_readme.md>`_ for INT8 model

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
