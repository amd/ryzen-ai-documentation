#############################
Troubleshooting
#############################

This page addresses common issues and solutions when using Windows ML on Ryzen AI PCs.

.. contents:: Topics
   :local:
   :depth: 2

***********************
Installation and Setup
***********************

Issue: Windows App SDK Version Mismatch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** Inference fails or EPs do not load; version mismatch errors.

**Solution:** Ensure the installed Windows App SDK Python package matches the Windows App SDK version required by your sample branch (stable or preview). Run ``conda list | findstr wasdk`` to verify. Download the matching version from `Windows App SDK downloads <https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/downloads>`_.


Issue: EP Not Found or Not Registered
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** Inference fails with "execution provider not found" or similar error message.

**Solution:**

- Ensure you have called EP registration before creating the session. See :doc:`winml_ep`.
- Run the application with administrator privileges if the EP requires Microsoft Store download.
- Verify the NPU driver is installed. See :doc:`installation`.


Issue: Model Compilation Fails
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** Compilation step fails or times out.

**Solution:**

- Ensure the model is in a supported format (FP32 or QDQ). See :doc:`model_support`.
- For quantized models, verify the quantization configuration (A8W8 for CNN, A16W8 for Transformer).
- Check model opset compatibility. ONNX opset 17 is recommended. See :doc:`Model compilation and deployment <../modelrun>`.


**************
Runtime Issues
**************

Issue: NPU Not Selected
~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** Model runs on CPU or GPU instead of NPU.

**Solution:**

- Set execution policy to ``PREFER_NPU`` or explicitly use ``VitisAIExecutionProvider``. See :doc:`winml_ep`.
- Verify the NPU driver is installed and the device is recognized.
- Check that the model is compatible with the Vitis AI EP. See :doc:`model_support`.


Issue: TensorRTRTX or Pywinrt Registration Failure (Python)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** Importing ``winrt.runtime`` causes the TensorRTRTX execution provider to fail registration.

**Solution:** Run pywinrt-related code in a **separate process**. Use the subprocess pattern shown in :doc:`winml_ep` (place ``winml.py`` in the same directory as your application script).

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
