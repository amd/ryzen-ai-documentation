#########################
Development Flow Overview
#########################


The Ryzen AI Software enables developers to execute machine learning models trained in PyTorch or TensorFlow on laptops powered by AMD Ryzen™ AI. The development flow for Ryzen AI consists of three simple steps.

.. image:: images/devflow.png
   :scale: 100%
   :align: center

|

*****************
Pre-Trained Model
*****************
The Ryzen AI development flow does not require any modifications to the existing model training processes and methods. The pre-trained model (in PyTorch or TensorFlow) can be used as the starting point of the Ryzen AI flow. 

Cutting edge pre-trained and pre-quantized models can be found on the `Ryzen AI Model Zoo <https://huggingface.co/models?other=RyzenAI>`_ on Hugging Face.

************
Quantization
************
Quantization involves converting the AI model's parameters from floating-point to lower-precision representations, such as 16-bit or 8-bit integers. Quantized models are more power-efficient, utilize less memory, and offer better performance. 

**Quark** is a comprehensive cross-platform deep learning toolkit designed to simplify and enhance the quantization of deep learning models. Supporting both PyTorch and ONNX models, Quark empowers developers to optimize their models for deployment on a wide range of hardware backends, achieving significant performance gains without compromising accuracy.

For more details, refer to the :doc:`modelport` page.

**********
Deployment
**********
The AI model is deployed using the ONNX Runtime with either C++ or Python APIs. The Vitis AI Execution Provider included in the ONNX Runtime intelligently determines what portions of the AI model should run on the NPU, optimizing workloads to ensure optimal performance with lower power consumption.

For more details, refer to the :doc:`modelrun` page.


..
  ------------

  #####################################
  License
  #####################################

  Ryzen AI is licensed under MIT License. Refer to the LICENSE file for the full license text and copyright notice.
