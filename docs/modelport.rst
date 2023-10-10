##################
Model Quantization 
##################

.. contents:: Table of Contents


Quantization is the process of converting model weights and activation values from floating-point to lower-precision integer representations. Quantized models are more power-efficient, utilize less memory, and offer better performance. Ryzen AI requires INT8 quantization for inference. 

Vitis AI ONNX Quantization
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Vitis AI ONNX Quantization** provides an easy-to-use Post Training Quantization (PTQ) flow on the pre-trained model saved in ONNX format. It generates a quantized ONNX model ready to be deployed with the Ryzen AI software platform and is mostly recommended for CNN-based models. 

For more details regarding Vitis AI ONNX Quantization please refer :doc:`vai_quant/vai_q_onnx`


Alternate Quantization options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ryzen AI Software Platform supports a few other quantization tools that can be used in specific situations: 

**Vitis AI PyTorch Quantization**: Allows quantizing models through the PyTorch framework. This flow supports both post-training quantization (PTQ) and quantization-aware training (QAT) to improve model accuracy. For more details please refer :doc:`vai_quant/pt`

**Vitis AI TensorFlow Quantization**: Allows quantizing models through the TensorFlow framework. This flow supports both post-training quantization (PTQ) and quantization-aware training (QAT) to improve model accuracy. For more details please refer :doc:`vai_quant/tf2`

**Microsoft Olive**: Microsoft Olive framework has plugin support of Vitis AI ONNX Quantization. If you are familiar with Olive Framework and use it for other model optimization purposes, you may use this flow to enable the Vitis AI ONNX quantization through it. For more detail please refer :doc:`olive_quant`  


   
..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
