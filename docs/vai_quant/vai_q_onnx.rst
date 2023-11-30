###########################
Vitis AI Quantizer for ONNX 
###########################

********
Overview
********

The AMD-Xilinx Vitis AI Quantizer for ONNX models. It supports various configuration and functions to quantize models targeting for deployment on IPU_CNN, IPU_Transformer and CPU. It is customized based on `Quantization Tool <https://github.com/microsoft/onnxruntime/tree/main/onnxruntime/python/tools/quantization>`_ in ONNX Runtime.

The Vitis AI Quantizer for ONNX supports Post Training Quantization. This static quantization method first runs the model using a set of inputs called calibration data. During these runs, the flow computes the quantization parameters for each activation. These quantization parameters are written as constants to the quantized model and used for all inputs. The quantization tool supports the following calibration methods: MinMax, Entropy and Percentile, and MinMSE.


************
Installation
************

If you have prepared your working environment using the :ref:`automatic installation script <install-bundeld>`, the Vitis AI Quantizer for ONNX is already installed. 

Otherwise, ensure that the Vitis AI Quantizer for ONNX is correctly installed by following the :ref:`installation instructions <install-onnx-quantizer>`.
 
  
******************
Running vai_q_onnx
******************
  
Quantization in ONNX refers to the linear quantization of an ONNX model. The ``vai_q_onnx`` tool is as a plugin for the ONNX Runtime. It offers powerful post-training quantization (PTQ) functions to quantize machine learning models. Post-training quantization (PTQ) is a technique to convert a pre-trained float model into a quantized model with little degradation in model accuracy. A representative dataset is needed to run a few batches of inference on the float model to obtain the distributions of the activations, which is also called quantized calibration.

Use the following steps to run PTQ with vai_q_onnx.


1. Preparing the Float Model and Calibration Set 
================================================

Before running ``vai_q_onnx``, prepare the float model and calibration set, including these files:

- float model: Floating-point models in ONNX format.
- calibration dataset: A subset of the training dataset or validation dataset to represent the input data distribution; usually 100 to 1000 images are enough.

**Exporting PyTorch Models to ONNX**

For PyTorch models, it is recommended to use the TorchScript-based onnx exporter for exporting ONNX models. Please refer to the [PyTorch documentation for guidance](https://pytorch.org/docs/stable/onnx_torchscript.html#torchscript-based-onnx-exporter). 

Tips:

- Before exporting, please perform model.eval().
- Models with opset 13 are recommended.
- For CNN's on IPU platform, dynamic input shapes are currently not supported and only a batch size of 1 is allowed. Please ensure that the shape of input is a fixed value, and the batch dimension is set to 1.

Example code:

.. code-block::
   
   torch.onnx.export(
      model,
      input,
      model_output_path,
      opset_version=13,
      input_names=['input'],
      output_names=['output'],
   )


**NOTE:** 

* **Opset Versions**:The ONNX models must be opset 10 or higher (recommended setting 13) to be quantized by Vitis AI ONNX Quantizer. Models with opset < 10 must be reconverted to ONNX from their original framework using opset 10 or above. Alternatively, you can refer to the usage of the version converter for ONNX Version Converter https://github.com/onnx/onnx/blob/main/docs/VersionConverter.md

* **Large Models > 2GB**: Due to the 2GB file size limit of Protobuf, for ONNX models exceeding 2GB, additional data will be stored separately. Please ensure that the .onnx file and the data file are placed in the same directory. Also, please set the use_external_data_format parameter to True for large models when quantizing.


2. (Recommended) Pre-processing on the Float Model
==================================================

**NOTE:** 

ONNX model optimization cannot output a model size greater than 2GB. For models larger than 2GB, the optimization step must be skipped.

Pre-processing transforms a float model to prepare it for quantization. It consists of the following three optional steps:

- Symbolic shape inference: It is best-suited for transformer models.
- Model Optimization: This step uses the ONNX Runtime native library to rewrite the computation graph, including merging computation nodes, and eliminating redundancies to improve runtime efficiency.
- ONNX shape inference.

The goal of these steps is to improve the quantization quality. The ONNX Runtime quantization tool works best when the tensor’s shape is known. Both symbolic shape inference and ONNX shape inference help figure out tensor shapes. Symbolic shape inference works best with transformer-based models, and ONNX shape inference works with other models.

Model optimization performs certain operator fusion that makes the quantization tool’s job easier. For instance, a Convolution operator followed by BatchNormalization can be fused into one during the optimization, which can be quantized very efficiently.

Pre-processing API is in the Python module ``onnxruntime.quantization.shape_inference``, function ``quant_pre_process()``.

.. code-block::

   from onnxruntime.quantization import shape_inference

   shape_inference.quant_pre_process(
      input_model_path: str,
      output_model_path: str,
      skip_optimization: bool = False,
      skip_onnx_shape: bool = False,
      skip_symbolic_shape: bool = False,
      auto_merge: bool = False,
      int_max: int = 2**31 - 1,
      guess_output_rank: bool = False,
      verbose: int = 0,
      save_as_external_data: bool = False,
      all_tensors_to_one_file: bool = False,
      external_data_location: str = "./",
      external_data_size_threshold: int = 1024,)


**Arguments**

``input_model_path``: (String) Specifies the file path of the input model that is to be pre-processed for quantization.

``output_model_path``: (String) Specifies the file path to save the pre-processed model.

``skip_optimization``: (Boolean) Indicates whether to skip the model optimization step. If set to True, model optimization is skipped, which may cause ONNX shape inference failure for some models. The default value is False.

``skip_onnx_shape``: (Boolean) Indicates whether to skip the ONNX shape inference step. The symbolic shape inference is most effective with transformer-based models. Skipping all shape inferences may reduce the effectiveness of quantization, as a tensor with an unknown shape cannot be quantized. The default value is False.

``skip_symbolic_shape``: (Boolean) Indicates whether to skip the symbolic shape inference step. Symbolic shape inference is most effective with transformer-based models. Skipping all shape inferences may reduce the effectiveness of quantization, as a tensor with an unknown shape cannot be quantized. The default value is False.

``auto_merge``: (Boolean) Determines whether to automatically merge symbolic dimensions when a conflict occurs during symbolic shape inference. The default value is False.

``int_max``: (Integer) Specifies the maximum integer value that is to be considered as boundless for operations like slice during symbolic shape inference. The default value is 2**31 - 1.

``guess_output_rank``: (Boolean) Indicates whether to guess the output rank to be the same as input 0 for unknown operations. The default value is False.

``verbose``: (Integer) Controls the level of detailed information logged during inference. 

- 0 turns off logging (default)
- 1 logs warnings
- 3 logs detailed information. 
  

``save_as_external_data``: (Boolean) Determines whether to save the ONNX model to external data. The default value is False.

``all_tensors_to_one_file``: (Boolean) Indicates whether to save all the external data to one file. The default value is False.

``external_data_location``: (String) Specifies the file location where the external file is saved. The default value is "./".

``external_data_size_threshold``: (Integer) Specifies the size threshold for external data. The default value is 1024.

3. Quantizing Using the vai_q_onnx API
======================================

The static quantization method first runs the model using a set of inputs called calibration data. During these runs, the quantization parameters for each activation are computed. These quantization parameters are written as constants to the quantized model and used for all inputs. Vai_q_onnx quantization tool has expanded calibration methods to power-of-2 scale/float scale quantization methods. Float scale quantization methods include MinMax, Entropy, and Percentile. Power-of-2 scale quantization methods include MinMax and MinMSE.

.. code-block::

   vai_q_onnx.quantize_static(
      model_input,
      model_output,
      calibration_data_reader,
      quant_format=vai_q_onnx.QuantFormat.QDQ,
      calibrate_method=vai_q_onnx.PowerOfTwoMethod.MinMSE,
      activation_type=QuantType.QUInt8,
      weight_type=QuantType.QInt8,
      input_nodes=[],
      output_nodes=[],
      enable_dpu=True,
      extra_options={'ActivationSymmetric':True}
   )

**Arguments**

* **model_input**: (String) This parameter represents the file path of the model to be quantized.
* **model_output**: (String) This parameter represents the file path where the quantized model will be saved.
* **calibration_data_reader**: (Object or None) This parameter is a calibration data reader. It enumerates the calibration data and generates inputs for the original model. If you wish to use random data for a quick test, you can set calibration_data_reader to None. The default value is None.
* **quant_format**: (String) This parameter is used to specify the quantization format of the model. It has the following options:

  -  vai_q_onnx.QuantFormat.QOperator: This option quantizes the model directly using quantized operators.
  -  vai_q_onnx.QuantFormat.QDQ: This option quantizes the model by inserting QuantizeLinear/DeQuantizeLinear into the tensor. It supports 8-bit quantization only.
  -  vai_q_onnx.VitisQuantFormat.QDQ: This option quantizes the model by inserting VitisQuantizeLinear/VitisDeQuantizeLinear into the tensor. It supports a wider range of bit-widths and configurations.
  -  vai_q_onnx.VitisQuantFormat.FixNeuron (Experimental): This option quantizes the model by inserting FixNeuron (a combination of QuantizeLinear and DeQuantizeLinear) into the tensor. This quant format is currently experimental and cannot be used for actual deployment.
* **calibrate_method**: (String) The method used in calibration, default to vai_q_onnx.PowerOfTwoMethod.MinMSE.

 -  For IPU_CNN platforms, power-of-two methods should be used, options are:
  -  vai_q_onnx.PowerOfTwoMethod.NonOverflow: This method get the power-of-two quantize parameters for each tensor to make sure min/max values not overflow.
  -  vai_q_onnx.PowerOfTwoMethod.MinMSE: This method get the power-of-two quantize parameters for each tensor to minimize the mean-square-loss of quantized values and float values. This takes longer time but usually gets better accuracy.

 -  For IPU_Transformer or CPU platforms, float scale methods should be used, options are:
  -  vai_q_onnx.CalibrationMethod.MinMax: This method obtains the quantization parameters based on the minimum and maximum values of each tensor.
  -  vai_q_onnx.CalibrationMethod.Entropy: This method determines the quantization parameters by considering the entropy algorithm of each tensor's distribution.
  -  vai_q_onnx.CalibrationMethod.Percentile: This method calculates quantization parameters using percentiles of the tensor values.

* **activation_type**: (QuantType) Specifies the quantization data type for activations.
* **weight_type**: (QuantType) Specifies the quantization data type for weights, For DPU/IPU devices, this must be set to QuantType.QInt8.
* **enable_dpu**: (Boolean) This parameter is a flag that determines whether to generate a quantized model that adapts the approximations and constraints the DPU/IPU. If set to True, the quantization process will consider the specific limitations and requirements of the DPU/IPU.
* **input_nodes**:  (List of Strings) This parameter is a list of the names of the starting nodes to be quantized. Nodes in the model before these nodes will not be quantized. For example, this argument can be used to skip some pre-processing nodes or stop the first node from being quantized. The default value is an empty list ([]).
* **output_nodes**: (List of Strings) This parameter is a list of the names of the end nodes to be quantized. Nodes in the model after these nodes will not be quantized. For example, this argument can be used to skip some post-processing nodes or stop the last node from being quantized. The default value is an empty list ([]).
* **enable_dpu**:  (Boolean) This parameter is a flag that determines whether to generate a quantized model that is suitable for the DPU/IPU. If set to True, the quantization process will consider the specific limitations and requirements of the DPU/IPU, thus creating a model that is optimized for DPU/IPU computations
* **extra_options**:  (Dictionary or None) Contains key-value pairs for various options in different cases.
  -  ActivationSymmetric: (Boolean) If True, symmetrize calibration data for activations. For DPU/IPU, this need be set to True.
  For more details of the extra_options parameters, please refer to the [extra_options](#extra_options).




*************************
Recommended Configuration
*************************

Configurations For CNN's On IPU  
===============================

To accelerate inference of CNN-based models on the IPU, the recommended configuration is as follows:

.. code-block::

   from onnxruntime.quantization import QuantFormat, QuantType 
   import vai_q_onnx

   vai_q_onnx.quantize_static(
      model_input,
      model_output,
      calibration_data_reader,
      quant_format=vai_q_onnx.QuantFormat.QDQ,
      calibrate_method=vai_q_onnx.PowerOfTwoMethod.MinMSE,
      activation_type=vai_q_onnx.QuantType.QUInt8,
      weight_type=vai_q_onnx.QuantType.QInt8,
      enable_dpu=True,
      extra_options={'ActivationSymmetric':True}
   )


Configurations For Transformers On IPU
======================================

To accelerate inference of Transformer-based models on the IPU, the recommended configuration is as follows:

.. code-block::

   import vai_q_onnx

   vai_q_onnx.quantize_static(
      model_input,
      model_output,
      calibration_data_reader,
      quant_format=vai_q_onnx.QuantFormat.QDQ,
      calibrate_method=vai_q_onnx.CalibrationMethod.MinMax,
      activation_type=vai_q_onnx.QuantType.QInt8,
      weight_type=vai_q_onnx.QuantType.QInt8,
   )


Configurations For CPU  
======================

To accelerate CNN models on CPU, the recommended configuration is as follows:

.. code-block::

   import vai_q_onnx

   vai_q_onnx.quantize_static(
      model_input,
      model_output,
      calibration_data_reader,
      quant_format=vai_q_onnx.QuantFormat.QDQ,
      calibrate_method=vai_q_onnx.CalibrationMethod.MinMax,
      activation_type=vai_q_onnx.QuantType.QUInt8,
      weight_type=vai_q_onnx.QuantType.QInt8
   )


******************************
Quantizing to Other Precisions
******************************


**NOTE:**

  The current release of the Vitis AI Execution Provider ingests quantized ONNX models with INT8/UINT8 data types only. No support is provided for direct deployment of models with other precisions, including FP32.


In addition to the INT8/UINT8, the VAI_Q_ONNX API supports quantizing models to other data formats, including INT16/UINT16, INT32/UINT32, Float16 and BFloat16, which can provide better accuracy or be used for experimental purposes. These new data formats are achieved by a customized version of QuantizeLinear and DequantizeLinear named "VitisQuantizeLinear" and "VitisDequantizeLinear", which expands onnxruntime's UInt8 and Int8 quantization to support UInt16, Int16, UInt32, Int32, Float16 and BFloat16. This customized Q/DQ was implemented by a custom operations library in VAI_Q_ONNX using onnxruntime's custom operation C API.

The custom operations library was developed based on Linux and does not currently support compilation on Windows. If you want to run the quantized model that has the custom Q/DQ on Windows, it is recommended to switch to WSL as a workaround.

To use this feature, the ```quant_format``` should be set to VitisQuantFormat.QDQ. The ```quant_format``` is set to ```QuantFormat.QDQ``` for accelerating both CNN's and transformers on the IPU target. 



1. Quantizing Float32 Models to Int16 or Int32 
==============================================


The quantizer supports quantizing float32 models to Int16 and Int32 data formats. To enable this, you need to set the "activation_type" and "weight_type" in the quantize_static API to the new data types. Options are ```VitisQuantType.QInt16/VitisQuantType.QUInt16``` for Int16, and ```VitisQuantType.QInt32/VitisQuantType.QUInt32``` for Int32.

.. code-block::

   vai_q_onnx.quantize_static(
      model_input,
      model_output,
      calibration_data_reader,
      calibrate_method=vai_q_onnx.PowerOfTwoMethod.MinMSE,
      quant_format=vai_q_onnx.VitisQuantFormat.QDQ,
      activation_type=vai_q_onnx.VitisQuantType.QInt16,
      weight_type=vai_q_onnx.VitisQuantType.QInt16,
   )


2. Quantizing Float32 Models to Float16 or BFloat16
===================================================


Besides integer data formats, the quantizer also supports quantizing float32 models to float16 and bfloat16 data formats, by setting the "activation_type" and "weight_type" to ```VitisQuantType.QFloat16``` or ```VitisQuantType.QBFloat16``` respectively.

.. code-block::

   vai_q_onnx.quantize_static(
      model_input,
      model_output,
      calibration_data_reader,
      calibrate_method=vai_q_onnx.PowerOfTwoMethod.MinMSE,
      quant_format=vai_q_onnx.VitisQuantFormat.QDQ,
      activation_type=vai_q_onnx.VitisQuantType.QFloat16,
      weight_type=vai_q_onnx.VitisQuantType.QFloat16,
   )


3. Quantizing Float32 Models to Mixed Data Formats
==================================================


The quantizer supports setting the activation and weight to different precisions. For example, activation is Int16 while weight is set to Int8. This can be used when pure Int8 quantization does not meet the accuracy requirements.

.. code-block::
      
   vai_q_onnx.quantize_static(
      model_input,
      model_output,
      calibration_data_reader,
      calibrate_method=vai_q_onnx.PowerOfTwoMethod.MinMSE,
      quant_format=vai_q_onnx.VitisQuantFormat.QDQ,
      activation_type=vai_q_onnx.VitisQuantType.QInt16,
      weight_type=QuantType.QInt8,
   )


4. Quantizing Float16 Models
============================


For models in float16, we recommend setting convert_fp16_to_fp32 to True. This will first convert your float16 model to a float32 model before quantization, reducing redundant nodes such as cast in the model.

.. code-block::
      
   vai_q_onnx.quantize_static(
      model_input,
      model_output,
      calibration_data_reader,
      quant_format=QuantFormat.QDQ,
      calibrate_method=vai_q_onnx.PowerOfTwoMethod.MinMSE,
      activation_type=QuantType.QUInt8,
      weight_type=QuantType.QInt8,
      enable_dpu=True,
      convert_fp16_to_fp32=True,
      extra_options={'ActivationSymmetric':True}
   )


5. Converting NCHW Models to NHWC and Quantize
==============================================


NHWC input shape typically yields better acceleration performance compared to NCHW on IPU. VAI_Q_ONNX facilitates the conversion of NCHW input models to NHWC input models by setting "convert_nchw_to_nhwc" to True. Please note that the conversion steps will be skipped if the model is already NHWC or has non-convertable input shapes.

.. code-block::
      
   vai_q_onnx.quantize_static(
      model_input,
      model_output,
      calibration_data_reader,
      quant_format=QuantFormat.QDQ,
      calibrate_method=vai_q_onnx.PowerOfTwoMethod.MinMSE,
      activation_type=QuantType.QUInt8,
      weight_type=QuantType.QInt8,
      enable_dpu=True,
      extra_options={'ActivationSymmetric':True},
      convert_nchw_to_nhwc=True,
   )


6. Quantizing Using CrossLayerEqualization(CLE)
===============================================

CrossLayerEqualization (CLE) is a technique used to improve PTQ accuracy. It can equalize the weights of consecutive convolution layers, making the model weights easier to perform per-tensor quantization. Experiments show that using CLE technique can improve the PTQ accuracy of some models, especially for models with depthwise_conv layers, such as MobileNet. Here is an example showing how to enable CLE using VAI_Q_ONNX.

.. code-block::
      
   vai_q_onnx.quantize_static(
      model_input,
      model_output,
      calibration_data_reader,
      quant_format=QuantFormat.QDQ,
      calibrate_method=vai_q_onnx.PowerOfTwoMethod.MinMSE,
      activation_type=QuantType.QUInt8,
      weight_type=QuantType.QInt8,
      enable_dpu=True,
      include_cle=True,
      extra_options={
         'ActivationSymmetric':True,
         'ReplaceClip6Relu': True,
         'CLESteps': 1,
         'CLEScaleAppendBias': True,
         },
   )

**Arguments**

* **include_cle**:  (Boolean) This parameter is a flag that determines whether to optimize the models using CrossLayerEqualization; it can improve the accuracy of some models. The default is False.

* **extra_options**:  (Dictionary or None) Contains key-value pairs for various options in different cases. Options related to CLE are:
  -  ReplaceClip6Relu: (Boolean) If True, Replace Clip(0,6) with Relu in the model. The default value is False.
  -  CLESteps: (Int): Specifies the steps for CrossLayerEqualization execution when include_cle is set to true, The default is 1, When set to -1, an adaptive CrossLayerEqualization steps will be conducted. The default value is 1.
  -  CLEScaleAppendBias: (Boolean) Whether the bias be included when calculating the scale of the weights, The default value is True.


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
