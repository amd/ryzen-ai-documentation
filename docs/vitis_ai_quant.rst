.. _quantization-with-vai:

##########################
Quantization with Vitis-AI
##########################

Vitis-AI supports Post Training Quantization directly on the pre-trained model saved in ONNX format. 

You can also perform model quantization using the Vitis AI PyTorch or TensorFlow quantization flow. Depending on your network format (PyTorch, TensorFlow 2, or Tensorflow), you can install the Vitis AI Docker container in a Linux environment to quantize your model and save it in the ONNX format. 


.. toctree::
   :maxdepth: 1

   Vitis AI ONNX Quantization <./vai_quant/vai_q_onnx>
   Vitis AI PyTorch Quantization <./vai_quant/pt>
   Vitis AI TensorFlow Quantization <./vai_quant/tf2>

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
