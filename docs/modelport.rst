##################
Model Quantization 
##################

.. Quantization is the process of converting model weights and activation values from floating-point to lower-precision integer representations. Quantized models are more power-efficient, utilize less memory, and offer better performance. Ryzen AI requires INT8 quantization for inference. 

.. Trained models can be quantized using either Microsoft Olive or the AMD Vitis AI quantizer. 

.. Quantized models are exported in the ONNX format for deployment with the ONNX runtime.

.. .. rubric:: Olive

.. Olive is an easy-to-use tool, which supports post-training quantization (PTQ). 

.. For more details, refer to the :doc:`olive_quant` page.


.. .. rubric:: Vitis AI Quantizer

.. The Vitis AI quantizer provides advanced user controls and supports both post-training quantization (PTQ) and quantization-aware training (QAT). 

.. For more details, refer to the :doc:`vitis_ai_quant` page.


Quantization is the process of converting model weights and activation values from floating-point to lower-precision integer representations. Quantized models are more power-efficient, utilize less memory, and offer better performance. Ryzen AI requires INT8 quantization for inference. 

Ryzen AI software platform supports multiple quantization flows.

- Vitis AI ONNX Quantization:  Provides an easy-to-use Post Training Quantization (PTQ) flow on the pre-trained model saved in ONNX format. It generates a quantized ONNX model ready to be deployed with the Ryzen AI software platform.
- Vitis AI PyTorch Quantization: Allows quantizing models through the PyTorch framework. This flow supports both post-training quantization (PTQ) and quantization-aware training (QAT) to improve model accuracy.
- Vitis AI TensorFlow Quantization: Allows quantizing models through the TensorFlow framework. This flow supports both post-training quantization (PTQ) and quantization-aware training (QAT) to improve model accuracy.
- Microsoft Olive: Microsoft Olive framework has plugin support of Vitis AI ONNX Quantization. If you are familiar with Olive Framework and use it for other model optimization purposes, you may use this flow to enable the Vitis AI ONNX quantization through it. 


For complete details about each quantization flow, refer to the following pages:

.. toctree::
   :maxdepth: 1

   Vitis AI ONNX Quantization <./vai_quant/vai_q_onnx>
   Vitis AI PyTorch Quantization <./vai_quant/pt>
   Vitis AI TensorFlow Quantization <./vai_quant/tf2>
   Microsoft Olive Quantization <./olive_quant>

   
..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
