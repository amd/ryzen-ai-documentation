.. include:: icons.txt

################################
Model Compilation and Deployment
################################

The Ryzen AI Software supports deploying quantized model saved in the ONNX format. NPU supports a subset of the ONNX operators (listed here :doc:`onnx_op_support`). At runtime, the ONNX graph is automatically partitioned into multiple subgraphs by the Vitis AI ONNX Execution Provider (VAI EP). The subgraph(s) containing operators supported by the NPU are executed on the NPU. The remaining subgraph(s) are executed on the CPU. This graph partitioning and deployment technique across CPU and NPU is fully automated by the VAI EP and is totally transparent to the end-user.

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

Caching the Compiled Model
~~~~~~~~~~~~~~~~~~~~~~~~~~

Model compilation can take some time depending on the model's complexity. However, once compiled, the model is saved in the cache directory. Any subsequent execution of the ONNX Runtime script will load the precompiled model from this cache directory, reducing initialization time.

To specify a model cache folder, it is recommended to use the ``cache_dir`` and ``cache_key`` provider options. Example:

.. code-block::

   from pathlib import Path  

   providers = ['VitisAIExecutionProvider']  
   cache_dir = Path(__file__).parent.resolve()  
   provider_options = [{'cache_dir': str(cache_dir),  
                        'cache_key': 'compiled_resnet50'}]  

   session = ort.InferenceSession(model.SerializeToString(),  
                                  providers=providers,  
                                  provider_options=provider_options)  


In the example above, the cache directory is set to the absolute path of the folder containing the ONNX Runtime script being executed. Once the session is created, the compiled model is saved inside a subdirectory named compiled_resnet50 within the specified cache folder.

**Note**: In the current release, if cache_dir is not set, the default cache location varies depending on the input model:

- INT8 models: Cached in C:\temp\{user}\vaip\.cache (on Windows).
- BF16 models: Cached in the current directory where the ONNX Runtime script is executed.

**Note**: To force recompilation and ignore the cached model, unset the XLNX_ENABLE_CACHE environment variable before running the script:

.. code-block::

    set XLNX_ENABLE_CACHE=


Compilation Configuration File for BF16 Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For BF16 model compilation, a compilation configuration file must be provided through the config_file option in provider_options.

.. code-block::

     provider_options = [{
        'config_file': 'vai_ep_config.json',
        'cache_dir': str(cache_dir),  
        'cache_key': 'compiled_resnet50'
     }]

Below is an example of a standard compilation configuration file (vai_ep_config.json):

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


Setting NPU Configuration for INT8 Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the current version of the Ryzen AI software, INT8 models require additional NPU configuration via the `xclbin` provider option. This configuration is not required for BF16 models.

There are two types of NPU configurations for INT8 models: standard and benchmark. Setting the NPU configuration involves specifying a specific `.xclbin` binary file, which is provided in the installer package.

Depending on the target processor and binary type (standard/benchmark), the following .xclbin files should be used:

**For STX/KRK APUs**:

- Standard binary: ``%RYZEN_AI_INSTALLATION_PATH%\voe-4.0-win_amd64\xclbins\strix\AMD_AIE2P_Nx4_Overlay.xclbin``
- Benchmark binary: ``%RYZEN_AI_INSTALLATION_PATH%\voe-4.0-win_amd64\xclbins\strix\AMD_AIE2P_4x4_Overlay.xclbin``

**For PHX/HPT APUs**:

- Standard binary: ``%RYZEN_AI_INSTALLATION_PATH%\voe-4.0-win_amd64\xclbins\phoenix\1x4.xclbin``
- Benchmark binary: ``%RYZEN_AI_INSTALLATION_PATH%\voe-4.0-win_amd64\xclbins\phoenix\4x4.xclbin``

Example code specifying standard NPU configuration setting through xclbin provider option.

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


By default, the Ryzen AI Conda environment automatically sets the STX/KRK standard binary for all inference sessions through the XLNX_VART_FIRMWARE environment variable. However, explicitly passing the xclbin option in provider_options overrides the default setting.

.. code-block::

    > echo %XLNX_VART_FIRMWARE%
      C:\Program Files\RyzenAI\1.4.0\voe-4.0-win_amd64\xclbins\strix\AMD_AIE2P_Nx4_Overlay.xclbin


Additional Provider Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Other supported provider options 

- encryptionKey (optional): Encryption/Decryption key for the models generated. 



     
|

******************
Python API Example
******************
 
.. code-block:: python
 
    import onnxruntime

    # Add user imports
    # ...
 
    # Load inputs and perform preprocessing
    # ...

    # Create an inference session using the Vitis AI execution provider
    session = onnxruntime.InferenceSession(
                  '[model_file].onnx',
                   providers=["VitisAIExecutionProvider"],
                   provider_options=[{"config_file":"/path/to/vaip_config.json"}])

    input_shape = session.get_inputs()[0].shape
    input_name = session.get_inputs()[0].name

    # Load inputs and do preprocessing by input_shape
    input_data = [...]
    result = session.run([], {input_name: input_data})  

|

***************
C++ API Example
***************

.. code-block:: cpp

    #include <onnxruntime_cxx_api.h>
    // include user header files
    // ...
    std::string xclbin_path = "path/to/xclbin";
    std::string model_path  = "path/to/model.onnx";
    std::string config_path = "path/to/config.json";
    auto model_name = strconverter.from_bytes(model_path);
    
    _putenv_s("XLNX_VART_FIRMWARE", xclbin_path.c_str());
    
    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "quicktest");
    
    // create inference session
    auto session_options = Ort::SessionOptions();
    auto options = std::unordered_map<std::string, std::string>{ 
        {"config_file", config_path},          // Required
        {"cacheDir",    "path/to/cacheDir"},   // Optional
        {"cacheKey",    "cacheName"}           // Optional
    };
    session_options.AppendExecutionProvider_VitisAI(options);
    auto session = Ort::Session(env, model_path.data(), session_options);

    // preprocess input data
    // ...


    // get input/output names from model
    size_t                   input_count;
    size_t                   output_count;
    std::vector<const char*> input_names; 
    std::vector<const char*> output_names;
    ...
    
    // initialize input tensors
    std::vector<Ort::Value>  input_tensors;
    ... 
    
    // run inference
    auto output_tensors = session.Run(
            Ort::RunOptions(), 
            input_names.data(), input_tensors.data(), input_count, 
            output_names.data(), output_count);
 
    // postprocess output data
    // ...

|

*********************
Simultaneous Sessions
*********************

Up to eight simultaneous inference sessions can be run on the NPU. The runtime automatically schedules each inference session on available slots to maximize performance of the application. 

The performance of individual inference sessions is impacted by multiple factors, including the APU type, the NPU configuration used, the number of other inference sessions running on the NPU, and the applications running the inference sessions.

|

****************
Model Encryption
****************

To protect developers’ intellectual property, encryption is supported as a session option.
With this enabled, all the compiled models generated are encrypted using AES256.
To enable encryption, you need to pass the encryption key through the VAI EP options as follows:

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

|

**************************
Operator Assignment Report
**************************


Vitis AI EP generates a file named ``vitisai_ep_report.json`` that provides a report on model operator assignments across CPU and NPU. This file is automatically generated in the cache directory, which by default is ``C:\temp\{user}\vaip\.cache\<model_cache_key>`` if no explicit cache location is specified in the code. This report includes information such as the total number of nodes, the list of operator types in the model, and which nodes and operators runs on the NPU or on the CPU. (NOTE: Nodes and operators running on the NPU are reported under the DPU name). Additionally, the report includes node statistics, such as input to a node, the applied operation, and output from the node.


.. code-block:: 

  {
    "deviceStat": [
    {
      "name": "all",
      "nodeNum": 402,
      "supportedOpType": [
      "::Add",
      ...
      ]
    },
    {
      "name": "CPU",
      "nodeNum": 2,
      "supportedOpType": [
      "::DequantizeLinear",
      ...
      ]
    },
    {
      "name": "DPU",
      "nodeNum": 400,
      "supportedOpType": [
      "::Add",
      ...
      ]
    }
    ],
    ...

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
