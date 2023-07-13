##################
Model Quantization 
##################

.. Quantization is the process of converting model weights and activation values from floating-point to lower-precision integer representations. Quantized models are more power-efficient, utilize less memory, and offer better performance. Ryzen AI requires INT8 quantization for inference. 

.. Trained models can be quantized using either Microsoft Olive or the AMD Vitis AI quantizer. 

.. Quantized models are exported in the ONNX format for deployment with the ONNX runtime.

.. .. rubric:: Olive

.. Olive is an easy-to-use tool which supports post-training quantization (PTQ). 

.. For more details, refer to the :doc:`olive_quant` page.


.. .. rubric:: Vitis AI Quantizer

.. The Vitis AI quantizer provides advanced user controls and supports both post-training quantization (PTQ) and quantization-aware training (QAT). 

.. For more details, refer to the :doc:`vitis_ai_quant` page.


Quantization is the process of converting model weights and activation values from floating-point to lower-precision integer representations. Quantized models are more power-efficient, utilize less memory, and offer better performance. Ryzen AI requires INT8 quantization for inference. 

Trained models can be quantized using either Microsoft Olive or the AMD Vitis AI quantizer. Olive is an easy-to-use tool which supports post-training quantization (PTQ). The Vitis AI quantizer provides advanced user controls and supports both post-training quantization (PTQ) and quantization-aware training (QAT). 

Quantized models are exported in the ONNX format for deployment with the ONNX runtime.


For complete details about each quantization flow, refer to the following pages:

-  :doc:`olive_quant`
-  :doc:`vitis_ai_quant`


.. toctree::
   :hidden:
   :maxdepth: 1

   Quantization with Olive <./olive_quant>
   Quantization with Vitis-AI <./vitis_ai_quant>
   
..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
