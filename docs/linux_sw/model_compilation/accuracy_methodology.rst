Model Accuracy Validation Methodology
======================================

Overview
--------

AI models trained in FP32 often run in lower precision formats (INT8, BF16) on AMD NPU hardware for better performance, but precision reduction can degrade accuracy. This section provides a systematic process for diagnosing accuracy loss by validating the converted or quantized model on CPU or GPU before deploying to NPU.


Why Validate on CPU First
-------------------------

When NPU accuracy is poor, you face multiple possible causes: quantization calibration, data type conversion, NPU compiler configuration, runtime settings, preprocessing differences, or hardware behavior. Without systematic isolation, you cannot distinguish between these causes, and teams often pursue NPU-specific fixes when the actual problem is poor conversion or calibration. Validating the converted or quantized model on CPU first catches these issues before NPU involvement, eliminating wasted debugging cycles.

Comparing NPU directly to the original FP32 model conflates two distinct error sources: quantization loss and NPU execution differences. When NPU differs from FP32 by 3%, you cannot tell whether the problem is 2% quantization error plus 1% NPU error, or 0.5% quantization plus 2.5% NPU error. The two-baseline approach separates these by establishing the Original Model Baseline as the upper bound (FP32 accuracy), the Quantized Model Baseline on CPU to isolate quantization quality before NPU involvement, and NPU validation that compares against the Quantized Model Baseline to isolate NPU-specific factors.

BF16 is always the starting point because it requires no manual conversion or quantization. If BF16 NPU accuracy is insufficient, use INT8 for performance-critical models (large CNNs, detection, segmentation) where calibration effort is justified by throughput gains. Mixed Precision applies only when pure INT8 fails on CPU.


Terminology
-----------

**Original Model Baseline (CPU):** Accuracy of your model in its training precision (typically FP32) on CPU/GPU. Established in Step 1, this is the upper bound. Converted or quantized models are compared against this to measure precision loss.

**Quantized Model Baseline (CPU):** Accuracy of your converted or quantized model (INT8, BF16) on CPU/GPU. Established in Step 2 through careful conversion or quantization with calibration. This becomes the reference for NPU validation. Should be as close as possible to the Original Model Baseline.

**Mixed Precision:** A quantization technique that extends INT8 by keeping sensitive operations (for example, attention layers, detection heads) in higher precision while quantizing the bulk of the model to INT8. Applied when pure INT8 quantization loses excessive accuracy on CPU.

**Tolerance:** "Within 1% tolerance" means within 1 percentage point absolute difference. For example, if a baseline achieves 85.0% accuracy, acceptable accuracy is 84.0% or higher.


Validation Workflow
-------------------

The workflow uses two distinct criteria, applied at different stages. See
:ref:`validation-workflow-steps`.

- **Quantization quality criterion (user-defined, Step 2).** How closely the Quantized
  Model Baseline on CPU must match the Original Model Baseline.
  This target depends on your use case, model, and application requirements. A classifier
  might tolerate a larger quantization gap than a safety-critical perception model.
  Set this target before starting Step 2 and use it to decide when calibration or mixed
  precision is sufficient.

- **NPU execution criterion (1% tolerance, Step 3).** How closely the NPU result must match the applicable baseline (Quantized Model Baseline when Step 2 is performed; Original Model Baseline when Step 2 is skipped). This criterion is fixed at 1% and measures NPU execution fidelity - whether the NPU faithfully runs the model that was validated on CPU. Deviations beyond 1% indicate NPU-specific issues (configuration, runtime, preprocessing).

.. _validation-workflow-steps:

.. list-table:: Validation Workflow Steps
   :header-rows: 1
   :widths: 8 35 57

   * - Step
     - Action
     - Acceptance Criterion
   * - 1
     - Establish Original Model Baseline on CPU/GPU
     - Accuracy measured, environment documented, results reproducible
   * - 2
     - Convert or quantize the model and establish the Quantized Model Baseline on CPU/GPU (optional for BF16)
     - User-defined: Quantized Model Baseline meets the application's quantization quality target (optional for BF16)
   * - 3
     - Compile with AMD Vitis™ AI and validate on NPU
     - NPU accuracy within 1% of the applicable baseline (Quantized Model Baseline when Step 2 is performed, Original Model Baseline when Step 2 is skipped)
   * - 4
     - Identify the failure mode and apply corresponding troubleshooting checks
     - Root cause identified; corrective action applied; re-enter at Step 2 or Step 3

Root Cause Isolation
^^^^^^^^^^^^^^^^^^^^

The two-baseline structure isolates the source of any accuracy gap:

- When the Quantized Model Baseline on CPU does not meet your quantization quality target, the cause is in data type conversion or calibration. Address it in Step 2 before proceeding.

- When the NPU result is outside the 1% tolerance of the Quantized Model Baseline on CPU, but the Quantized Model Baseline itself meets your quantization quality target, the cause is NPU-specific (configuration, runtime, preprocessing, or model shape). Address it in Step 4.

Step 1: Establish Original Model Baseline
------------------------------------------

Run your model in its original training precision on CPU or GPU with ONNX Runtime. Most models are trained in FP32. If your model was trained using a different precision, use that precision as your Original Model Baseline. This establishes the reference accuracy before any precision reduction for NPU deployment.

Use your complete validation dataset (the same data you'll use in production) and compute standard accuracy metrics for your model type, such as mAP for object detection, Top-1/Top-5 for classification, or F1 for segmentation.

For each validation run, record the accuracy metric values, hardware (CPU/GPU model, memory), software versions (ONNX Runtime, framework, drivers), dataset name and preprocessing, inference configuration (batch size, resolution), and the date. Reference these measurements repeatedly during troubleshooting; incomplete records make issues difficult to reproduce.


Step 2: Select Data Type and Validate on CPU/GPU
-------------------------------------------------

Compare the data type options and select one for NPU deployment: BF16 (no manual effort, recommended starting point) or INT8 (performance-critical models). The following subsections detail the workflow for each.

BF16
^^^^

BF16 is the recommended starting point for any deployment because it requires no manual conversion or quantization. The AMD Vitis™ AI compiler converts the model to BF16 automatically during NPU compilation. Keep your model in its original format (typically FP32) and skip directly to Step 3 to compile and validate on NPU.

For the default workflow, BF16 conversion happens during compilation with no CPU validation phase. The NPU result is compared directly to the Original Model Baseline. If BF16 NPU accuracy is inadequate, you can optionally perform BF16 CPU validation as described under **BF16 CPU Validation for Debugging** to isolate the issue.

BF16 CPU Validation for Debugging
""""""""""""""""""""""""""""""""""

When BF16 NPU accuracy fails to meet requirements, you might need to isolate whether the accuracy loss originates from BF16 quantization itself or from NPU-specific execution issues. Before investing in an INT8 alternative, you can use AMD Quark to create a BF16 model for CPU/GPU validation. This establishes a BF16 Quantized Model Baseline that isolates BF16 quantization effects from NPU-specific factors.

To perform BF16 CPU validation, use AMD Quark with the "with-cast" configuration to create a BF16 model (see :doc:`../model_quantization/model_quantization` for the Quark recipe). Run this BF16 model on CPU/GPU to establish the BF16 Quantized Model Baseline, then compare it against the Original Model Baseline to measure BF16 quantization loss. If the BF16 quantization loss is acceptable on CPU but NPU accuracy still fails, the issue is NPU-specific and should be addressed through Step 4 troubleshooting. If the BF16 quantization loss is unacceptable even on CPU, switch to INT8 instead.

The BF16 model created by Quark is used only for CPU/GPU validation. When compiling for NPU, always use the original FP32 model as input to the Vitis AI compiler, which performs its own BF16 conversion during NPU compilation.

The "with-cast" configuration is required because the Vitis AI compiler converts FP32 to BF16 using Cast operations. Quark's "with-cast" mode (enabled by setting BF16QDQToCast to True) produces the same Cast-based representation, ensuring CPU/GPU validation accurately reflects NPU execution. Without this flag, Quark produces QDQ nodes that do not match the NPU's BF16 implementation.

INT8
^^^^

Use INT8 for performance-critical applications and compute-intensive models such as large CNNs, detection models, and segmentation models. INT8 requires a calibration dataset and explicit quantization, and delivers the highest inference speed on NPU for most architectures. Some operations, such as detection post-processing, degrade severely under INT8 and might require mixed precision or higher-precision deployment (see Case Study).

Prepare a calibration dataset following **Calibration Dataset Guidelines**, then quantize the model using AMD Quark with the VINT8 configuration as described in :doc:`../model_quantization/model_quantization`. Validate the resulting INT8 model on CPU/GPU to establish the INT8 Quantized Model Baseline.

If the INT8 Quantized Model Baseline differs from the Original Model Baseline by more than 1%, improve calibration or apply mixed precision as described in the **Recovering INT8 Accuracy** and **Mixed Precision** subsections.

Once the INT8 Quantized Model Baseline is acceptable, compile for NPU and validate. NPU accuracy is acceptable when it falls within 1% of the INT8 Quantized Model Baseline.

Calibration Dataset Guidelines
""""""""""""""""""""""""""""""

The calibration dataset is used to estimate activation ranges during
post-training quantization. It must be realistic and representative of the
data the model will see in deployment, covering the variations relevant to
your model's domain.

Use data drawn from the same distribution as your deployment inputs. A subset
of the training or validation set is normally suitable. Do not use synthetic
or randomly generated inputs, and do not use a single batch of near-identical
samples: both produce activation ranges that do not reflect real inference
and can cause significant accuracy loss.

.. list-table:: Calibration dataset starting points
   :header-rows: 1
   :widths: 20 20 60

   * - Model type
     - Starting sample count
     - Coverage requirements
   * - Classification
     - 100 to 128
     - All classes, with varying lighting, backgrounds, and object scales
   * - Detection
     - 100 to 128
     - Different object sizes, occlusions, overlapping objects, and edge
       cases
   * - Segmentation
     - 100 to 128
     - Diverse scenes, representative class distributions, and boundary
       conditions

.. note::

   The preceding sample counts are starting points, not requirements. Calibration
   accuracy is driven more by how representative the samples are than by how
   many are used. A small, well-distributed set typically outperforms a larger
   set drawn from a narrow slice of the data.

Increase the sample count when any of the following apply:

- The model has a large number of output classes.
- The input data is highly varied (for example, mixed lighting conditions,
  multiple camera sources, or multiple capture resolutions).
- The measured accuracy gap against the floating-point baseline exceeds your
  accuracy target. 

Recovering INT8 Accuracy
""""""""""""""""""""""""

When the INT8 Quantized Model Baseline differs from the Original Model Baseline by more than 1%, first enhance the calibration dataset. Increase the dataset size toward the upper recommended range, verify coverage of all classes and edge cases, and add samples representing challenging scenarios such as occlusions, poor lighting, and scale variations. Confirm the calibration data represents your production data distribution.

If the failure is concentrated in specific classes, verify the calibration dataset represents those classes adequately. If the failure is concentrated in specific layers, or if improved calibration does not close the gap, apply mixed precision as described in the **Mixed Precision** subsection.

Mixed Precision
"""""""""""""""

Mixed precision extends INT8 quantization by excluding sensitive operations from quantization. Excluded operations remain in FP32 on CPU and are automatically converted to BF16 on NPU during compilation. Apply mixed precision when pure INT8 has unacceptable CPU accuracy and you have identified specific sensitive layers causing the degradation.

Use the standard VINT8 configuration from :doc:`../model_quantization/model_quantization` and add the ``subgraphs_to_exclude`` parameter to exclude sensitive subgraphs. The ``subgraphs_to_exclude`` option targets a connected sequence of nodes forming a logical processing block, such as a post-processing or NMS subgraph. The excluded subgraph is automatically compiled to BF16 by the Vitis AI compiler and runs entirely on the NPU, avoiding CPU fallback. Subgraph names are model-specific. Use Netron or AI Analyzer to identify the correct node names in your model. Validate the mixed precision model (INT8 + FP32) on CPU/GPU to establish the Mixed Precision Quantized Model Baseline.

Once the Mixed Precision Quantized Model Baseline is acceptable, compile for NPU. The excluded FP32 sections automatically convert to BF16, producing an INT8 model with BF16 excluded subgraphs. NPU accuracy is acceptable when it falls within 1% of the Mixed Precision Quantized Model Baseline.


Step 3: Compile and Validate on NPU
------------------------------------

After your converted or quantized model achieves acceptable accuracy on CPU or GPU, compile for NPU using the Vitis AI compiler. The compiler input depends on the data type:

- **INT8 and Mixed Precision:** Compile the quantized model created in Step 2.
- **BF16:** Always compile the **original FP32 model**, even if you performed BF16 CPU validation in Step 2. The BF16 model created by Quark is used only for CPU validation; the compiler performs its own BF16 conversion from the FP32 model.

Run the compiled model on NPU hardware using ONNX Runtime with the Vitis AI EP, using the same validation dataset and metrics you established in previous steps to ensure meaningful comparisons.

The comparison target depends on whether you performed Step 2. If you established a Quantized Model Baseline in Step 2, NPU is compared to that baseline. If you skipped Step 2 (typical for BF16), NPU is compared directly to the Original Model Baseline.

If NPU accuracy falls within 1% of the applicable baseline, proceed to deployment.

If NPU accuracy fails the 1% threshold, use the difference between CPU and NPU results to isolate the cause: when the Quantized Model Baseline (CPU) passed but NPU fails, the cause is NPU-specific and is addressed in Step 4.

For BF16 where Step 2 was skipped, you cannot isolate quantization from NPU-specific issues. If NPU accuracy is not acceptable, perform BF16 CPU validation using the workflow described in Step 2 to isolate the issue.


Step 4: Troubleshooting
-----------------------

Troubleshooting NPU-Specific Issues
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When NPU fails but the Quantized Model Baseline on CPU passes, the two most common causes are configuration file errors and preprocessing inconsistencies between environments.

Examine JSON configuration files and compiler settings to verify data types are specified correctly and consistently. Data type discrepancies in the JSON configuration file can cause poor NPU accuracy even when the quantized model performs well on CPU; correcting the JSON configuration resolves these issues.

Verify that preprocessing and postprocessing are identical between CPU/GPU and NPU. Differences in normalization values, color channel ordering (RGB vs. BGR), or resize methods cause accuracy discrepancies. For detection models, confirm that NMS (Non-Maximum Suppression) thresholds, confidence thresholds, and bounding box decoding operations are identical between environments.

Troubleshooting Data Type Conversion Issues
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When CPU/GPU accuracy is unacceptable in Step 2, the issue lies in data type conversion rather than NPU deployment, which allows you to troubleshoot without involving NPU hardware or compilation. Work through three categories of causes in order: preprocessing, export, and quantization.

For preprocessing, validate that your preprocessing matches the training pipeline exactly: the same normalization values, color format, and resize methods. Inspect input data for NaN or Inf values that can corrupt model execution.

For export, confirm the model is in evaluation mode with dropout disabled and deterministic operations enabled, and re-export from the training framework if problems persist.

If the INT8 Quantized Model Baseline fails after the export checks above, the cause is quantization-specific and requires improved calibration or mixed precision as described in Step 2.


Case Study: YOLOv8 Object Detection
------------------------------------

This case study demonstrates the INT8 validation path and shows when mixed precision becomes necessary for object detection models.

A YOLOv8m model was exported to ONNX format and validated on CPU using the COCO dataset, establishing the baseline mAP (mean Average Precision) as the Original Model Baseline. The first INT8 attempt quantized the entire model without exclusions, but CPU validation revealed near-zero mAP with most detections completely missed. Analysis showed that post-processing operations (particularly confidence scoring and bounding box concatenation) degraded severely under INT8 quantization, with quantization error sufficient to push confidence scores below detection thresholds and prevent the model from producing valid detections.

Applying mixed precision by excluding the sensitive post-processing subgraph kept it in FP32 while the rest of the model ran in INT8. CPU validation of this mixed precision configuration showed accuracy within the 1% tolerance threshold, confirming that the quantization approach itself was sound. Proceeding to NPU deployment, the Vitis AI compiler automatically converted the excluded FP32 subgraphs to BF16, resulting in INT8 + BF16 mixed precision on NPU. NPU validation revealed additional accuracy loss beyond what was observed on CPU, exceeding the 1% tolerance threshold. The gap between CPU and NPU execution indicated that the automatic FP32-to-BF16 conversion of the excluded subgraph introduced this additional degradation.

The systematic validation isolated the root cause to an NPU-specific factor (BF16 conversion of the excluded subgraph) rather than the quantization approach itself, which enabled informed decisions about deployment trade-offs: accept the accuracy loss in exchange for INT8 performance, switch to full BF16 deployment for better accuracy at some performance cost, partition the model to run sensitive operations on CPU, or invest in quantization-aware training to improve INT8 robustness.
