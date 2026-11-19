Model Quantization
==================

Model quantization is the process of converting a model's high-precision
floating-point weights and activations (for example, FP32) into a lower-precision
format. This technique is essential for deploying models efficiently on NPU
hardware, as it significantly reduces memory footprint and accelerates
computation.

This section covers BF16, INT8, and mixed precision quantization workflows for NPU deployment.

About AMD Quark
---------------

AMD Quark is a quantization toolkit for PyTorch and ONNX models. The toolkit
provides calibration and quantization tools to prepare models for NPU
deployment. Use AMD Quark to quantize models to INT8 before compilation with
the Vitis AI compiler. BF16 does not require AMD Quark (except for optional CPU
validation); it is handled automatically by the compiler.

The complete documentation for AMD Quark can be found at:
`AMD Quark documentation <https://quark.docs.amd.com>`_.

.. _install-quark:

Installing AMD Quark
~~~~~~~~~~~~~~~~~~~~

AMD Quark is not installed by the Ryzen AI installer. Activate the Ryzen AI
virtual environment and install AMD Quark version 0.13:

.. code-block:: bash

   source "$HOME/ryzen-ai-venv/bin/activate"
   pip install amd-quark==0.13

.. important::

   Ryzen AI Software for Linux 1.9 is validated with AMD Quark 0.13. Other versions might
   use different default settings and are not supported.

Quantization Workflows
----------------------

.. _quantization_bf16:

BF16 (Brain Float 16) Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Vitis AI compiler automatically converts floating-point (FP32) models to BF16
format during NPU compilation. Provide your FP32 model directly to the
compiler - no preprocessing with AMD Quark is required.

For compiler invocation details, see
:doc:`Model Compilation <../model_compilation/compiling>`.

For most deployments, no explicit BF16 quantization is needed. If you need to
debug BF16 accuracy issues on NPU, see the
`BF16 Quantization for CPU/GPU Validation`_ section at the end of
this section.

.. _quantization_int8:

INT8 Quantization using AMD Quark
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

INT8 quantization requires the AMD Quark toolkit before compilation. Use AMD
Quark with the **VINT8** configuration to convert a floating-point ONNX or
PyTorch model into a quantized INT8 model for compilation with the Vitis AI
compiler. This is the required workflow for targeting INT8.

For models where pure INT8 quantization degrades accuracy, AMD Quark supports
**mixed precision**, which keeps sensitive operations in higher precision
(FP32) while quantizing the rest to INT8. See :ref:`YOLO INT8 quantization (mixed precision) <yolo-int8-mixed-precision-quantization>` for a practical example, and
:doc:`../model_compilation/mixed_precision_compilation` for detailed
compilation patterns.

List of Supported Quark Configuration Options in Ryzen AI Software for Linux Flow
---------------------------------------------------------------------------------------------

Only the Quark configuration options listed in this section are supported in Ryzen AI Software for Linux Flow.
Options marked **Mandatory** must be set for all INT8 quantization workflows.
Options marked **Optional** are used for advanced
scenarios such as mixed precision or fast fine-tuning.

The ``VINT8`` default configuration in AMD Quark 0.13 already sets the options
required by the Vitis AI compiler (for example, ``Int32Bias``,
``DedicatedQDQPair``, ``QuantizeAllOpTypes``, ``ActivationSymmetric``, and the
``PowerOfTwoMethod.MinMSE`` calibration method). Do not set these options
explicitly.

.. raw:: latex

   \begin{landscape}
   \begingroup
   \scriptsize
   \setlength{\tabcolsep}{3pt}

.. tabularcolumns:: |>{\raggedright\arraybackslash}p{0.27\linewidth}|>{\raggedright\arraybackslash}p{0.12\linewidth}|>{\raggedright\arraybackslash}p{0.16\linewidth}|>{\raggedright\arraybackslash}p{0.40\linewidth}|

.. list-table::
   :header-rows: 1
   :widths: 27 12 16 40
   :class: longtable

   * - Quark Configuration Option
     - Required
     - Supported Value
     - Usage
   * - VINT8
     - Mandatory
     -
     - ``quant_config = QConfig.get_default_config("VINT8")``
   * - ``enable_npu_cnn``
     - Mandatory
     - True
     - ``quant_config.global_quant_config.enable_npu_cnn = True``
   * - ``subgraphs_to_exclude``
     - Optional
     - List of tuples
     - ``quant_config.global_quant_config.subgraphs_to_exclude = [(["/model.22/Concat_3"], ["/model.22/Concat_5"])]``
   * - ``nodes_to_exclude``
     - Optional
     - List of node names
     - ``quant_config.global_quant_config.nodes_to_exclude = ["/model/node1", "/model/node2"]``
   * - ``include_fast_ft``
     - Optional
     - True, False
     - ``quant_config.global_quant_config.include_fast_ft = True``
   * - ``extra_options["FastFinetune"]``
     - Optional
     - See usage column
     - ``quant_config.global_quant_config.extra_options["FastFinetune"] = {'OptimAlgorithm': 'adaround', 'OptimDevice': 'cpu', 'BatchSize': 1, 'NumIterations': 1000, 'LearningRate': 0.1}``

.. raw:: latex

   \endgroup
   \end{landscape}

For configuration parameter details and supported enum values, see the
`AMD Quark ONNX Quantization Configuration Guide
<https://quark.docs.amd.com/latest/onnx/user_guide_config_description.html>`_.

For a technical breakdown of how the MSE calibration algorithm calculates
clipping thresholds to minimize quantization noise, see the
`AMD Quark ONNX Calibration Methods Overview
<https://quark.docs.amd.com/latest/onnx/config/quantization_configuration.html>`_.

For advanced quantization workflows, see the
`AMD Quark ONNX documentation <https://quark.docs.amd.com/latest/>`_.

INT8 Quantization Example
--------------------------

The *VINT8* configuration uses symmetric INT8 activation with power-of-two
scales and is designed for Vitis AI compiler compatibility.

The following example shows the minimum required configuration for INT8
quantization with the Vitis AI compiler. Choose one of the following two calibration
options and substitute it into the ``quantizer.quantize_model`` call.

**Step 1: Configure and create the quantizer**

.. code-block:: python

   from quark.onnx import ModelQuantizer, QConfig

   # Configure quantization with the mandatory options for Vitis AI compiler
   quant_config = QConfig.get_default_config("VINT8")
   quant_config.global_quant_config.enable_npu_cnn = True

   # Create quantizer
   quantizer = ModelQuantizer(quant_config)

.. _preparing-calibration-data:

**Step 2: Provide calibration data**

Choose one of the following options.

*Option 1: Use random data (for testing only)*

When no calibration data reader is provided, the ``VINT8`` configuration
calibrates with random data automatically.

.. code-block:: python

   quantizer.quantize_model(
       model_input="model_fp32.onnx",
       model_output="model_int8.onnx",
       calibration_data_reader=None,  # Random data used automatically
   )

*Option 2: Use real calibration data (recommended for production)*

For best accuracy, provide a representative calibration dataset.
Implement a ``CalibrationDataReader`` subclass that yields
preprocessed input samples, then pass an instance to ``quantize_model``.

The following minimal template is based on the AMD Quark
`CalibrationDataReader reference
<https://quark.docs.amd.com/latest/onnx/config/calibration_datasets.html#class-datareader-for-amd-quark-quantizer>`_:

.. code-block:: python

   from onnxruntime.quantization.calibrate import CalibrationDataReader

   class ImageDataReader(CalibrationDataReader):
       def __init__(self, calibration_image_folder, input_name,
                    input_height, input_width):
           self.enum_data = None
           self.input_name = input_name
           self.data_list = self._preprocess_images(
               calibration_image_folder, input_height, input_width)

       def _preprocess_images(self, image_folder, input_height,
                              input_width, batch_size=1):
           data_list = []
           # User-defined preprocessing logic (resize, normalize, transpose, ...)
           return data_list

       def get_next(self):
           if self.enum_data is None:
               self.enum_data = iter(
                   [{self.input_name: data} for data in self.data_list])
           return next(self.enum_data, None)

       def rewind(self):
           # Called by the quantizer to reset the data iterator between
           # calibration passes. Reset enum_data to None so that get_next()
           # restarts from the beginning of data_list.
           self.enum_data = None

   calib_data_reader = ImageDataReader(
       calibration_image_folder="calib_images",
       input_name="input",
       input_height=224,
       input_width=224,
   )

   quantizer.quantize_model(
       model_input="model_fp32.onnx",
       model_output="model_int8.onnx",
       calibration_data_reader=calib_data_reader,
   )

Calibration Dataset Selection Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While AMD Quark leaves calibration dataset configuration entirely
user-defined, adhering to the following guidelines prevents accuracy
degradation on target hardware.

* **Quantity:** Supply enough samples to adequately saturate the tensor
  histograms without significantly increasing compilation time. A larger
  calibration set improves histogram coverage but yields diminishing
  accuracy returns beyond a moderate sample count—balance thoroughness
  with practical runtime constraints.
* **Balance:** Select an equal number of samples across every target class
  to prevent scale-factor bias.
* **Variance:** Mix environmental factors such as lighting, angles, and
  distances. Do not use sequential video frames.
* **Cleanliness:** Exclude corrupted, heavily blurred, or extreme anomaly
  frames to prevent artificial activation spikes.
* **Pipeline Alignment:** Manually apply all production transformations,
  cropping, and normalizations before passing data to Quark. Quark does
  not preprocess raw files.

Evaluating Quantization Quality
--------------------------------

After quantizing your model, verify that quantization has not significantly
degraded output quality. AMD Quark provides an evaluation tool that compares
inference results between a baseline floating-point model and the quantized
model.

**Generating inference results for comparison**

Before running the evaluation tool, run inference with both the baseline
FP32 model and the quantized INT8 model and save the output tensors to
separate folders. The evaluation tool expects one ``.npy`` (NumPy binary)
file per sample in each folder, with consistent filenames across both
folders. The dtype and shape of each saved array must match the model output
exactly.

.. note::

   Saved arrays must be at most 2-dimensional. The SSIM metric is computed
   with OpenCV, which accepts 2D arrays only, and the evaluation tool exits
   with the following error if an array has more than two dimensions:

   .. code-block:: text

      cv2.error: OpenCV(4.11.0) ... (-215:Assertion failed)
      dims <= 2 && step[0] > 0 in function 'locateROI'

   Removing size-1 dimensions, such as the batch axis, is sufficient for most
   classification and detection outputs. Outputs that retain spatial or
   channel dimensions after this step, such as ``(1, C, H, W)`` segmentation
   or image restoration outputs, should be saved one 2D plane per file rather
   than collapsed into a single array, since flattening changes what SSIM
   measures.

.. code-block:: python

   import numpy as np
   import onnxruntime as ort
   import os

   def save_inference_results(model_path, data_reader, output_folder):
       os.makedirs(output_folder, exist_ok=True)
       session = ort.InferenceSession(model_path)
       output_name = session.get_outputs()[0].name
       data_reader.rewind()
       idx = 0
       while True:
           inputs = data_reader.get_next()
           if inputs is None:
               break
           result = session.run([output_name], inputs)[0]
           # Remove size-1 dimensions such as the batch axis; the evaluation
           # tool requires arrays of at most 2 dimensions
           result = np.squeeze(result)
           # Save as .npy -- the evaluate tool expects NumPy binary format
           np.save(os.path.join(output_folder, f"result_{idx}.npy"), result)
           idx += 1

   save_inference_results("model_fp32.onnx", calib_data_reader, "output_fp32")
   save_inference_results("model_int8.onnx", calib_data_reader, "output_int8")

The folder structure produced by the preceding script is::

   output_fp32/
       result_0.npy
       result_1.npy
       ...
   output_int8/
       result_0.npy
       result_1.npy
       ...

**Running the evaluation tool**

After generating inference results on CPU/GPU from both models (as shown in the
preceding code), run the following command to evaluate
quantization quality:

.. code-block:: bash

   python3 -m quark.onnx.tools.evaluate \
       --baseline_results_folder output_fp32 \
       --quantized_results_folder output_int8

The tool analyzes the saved inference results and reports the following
metrics:

.. list-table:: Quantization Quality Metrics
   :header-rows: 1
   :widths: 20 50 30

   * - Metric
     - Description
     - Interpretation
   * - Cosine Similarity
     - Measures directional similarity of output vectors (0 to 1, where
       1.0 = identical direction)
     - Higher is better. Values above 0.98 indicate good preservation.
   * - L2 Distance
     - Euclidean distance measuring the absolute numerical difference
       between output tensors. The magnitude depends on output tensor
       scale and size and is not comparable across models.
     - Lower is better. No universal threshold applies. Use as a
       relative indicator: compare the L2 distance before and after
       applying accuracy recovery techniques such as mixed precision
       or fast fine-tuning to confirm improvement.
   * - PSNR
     - Peak Signal-to-Noise Ratio in decibels (dB)
     - Higher is better. Values above 30 dB indicate low quantization
       noise. Thresholds are task-dependent.
   * - SSIM
     - Structural Similarity Index (0 to 1, where 1.0 = identical
       structure). Computed with OpenCV and requires 2D input arrays.
     - Higher is better. Values above 0.99 indicate excellent structural
       preservation. Thresholds are task-dependent.

**Example output**

.. code-block:: text

   Mean cos similarity: 0.9867
   Min cos similarity: 0.9761
   Mean l2 distance: 11.41
   Max l2 distance: 15.47
   Mean psnr: 30.16
   Min psnr: 26.92
   Mean ssim: 0.9931
   Min ssim: 0.9888

These signal-level metrics indicate whether the quantized model's raw
outputs are numerically close to the baseline. They do not measure
task-level accuracy such as mean average precision (mAP) for object
detection or top-1 accuracy for classification. For a complete validation
methodology, see
:doc:`Model Accuracy Validation Methodology <../model_compilation/accuracy_methodology>`.

If these metrics indicate significant degradation, mixed precision
techniques can recover performance by excluding sensitive operations from
quantization. The following case study demonstrates this approach for YOLO models.

.. _yolo-int8-mixed-precision-quantization:

YOLO INT8 Quantization: Mixed Precision Solution
-------------------------------------------------

A common issue with YOLO ONNX models is a significant drop in object
detection accuracy after quantization to INT8. This often appears as missed
detections and lower confidence scores compared to the original
floating-point model.

Problem Description
~~~~~~~~~~~~~~~~~~~

The accuracy degradation occurs because YOLO's post-processing subgraph
concatenates tensors with vastly different numerical ranges into a single
output tensor. Confidence scores are small values between 0.0 and 1.0,
while bounding box coordinates are large values representing pixel locations
(for example, 0 to 640). When combined, the quantizer must choose a single INT8
scale for the entire output. This scale is dominated by the large coordinate
values, which distorts the precision of small confidence scores and causes
severe accuracy degradation.

Solution: Exclude Post-Processing from Quantization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To resolve this, prevent the post-processing subgraph from being quantized.
Run the main model body in INT8 and perform the post-processing step
externally in floating-point precision.

.. important::

   The subgraph node names used in the example (for example, ``/model.22/Concat_3``)
   are **model-specific**. The exact names depend on the architecture of your
   particular YOLO model and how it was exported to ONNX. You must inspect
   your model to find the correct node names for the post-processing subgraph
   you wish to exclude before running the following code.

   To inspect node names, use a model visualization tool such as
   `Netron <https://netron.app>`_ or the ONNX Python API:

   .. code-block:: python

      import onnx

      model = onnx.load("your_model.onnx")
      for node in model.graph.node:
          print(node.op_type, node.name)

This is achieved by using the ``subgraphs_to_exclude`` option in the Quark
configuration. The ``subgraphs_to_exclude`` option targets a connected sequence
of nodes forming a logical processing block, such as a post-processing or NMS
subgraph. The excluded subgraph is automatically compiled to BF16 by the Vitis
AI compiler and runs entirely on the NPU, avoiding CPU fallback.

.. note::

   AMD Quark also provides a ``nodes_to_exclude`` option, which targets
   individual named nodes rather than connected subgraphs. For mixed precision
   compilation workflows, use ``subgraphs_to_exclude`` to exclude entire
   functional blocks. Use ``nodes_to_exclude`` only when a single isolated node
   must be excluded.

.. code-block:: python

   from quark.onnx import ModelQuantizer, QConfig

   # Configure quantization with mandatory options for Vitis AI compiler
   quant_config = QConfig.get_default_config("VINT8")
   quant_config.global_quant_config.enable_npu_cnn = True

   # Exclude the post-processing subgraph from INT8 quantization.
   # Replace the node names below with the correct names for your model.
   quant_config.global_quant_config.subgraphs_to_exclude = [
       (["/model.22/Concat_3"], ["/model.22/Concat_5"])
   ]

   # Create quantizer and run quantization
   quantizer = ModelQuantizer(quant_config)

   quantizer.quantize_model(
       model_input="model_fp32.onnx",
       model_output="model_int8.onnx",
       calibration_data_reader=calib_data_reader,
   )

After quantization, the excluded post-processing subgraph remains in
floating-point precision in the output model. The Vitis AI compiler
automatically converts the excluded FP32 subgraph to BF16 and runs it on the
NPU alongside the INT8 quantized body. For details on how the
compiler handles mixed precision subgraphs and how to control operator
placement, see :doc:`../model_compilation/mixed_precision_compilation`.

After running quantization with ``subgraphs_to_exclude``, re-run the
evaluation tool described in the `Evaluating Quantization Quality`_ section
to confirm that the cosine similarity, PSNR, and SSIM metrics have improved.
For model accuracy recovery methodology, see
:doc:`Model Accuracy Validation Methodology <../model_compilation/accuracy_methodology>`.

BF16 Quantization for CPU/GPU Validation
-----------------------------------------

This section is only required when debugging BF16 accuracy issues on NPU. For
standard BF16 deployments, the compiler handles conversion automatically as
described in the `BF16 (Brain Float 16) Models`_ section.

See :doc:`../model_compilation/accuracy_methodology` for when to use this
workflow.

When BF16 NPU accuracy is inadequate, you can use AMD Quark to create a BF16
model for CPU/GPU validation. This isolates BF16 quantization effects from
NPU-specific execution issues.

The following example shows BF16 quantization with the "with-cast"
configuration, which produces Cast nodes that match the Vitis AI compiler's
BF16 implementation.

.. code-block:: python

   from quark.onnx import ModelQuantizer, QConfig

   # 1. Start from the default BF16 config
   quant_config = QConfig.get_default_config("BF16")

   # 2. Enable "with-cast" mode to match NPU BF16 behavior
   #    This replaces QDQ nodes with Cast nodes
   quant_config.global_quant_config.extra_options["BF16QDQToCast"] = True

   # 3. Create quantizer and quantize
   quantizer = ModelQuantizer(quant_config)

   quantizer.quantize_model(
       model_input="models/model_fp32.onnx",
       model_output="models/model_bf16_cpu_validation.onnx",
       calibration_data_reader=calibration_dataset,  # optional for BF16
   )

.. note::

   Calibration data is optional for BF16 quantization but might improve
   accuracy. You can pass ``None`` for ``calibration_data_reader`` if
   calibration data is unavailable.

After quantization, validate the BF16 model on CPU/GPU using ONNX Runtime.
Compare the results against your FP32 baseline to measure BF16 quantization
loss.

.. important::

   The BF16 model created by Quark is used only for CPU/GPU validation. When
   compiling for NPU deployment, use the **original FP32 model** as input to
   the Vitis AI compiler. The compiler performs its own BF16 conversion
   during NPU compilation.

For the complete BF16 validation workflow and accuracy comparison
methodology, see
:doc:`../model_compilation/accuracy_methodology`.
