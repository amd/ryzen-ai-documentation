###########
Version 0.7
###########

Quantizer
~~~~~~~~

- Docker Containers

  - Provide CPU dockers for Pytorch, Tensorflow 1.x and Tensorflow 2.x quantizer
  - Provide GPU dockerfiles to build GPU dockers

- Pytorch Quantizer

  - Support multiple output conversion to slicing
  - Enhancement of transpose OP optimization
  - Inspector support some new IP targets for IPU

- ONNX Quantizer

  - Provide python wheel file for installation
  - Supports quantizing ONNX models for IPU as a plugin for the ONNXRuntime native quantizer.
  - Support power-of-two quantization with both QDQ and QOP format.
  - Support Non-overflow and Min-MSE quantization methods.
  - Support various quantization configurations in power-of-two quantization in both QDQ and QOP format.
   
      - Support signed and unsigned configurations.
      - Support symmetry and asymmetry configurations.
      - Support per-tensor and per-channel configurations.
  - Support bias quantization using int8 datatype for IPU.
  - Support quantization parameters (scale) refinement for IPU.
  - Support excluding certain operations from quantization for IPU.
  - Support onnx models larger than 2GB.
  - Support using CUDAExecutionProvider for calibration in quantization
  - Open source and upstreamed to Microsoft Olive Github repo

- TensorFlow 2.x Quantizer

   - Add support for exporting the quantized model onnx format.
   - Add support for the keras.layers.Activation('leaky_relu')

- TensorFlow 1.x Quantizer

   - Add support for folding Reshape and ResizeNearestNeighbor operators.
   - Add support for splitting Avgpool and Maxpool with large kernel sizes into smaller kernel sizes.
   - Add support for quantizing Sum, StridedSlice, and Maximum operators.
   - Add support for setting the input shape of the model, which is useful in the deployment of models with undefined input shapes.
   - Add support for setting the opset version in exporting onnx format

ONNXRuntime Execution Provider
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vitis ONNXRuntime Execution Provider (VOE)

   - Support for ONNX Opset version 18, ONNX Runtime 1.16.0 and ONNX version 1.13
   - Support for both C++ and Python APIs(Python version 3)
   - Support deploy model with other EPs 
   - Support falling back to CPU EP
   - Open source and upstreamed to ONNXRuntime Github repo
   - Compiler

       - Multiple Level op fusion
       - Support same muti-output opterator like chunk split 
       - Support split big pooling to small pooling        
       - Support 2-channel writeback feature for Hard-Sigmoid and Depthwise-Convolution
       - Support 1 channel GStiling
       - explicit pad-fix in CPU subgraph for 4 byte alignment
       - Tuning the performance for multiple models

IPU
~~~

- Two configurations

   - Power Optimized Overlay
      
       - Suitable for smaller AI models (1x4.xclbin)
       - Support spatial sharing, up to 4 concurrent AI workloads

   - Performance Optimized Overlay (5x4.xclbin)
       
       - Suitable for larger AI models

Known issues
~~~~~~~~~~~~
- Flow control OPs including "Loop", "If", "Reduce" not supported by VOE
- Resize OP in ONNX opset 10 or lower not supported by VOE
- Tensorflow 2.x quantizer supports models within tf.keras.model only
- Running quantizer docker in WSL on Ryzen AI laptops may encounter OOM (Out-of-memory) issue
- Run multiple concurrent models by temporal sharing on the Performance optimized overlay (5x4.xclbin) is not supported
 



..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
