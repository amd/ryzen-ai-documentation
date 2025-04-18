##################
Model Quantization
##################

**Model quantization** is the process of mapping high-precision weights/activations to a lower precision format, such as BF16/INT8, while maintaining model accuracy. This technique enhances the computational and memory efficiency of the model for deployment on NPU devices. It can be applied post-training, allowing existing models to be optimized without the need for retraining.

The Ryzen AI compiler supports input models quantized to either INT8 or BF16 format:

- CNN models: INT8 or BF16
- Transformer models: BF16

Quantization introduces several challenges, primarily revolving around the potential drop in model accuracy. Choosing the right quantization parameters—such as data type, bit-width, scaling factors, and the decision between per-channel or per-tensor quantization—adds layers of complexity to the design process.

*********
AMD Quark
*********

**AMD Quark** is a comprehensive cross-platform deep learning toolkit designed to simplify and enhance the quantization of deep learning models. Supporting both PyTorch and ONNX models, Quark empowers developers to optimize their models for deployment on a wide range of hardware backends, achieving significant performance gains without compromising accuracy.

For more challenging model quantization needs **AMD Quark** supports advanced quantization technique like **Fast Finetuning** that helps recover the lost accuracy of the quantized model. 

Documentation
=============
The complete documentation for AMD Quark for Ryzen AI can be found here: https://quark.docs.amd.com/latest/supported_accelerators/ryzenai/index.html


INT8 Examples
=============
- `AMD Quark Tutorial <https://github.com/amd/RyzenAI-SW/tree/main/tutorial/quark_quantization>`_ for Ryzen AI Deployment
- Running INT8 model on NPU using :doc:`Getting Started Tutorial <getstartex>`
- Advanced quantization techniques `Fast Finetuning and Cross Layer Equalization <https://gitenterprise.xilinx.com/VitisAI/RyzenAI-SW/blob/dev/tutorial/quark_quantization/docs/advanced_quant_readme.md>`_ for INT8 model


BF16 Examples
=============
- `Image Classification <https://github.com/amd/RyzenAI-SW/tree/main/example/image_classification>`_ using ResNet50 to run BF16 model on NPU
- `Finetuned DistilBERT for Text Classification <https://github.com/amd/RyzenAI-SW/tree/main/example/DistilBERT_text_classification_bf16>`_ 
- `Text Embedding Model Alibaba-NLP/gte-large-en-v1.5  <https://github.com/amd/RyzenAI-SW/tree/main/example/GTE>`_ 
- Advanced quantization techniques `Fast Finetuning <https://quark.docs.amd.com/latest/supported_accelerators/ryzenai/tutorial_convert_fp32_or_fp16_to_bf16.html>`_ for BF16 models.


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
