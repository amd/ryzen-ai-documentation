.. include:: /icons.txt

################################
Model Compilation and Deployment
################################

The Ryzen AI Software supports deploying quantized model saved in the ONNX format. NPU supports a subset of the ONNX operators. At runtime, the ONNX graph is automatically partitioned into multiple subgraphs by the Vitis AI ONNX Execution Provider (VAI EP). The subgraph(s) containing operators supported by the NPU are executed on the NPU. The remaining subgraph(s) are executed on the CPU. This graph partitioning and deployment technique across CPU and NPU is fully automated by the VAI EP and is totally transparent to the end-user.

|memo| **NOTE**: Models with ONNX opset 17 are recommended. If your model uses a different opset version, consider converting it using the `ONNX Version Converter <https://github.com/onnx/onnx/blob/main/docs/VersionConverter.md>`_

*****************
Model Compilation
*****************

Quantized models are compiled for the NPU when an ONNX inference session is created using the Vitis AI Execution Provider (VAI EP):

.. code-block:: python

  providers = ['VitisAIExecutionProvider']
  session = ort.InferenceSession(model, sess_options = sess_opt,
                                            providers = providers,
                                            provider_options = provider_options)


The ``provider_options`` parameter allows passing compile-specific options for the Vitis AI Execution Provider (VAI EP). Below are some commonly used options:

.. list-table:: 
   :widths: 20 35
   :header-rows: 1

   * - Provider Options
     - Description 
   * - config_file
     - Configuration file to pass certain compile-specific options, used for BF16 compilation.
   * - xclbin
     - NPU binary file to specify NPU configuration, used for INT8 models.
   * - cache_dir
     - The path and name of the cache directory.
   * - cache_key
     - The subfolder in the cache directory where the compiled model is stored.
   * - encryptionKey
     - Used for generating an encrypted compiled model.

Detailed usage of these options is discussed in the subsequent section of this page.



.. _compile-bf16:

Compilation of BF16 models
==========================

For BF16 model compilation, a compilation configuration file must be provided through the ``config_file`` option in provider_options.

.. code-block::

     provider_options = [{
        'config_file': 'vai_ep_config.json',
        'cache_dir': str(cache_dir),  
        'cache_key': 'compiled_resnet50'
     }]

Below is an example of a standard BF16 model compilation configuration file:

.. code-block::

   {
    "passes": [
        {
            "name": "init",
            "plugin": "vaip-pass_init"
        },
        {
            "name": "vaiml_partition",
            "plugin": "vaip-pass_vaiml_partition",
            "vaiml_config": {}
        }
    ]
   }


The ``vaiml_config`` section allows additional configurations in specific cases. Below are few such options:

**Performance Optimization**

The default compilation optimization level is 1. The optimization level can be changed as follows:

.. code-block::

    "vaiml_config": {"optimize_level": 2}

Supported values: 1 (default), 2


**Automatic FP32 to BF16 Conversion** 

If a FP32 model is passed, the compiler can automatically cast it to BF16. This method is not recommended, as it is advisable to quantize the model to BF16 using Quark for better accuracy control. However, this method can be useful for quick prototyping.

.. code-block::

    "vaiml_config": {"enable_f32_to_bf16_conversion": true}

Supported values: false (default), true


**Optimizations for Transformer-Based Models**

By default, the compiler vectorizes the data to optimize performance for CNN models. However, transformers perform best with unvectorized data. To better optimize transformer-based models, set:

.. code-block::

    "vaiml_config": {"preferred_data_storage": "unvectorized"}

Supported values: "vectorized" (default), "unvectorized"


.. _compile-int8:

Compilation of INT8 models
==========================

In the current version of the Ryzen AI software, INT8 models require additional NPU configuration via the ``xclbin`` provider option. This configuration is not required for BF16 models.

There are two types of NPU configurations for INT8 models: standard and benchmark. Setting the NPU configuration involves specifying a specific ``.xclbin`` binary file, which is located in the Ryzen AI Software installation tree.

Depending on the target processor and binary type (standard/benchmark), the following ``.xclbin`` files should be used:

**For STX/KRK APUs**:

- Standard binary: ``%RYZEN_AI_INSTALLATION_PATH%\voe-4.0-win_amd64\xclbins\strix\AMD_AIE2P_Nx4_Overlay.xclbin``
- Benchmark binary: ``%RYZEN_AI_INSTALLATION_PATH%\voe-4.0-win_amd64\xclbins\strix\AMD_AIE2P_4x4_Overlay.xclbin``

**For PHX/HPT APUs**:

- Standard binary: ``%RYZEN_AI_INSTALLATION_PATH%\voe-4.0-win_amd64\xclbins\phoenix\1x4.xclbin``
- Benchmark binary: ``%RYZEN_AI_INSTALLATION_PATH%\voe-4.0-win_amd64\xclbins\phoenix\4x4.xclbin``

Example code selecting the standard NPU configuration for STX/KRK through the ``xclbin`` provider option.

.. code-block::

   import os
   from pathlib import Path  

   providers = ['VitisAIExecutionProvider']

   cache_dir = Path(__file__).parent.resolve()

   provider_options = [{
    'cache_dir': str(cache_dir),  
    'cache_key': 'compiled_resnet50', 
    'xclbin': '{}\\voe-4.0-win_amd64\\xclbins\\strix\\AMD_AIE2P_Nx4_Overlay.xclbin'.format(os.environ["RYZEN_AI_INSTALLATION_PATH"]) 
   }]

   session = ort.InferenceSession(model.SerializeToString(),  
                                  providers=providers,  
                                  provider_options=provider_options)


By default, the Ryzen AI Conda environment automatically sets the standard binary for all inference sessions through the ``XLNX_VART_FIRMWARE`` environment variable. However, explicitly passing the xclbin option in the provider options overrides the environment variable.

.. code-block::

    > echo %XLNX_VART_FIRMWARE%
      C:\Program Files\RyzenAI\1.4.0\voe-4.0-win_amd64\xclbins\strix\AMD_AIE2P_Nx4_Overlay.xclbin



|

**************************
Caching the Compiled Model
**************************

To avoid the overhead of recompiling models, it can be advantageous to work with pre-compiled models. The pre-compiled models can be loaded instantenously and immediately executed on the NPU. This greatly improves the session creation time and overall end-user experience. 

The RyzenAI Software supports two mechanisms for caching compiled models:

- VitisAI EP Cache
- OnnxRuntime EP Context Cache


VitisAI EP Cache
================

The VitisAI EP supports a built-in caching mechanism. This mechanism is enabled by default. When a model is compiled for the first time, it is automatically saved in the VitisAI EP cache directory. Any subsequent creation of an ONNX Runtime session using the same model will load the precompiled model from this cache directory, thereby reducing session creation time.

To VitisAI EP cache directory is specified with the ``cache_dir`` and ``cache_key`` provider options:

- ``cache_dir`` - Specifies the path and name of the cache directory.
- ``cache_key`` - Specifies the subfolder in the cache directory where the compiled model is stored.

Example:

.. code-block::

   from pathlib import Path  

   providers = ['VitisAIExecutionProvider']  
   cache_dir = Path(__file__).parent.resolve()  
   provider_options = [{'cache_dir': str(cache_dir),  
                        'cache_key': 'compiled_resnet50'}]  

   session = ort.InferenceSession(model.SerializeToString(),  
                                  providers=providers,  
                                  provider_options=provider_options)  


In the example above, the cache directory is set to the absolute path of the folder containing the ONNX Runtime script being executed. Once the session is created, the compiled model is saved inside a subdirectory named ``compiled_resnet50`` within the specified cache folder.

|memo| **NOTE**: In the current release, if ``cache_dir`` is not set, the default cache location varies based on the type of model:

- INT8 models - ``C:\temp\{user}\vaip\.cache``
- BF16 models - The current directory where the ONNX Runtime script is executed.

|memo| **NOTE**: To force recompilation and ignore the cached model, unset the ``XLNX_ENABLE_CACHE`` environment variable before running the application:

.. code-block::

    set XLNX_ENABLE_CACHE=




VitisAI EP Cache Encryption
---------------------------

To protect developers’ intellectual property, encryption is supported as a provider option. With this enabled, all the compiled models generated are encrypted using AES256. To enable encryption, you need to pass the encryption key through the VAI EP options as follows:

In Python:

.. code-block:: python
 
    session = onnxruntime.InferenceSession(
        '[model_file].onnx',
        providers=["VitisAIExecutionProvider"],
        provider_options=[{
            "config_file":"/path/to/vaip_config.json",
            "encryptionKey": "89703f950ed9f738d956f6769d7e45a385d3c988ca753838b5afbc569ebf35b2"
    }])

In C++:

.. code-block:: cpp

    auto onnx_model_path = "resnet50_pt.onnx"
    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "resnet50_pt");
    auto session_options = Ort::SessionOptions();
    auto options = std::unorderd_map<std::string,std::string>({});
    options["config_file"] = "/path/to/vaip_config.json";
    options["encryptionKey"] = "89703f950ed9f738d956f6769d7e45a385d3c988ca753838b5afbc569ebf35b2";

    session_options.AppendExecutionProvider("VitisAI", options);
    auto session = Ort::Experimental::Session(env, model_name, session_options);

The key is a 256-bit value represented as a 64-digit string. The model generated in the cache directory cannot be opened with Netron currently. Additionally, there is a side effect: dumping is disabled to prevent the leakage of sensitive information about the model.


OnnxRuntime EP Context Cache
============================

The Vitis AI EP supports the ONNX Runtime EP context cache feature. This features allows dumping and reloading a snapshot of the EP context before deployment. Currently, this feature is only available for INT8 models.

The user can enable dumping of the EP context by setting the ``ep.context_enable`` session option to 1. 

The following options can be used for additional control:

- ``ep.context_file_path`` – Specifies the output path for the dumped context model.
- ``ep.context_embed_mode`` – Embeds the EP context into the ONNX model when set to 1.

For further details, refer to the official ONNX Runtime documentation: https://onnxruntime.ai/docs/execution-providers/EP-Context-Design.html


EP Context Encryption
---------------------

By default, an unencrypted context model is generated, which can be used directly during inference. 

After the context model is generated, developers can use custom methods for encrypting the generated file and decrypting it before using it at runtime.

Alternatively, Vitis AI EP-managed encryption can be enabled by passing an encryption key via the ``encryptionKey`` provider option (discussed in the previous section). At runtime, the exact same encryption key must be provided to decrypt and load the context cache model.

Example Code:

.. code-block::

   
    # Compile session
    session_options = ort.SessionOptions()
    session_options.add_session_config_entry('ep.context_enable', '1') 
    session_options.add_session_config_entry('ep.context_file_path', '</path/to/context_file>') 
    session_options.add_session_config_entry('ep.context_embed_mode', '1') 

    session = ort.InferenceSession(
        model.SerializeToString(),
        sess_options=session_options,
        providers=['VitisAIExecutionProvider'],
        provider_options=[{'encryptionKey': '89703f950ed9f738d956f6769d7e45a385d3c988ca753838b5afbc569ebf35b2'}]
    )

   # Inference session
   session_options = ort.SessionOptions()
   session = ort.InferenceSession(
       path_or_bytes='</path/to/context_file>',
       sess_options=session_options,
       providers=['VitisAIExecutionProvider'],
       provider_options=[{'encryptionKey': '89703f950ed9f738d956f6769d7e45a385d3c988ca753838b5afbc569ebf35b2'}]
   )


**Note**: When compiling with encryptionKey, ensure that any existing cache directory (either the default cache directory or the directory specified by the ``cache_dir`` provider option) is deleted before compiling.

|

**************************
Operator Assignment Report
**************************


Vitis AI EP generates a file named ``vitisai_ep_report.json`` that provides a report on model operator assignments across CPU and NPU. This file is automatically generated in the cache directory if no explicit cache location is specified in the code. This report includes information such as the total number of nodes, the list of operator types in the model, and which nodes and operators runs on the NPU or on the CPU. Additionally, the report includes node statistics, such as input to a node, the applied operation, and output from the node.


.. code-block:: 

  {
   "deviceStat": [
   {
    "name": "all",
    "nodeNum": 400,
    "supportedOpType": [
     "::Add",
     "::Conv",
     ...
    ]
   },
   {
    "name": "CPU",
    "nodeNum": 2,
    "supportedOpType": [
     "::DequantizeLinear",
     "::QuantizeLinear"
    ]
   },
   {
    "name": "NPU",
    "nodeNum": 398,
    "supportedOpType": [
     "::Add",
     "::Conv",
     ...
    ]
    ...

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
