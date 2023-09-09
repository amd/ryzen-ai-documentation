#############
Release Notes
#############

Version 0.8
$$$$$$$$$$$

Quantizer
~~~~~~~~~

- Pytorch Quantizer

  - Pytorch 1.13 and 2.0 support
  - Mixed precision quantization support, supporting float32/float16/bfloat16/intx mixed quantization
  - Support of bit-wise accuracy cross check between quantizer and ONNX-runtime
  - Split and chunk operators were automatically converted to slicing
  - Add support for BFP data type quantization
  - Support of some operations in quantizer: where, less, less_equal, greater, greater_equal, not, and, or, eq, maximum, minimum, sqrt, Elu, Reduction_min, argmin
  - QAT supports training on multiple GPUs
  - QAT supports operations with multiple inputs or outputs

- ONNX Quantizer

  - Provided Python wheel file for installation
  - Support OnnxRuntime 1.15
  - Supports setting input shapes of random data reader
  - Supports random data reader in the dump model function
  - Supports saving the S8S8 model in U8S8 format for IPU
  - Supports simulation of Sigmoid, Swish, Softmax, AvgPool, GlobalAvgPool, ReduceMean and LeakyRelu for IPU
  - Supports node fusions for IPU
  
ONNXRuntime Execution Provider 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Supports for U8S8 quantized ONNX models
- Improve the function of falling back to CPU EP
- Improve AIE plugin framework

  - Supports LLM Demo
  - Supports Gemm ASR
  - Supports E2E AIE acceleration for Pre/Post ops
  - Improve the easy-of-use for partition and  deployment
- Supports  models containing subgraphs
- Supports report summary about OP assignment
- Supports report summary about DPU subgraphs falling back to CPU
- Improve log printing and troubleshooting tools.
- Upstreamed to ONNX Runtime Github repo for any data type support and bug fix

IPU and Compiler
~~~~~~~~~~~~~~~~

- Extended the support range of some operators

  - Larger input size: conv2d, dwc
  - Padding mode: pad
  - Broadcast: add
  - Variant dimension (non-NHWC shape): reshape, transpose, add
- Support new operators, e.g. reducemax(min/sum/avg), argmax(min)
- Enhanced multi-level fusion
- Performance enhancement for some operators
- Add quantization information validation
- Improvement in device partition

  - User friendly message
  - Target-dependency check

Demos
~~~~~

- New Demos link: https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=transformers_2308.zip

  - LLM demo with OPT-1.3B/2.7B/6.7B
  - Automatic speech recognition demo with Whisper-tiny

Known issues
~~~~~~~~~~~~
- Flow control OPs including "Loop", "If", "Reduce" not supported by VOE
- Resize OP in ONNX opset 10 or lower not supported by VOE
- Tensorflow 2.x quantizer supports models within tf.keras.model only
- Running quantizer docker in WSL on Ryzen AI laptops may encounter OOM (Out-of-memory) issue
- Run multiple concurrent models by temporal sharing on the Performance optimized overlay (5x4.xclbin) is not supported
- Support batch size 1 only for IPU


|
|
|
|


Version 0.7
$$$$$$$$$$$

Quantizer
~~~~~~~~~

- Docker Containers

  - Provided CPU dockers for Pytorch, Tensorflow 1.x, and Tensorflow 2.x quantizer
  - Provided GPU Docker files to build GPU dockers

- Pytorch Quantizer

  - Supports multiple output conversion to slicing
  - Enhanced transpose OP optimization
  - Inspector support new IP targets for IPU

- ONNX Quantizer

  - Provided Python wheel file for installation
  - Supports quantizing ONNX models for IPU as a plugin for the ONNX Runtime native quantizer
  - Supports power-of-two quantization with both QDQ and QOP format
  - Supports Non-overflow and Min-MSE quantization methods
  - Supports various quantization configurations in power-of-two quantization in both QDQ and QOP format.
   
    - Supports signed and unsigned configurations.
    - Supports symmetry and asymmetry configurations.
    - Supports per-tensor and per-channel configurations.
  - Supports bias quantization using int8 datatype for IPU.
  - Supports quantization parameters (scale) refinement for IPU.
  - Supports excluding certain operations from quantization for IPU.
  - Supports ONNX models larger than 2GB.
  - Supports using CUDAExecutionProvider for calibration in quantization
  - Open source and upstreamed to Microsoft Olive Github repo

- TensorFlow 2.x Quantizer

  - Added support for exporting the quantized model ONNX format.
  - Added support for the keras.layers.Activation('leaky_relu')

- TensorFlow 1.x Quantizer

  - Added support for folding Reshape and ResizeNearestNeighbor operators.
  - Added support for splitting Avgpool and Maxpool with large kernel sizes into smaller kernel sizes.
  - Added support for quantizing Sum, StridedSlice, and Maximum operators.
  - Added support for setting the input shape of the model, which is useful in deploying models with undefined input shapes.
  - Add support for setting the opset version in exporting ONNX format

ONNX Runtime Execution Provider
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vitis ONNX Runtime Execution Provider (VOE)

  - Supports ONNX Opset version 18, ONNX Runtime 1.16.0, and ONNX version 1.13
  - Supports both C++ and Python APIs(Python version 3)
  - Supports deploy model with other EPs 
  - Supports falling back to CPU EP
  - Open source and upstreamed to ONNX Runtime Github repo
  - Compiler

    - Multiple Level op fusion
    - Supports the  same muti-output operator like chunk split 
    - Supports split big pooling to small pooling        
    - Supports 2-channel writeback feature for Hard-Sigmoid and Depthwise-Convolution
    - Supports 1-channel GStiling
    - Explicit pad-fix in CPU subgraph for 4-byte alignment
    - Tuning the performance for multiple models

IPU
~~~

- Two configurations

  - Power Optimized Overlay
      
    - Suitable for smaller AI models (1x4.xclbin)
    - Supports spatial sharing, up to 4 concurrent AI workloads

  - Performance Optimized Overlay (5x4.xclbin)
       
    - Suitable for larger AI models

Known issues
~~~~~~~~~~~~
- Flow control OPs including "Loop", "If", "Reduce" are not supported by VOE
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
