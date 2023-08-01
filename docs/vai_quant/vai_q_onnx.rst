#################
ONNX Quantization 
#################

Post Training Quantization(PTQ) - Static Quantization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
The static quantization method first runs the model using a set of inputs called calibration data. During these runs, the flow computes the quantization parameters for each activation. These quantization parameters are written as constants to the quantized model and used for all inputs. The quantization tool supports the following calibration methods: MinMax, Entropy and Percentile, MinMSE.

.. code-block::
  
    import vai_q_onnx

    vai_q_onnx.quantize_static(
       model_input,
       model_output,
       calibration_data_reader,
       quant_format=vai_q_onnx.VitisQuantFormat.FixNeuron,
       calibrate_method=vai_q_onnx.PowerOfTwoMethod.MinMSE)

  
Arguments

model_input: (String) This parameter represents the file path of the model to be quantized.
model_output: (String) This parameter represents the file path where the quantized model will be saved.
calibration_data_reader: (Object or None) This parameter is a calibration data reader. It enumerates the calibration data and generates inputs for the original model. If you wish to use random data for a quick test, you can set calibration_data_reader to None. The default value is None.
quant_format: (String) This parameter is used to specify the quantization format of the model. It has the following options:
QOperator: This option quantizes the model directly using quantized operators.
QDQ: This option quantizes the model by inserting QuantizeLinear/DeQuantizeLinear into the tensor. It supports 8-bit quantization only.
VitisQuantFormat.QDQ: This option quantizes the model by inserting VAIQuantizeLinear/VAIDeQuantizeLinear into the tensor. It supports a wider range of bit-widths and configurations.
VitisQuantFormat.FixNeuron: This option quantizes the model by inserting FixNeuron (a combination of QuantizeLinear and DeQuantizeLinear) into the tensor.
calibrate_method: (String) For DPU devices, set calibrate_method to either 'vai_q_onnx.PowerOfTwoMethod.NonOverflow' or 'vai_q_onnx.PowerOfTwoMethod.MinMSE' to apply power-of-2 scale quantization. The PowerOfTwoMethod currently supports two methods: MinMSE and NonOverflow. The default method is MinMSE.

  
Running vai_q_onnx
~~~~~~~~~~~~~~~~~~
  
Quantization in ONNX Runtime refers to the linear quantization of an ONNX model. We have developed the vai_q_onnx tool as a plugin for ONNX Runtime to support more post-training quantization(PTQ) functions for quantizing a deep learning model. Post-training quantization(PTQ) is a technique to convert a pre-trained float model into a quantized model with little degradation in model accuracy. A representative dataset is needed to run a few batches of inference on the float model to obtain the distributions of the activations, which is also called quantized calibration.

vai_q_onnx supports static quantization and the usage is as follows.

vai_q_onnx Post-Training Quantization(PTQ)
Use the following steps to run PTQ with vai_q_onnx.

Preparing the Float Model and Calibration Set
Before running vai_q_onnx, prepare the float model and calibration set, including the files listed in the following table.

Table 1. Input files for vai_q_onnx

No.	Name	Description
1	float model	Floating-point ONNX models in onnx format.
2	calibration dataset	A subset of the training dataset or validation dataset to represent the input data distribution, usually 100 to 1000 images are enough.
(Recommended) Pre-processing on the Float Model
Pre-processing is to transform a float model to prepare it for quantization. It consists of the following three optional steps:

Symbolic shape inference: This is best suited for transformer models.
Model Optimization: This step uses ONNX Runtime native library to rewrite the computation graph, including merging computation nodes, and eliminating redundancies to improve runtime efficiency.
ONNX shape inference.
The goal of these steps is to improve quantization quality. ONNX Runtime quantization tool works best when the tensor’s shape is known. Both symbolic shape inference and ONNX shape inference help figure out tensor shapes. Symbolic shape inference works best with transformer-based models, and ONNX shape inference works with other models.

Model optimization performs certain operator fusion that makes the quantization tool’s job easier. For instance, a Convolution operator followed by BatchNormalization can be fused into one during the optimization, which can be quantized very efficiently.

Unfortunately, a known issue in ONNX Runtime is that model optimization can not output a model size greater than 2GB. So for large models, optimization must be skipped.

Pre-processing API is in the Python module onnxruntime.quantization.shape_inference, function quant_pre_process().

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
Arguments

input_model_path: (String) This parameter specifies the file path of the input model that is to be pre-processed for quantization.
output_model_path: (String) This parameter specifies the file path where the pre-processed model will be saved.
skip_optimization: (Boolean) This flag indicates whether to skip the model optimization step. If set to True, model optimization will be skipped, which may cause ONNX shape inference failure for some models. The default value is False.
skip_onnx_shape: (Boolean) This flag indicates whether to skip the ONNX shape inference step. The symbolic shape inference is most effective with transformer-based models. Skipping all shape inferences may reduce the effectiveness of quantization, as a tensor with an unknown shape cannot be quantized. The default value is False.
skip_symbolic_shape: (Boolean) This flag indicates whether to skip the symbolic shape inference step. Symbolic shape inference is most effective with transformer-based models. Skipping all shape inferences may reduce the effectiveness of quantization, as a tensor with an unknown shape cannot be quantized. The default value is False.
auto_merge: (Boolean) This flag determines whether to automatically merge symbolic dimensions when a conflict occurs during symbolic shape inference. The default value is False.
int_max: (Integer) This parameter specifies the maximum integer value that is to be considered as boundless for operations like slice during symbolic shape inference. The default value is 2**31 - 1.
guess_output_rank: (Boolean) This flag indicates whether to guess the output rank to be the same as input 0 for unknown operations. The default value is False.
verbose: (Integer) This parameter controls the level of detailed information logged during inference. A value of 0 turns off logging, 1 logs warnings, and 3 logs detailed information. The default value is 0.
save_as_external_data: (Boolean) This flag determines whether to save the ONNX model to external data. The default value is False.
all_tensors_to_one_file: (Boolean) This flag indicates whether to save all the external data to one file. The default value is False.
external_data_location: (String) This parameter specifies the file location where the external file is saved. The default value is "./".
external_data_size_threshold: (Integer) This parameter specifies the size threshold for external data. The default value is 1024.
Quantizing Using the vai_q_onnx API
The static quantization method first runs the model using a set of inputs called calibration data. During these runs, we compute the quantization parameters for each activation. These quantization parameters are written as constants to the quantized model and used for all inputs. Vai_q_onnx quantization tool has expanded calibration methods to power-of-2 scale/float scale quantization methods. Float scale quantization methods include MinMax, Entropy, and Percentile. Power-of-2 scale quantization methods include MinMax and MinMSE.

vai_q_onnx.quantize_static(
    model_input,
    model_output,
    calibration_data_reader,
    quant_format=vai_q_onnx.VitisQuantFormat.FixNeuron,
    calibrate_method=vai_q_onnx.PowerOfTwoMethod.MinMSE,
    input_nodes=[],
    output_nodes=[],
    extra_options=None,)
Arguments

model_input: (String) This parameter specifies the file path of the model that is to be quantized.
model_output: (String) This parameter specifies the file path where the quantized model will be saved.
calibration_data_reader: (Object or None) This parameter is a calibration data reader that enumerates the calibration data and generates inputs for the original model. If you wish to use random data for a quick test, you can set calibration_data_reader to None.
quant_format: (Enum) This parameter defines the quantization format for the model. It has the following options:
QOperator This option quantizes the model directly using quantized operators.
QDQ This option quantizes the model by inserting QuantizeLinear/DeQuantizeLinear into the tensor. It supports 8-bit quantization only.
VitisQuantFormat.QDQ This option quantizes the model by inserting VAIQuantizeLinear/VAIDeQuantizeLinear into the tensor. It supports a wider range of bit-widths and configurations.
VitisQuantFormat.FixNeuron This option quantizes the model by inserting FixNeuron (a combination of QuantizeLinear and DeQuantizeLinear) into the tensor. This is the default value.
calibrate_method: (Enum) This parameter is used to set the power-of-2 scale quantization method for DPU devices. It currently supports two methods: 'vai_q_onnx.PowerOfTwoMethod.NonOverflow' and 'vai_q_onnx.PowerOfTwoMethod.MinMSE'. The default value is 'vai_q_onnx.PowerOfTwoMethod.MinMSE'.
input_nodes: (List of Strings) This parameter is a list of the names of the starting nodes to be quantized. Nodes in the model before these nodes will not be quantized. For example, this argument can be used to skip some pre-processing nodes or stop the first node from being quantized. The default value is an empty list ([]).
output_nodes: (List of Strings) This parameter is a list of the names of the end nodes to be quantized. Nodes in the model after these nodes will not be quantized. For example, this argument can be used to skip some post-processing nodes or stop the last node from being quantized. The default value is an empty list ([]).
extra_options: (Dict or None) This parameter is a dictionary of additional options that can be passed to the quantization process. If there are no additional options to provide, this can be set to None. The default value is None.
(Optional) Evaluating the Quantized Model
If you have scripts to evaluate float models, like the models in Xilinx Model Zoo, you can replace the float model file with the quantized model for evaluation.

To support the customized FixNeuron op, the vai_dquantize module should be imported, for example:

import onnxruntime as ort
from onnxruntime_extensions import get_library_path as _lib_path
from vai_q_onnx.operators.vai_ops.qdq_ops import vai_dquantize

so = ort.SessionOptions()
so.register_custom_ops_library(_lib_path())
sess = ort.InferenceSession(model, so)
input_name = sess.get_inputs()[0].name
results_outputs = sess.run(None, {input_name: input_data})
After that, evaluate the quantized model just as the float model.

(Optional) Dumping the Simulation Results
Sometimes after deploying the quantized model, it is necessary to compare the simulation results on the CPU/GPU and the output values on the DPU. You can use the dump_model API of vai_q_onnx to dump the simulation results with the quantized_model. Currently, only models containing fixneuron nodes support this feature.

# This function dumps the simulation results of the quantized model,
# including weights and activation results.
vai_q_onnx.dump_model(
    model,
    dump_data_reader=None,
    random_data_reader_input_shape=[],
    dump_float=False,
    output_dir='./dump_results',)
Arguments

model: (String) This parameter specifies the file path of the quantized model whose simulation results are to be dumped.
dump_data_reader: (CalibrationDataReader or None) This parameter is a data reader that is used for the dumping process. The first batch will be taken as input. If you wish to use random data for a quick test, you can set dump_data_reader to None. The default value is None.
random_data_reader_input_shape: (List or Tuple of Int) If dynamic axes of inputs require specific value, users should provide its shapes when using internal random data reader (That is, set dump_data_reader to None). The basic format of shape for single input is list (Int) or tuple (Int) and all dimensions should have concrete values (batch dimensions can be set to 1). For example, random_data_reader_input_shape=[1, 3, 224, 224] or random_data_reader_input_shape=(1, 3, 224, 224) for single input. If the model has multiple inputs, it can be fed in list (shape) format, where the list order is the same as the onnxruntime got inputs. For example, random_data_reader_input_shape=[[1, 1, 224, 224], [1, 2, 224, 224]] for 2 inputs. Moreover, it is possible to use dict {name : shape} to specify a certain input, for example, random_data_reader_input_shape={"image" : [1, 3, 224, 224]} for the input named "image". The default value is [].
dump_float: (Boolean) This flag determines whether to dump the floating-point value of nodes' results. If set to True, the float values will be dumped. Note that this may require a lot of storage space. The default value is False.
output_dir: (String) This parameter specifies the directory where the dumped simulation results will be saved. After successful execution of the function, dump results are generated in this specified directory. The default value is './dump_results'.
Note: The batch_size of the dump_data_reader will be better to set to 1 for DPU debugging.

Dump results of each FixNeuron node (including weights and activation) are generated in output_dir after the command has been successfully executed.

For each quantized node, results are saved in *.bin and *.txt formats (* represents the output name of the node). If "dump_float" is set to True, output of all nodes are saved in *_float.bin and *_float.txt (* represents the output name of the node), please note that this may require a lot of storage space.

Examples of dumping results are shown in the

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
