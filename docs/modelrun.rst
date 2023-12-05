###################
Model Deployment
###################


*********************************************
ONNX Runtime with Vitis AI Execution Provider
*********************************************

After the model is quantized, you can deploy it with ONNX Runtime by utilizing C++ or Python APIs using Vitis AI Execution Provider (VAI EP) for the inference session: 

.. code-block::

  providers = ['VitisAIExecutionProvider']
  session = ort.InferenceSession(model, sess_options = sess_opt,
                                            providers = providers,
                                            provider_options = provider_options)

****************
Provider Options
****************

VAI EP supports three provider options:


.. list-table:: 
   :widths: 25 20 20 35
   :header-rows: 1

   * - Provider Options
     - Type
     - Default 
     - Description 
   * - config_file
     - Mandatory
     - None
     - The path and name of the runtime configuration file. 
       A default version of this file can be found in the ``voe-4.0-win_amd64`` folder of the Ryzen AI software installation package under the name :file:`vaip_config.json`.
   * - cacheDir
     - Optional
     - ``C:\temp\{user}\vaip\.cache``
     - The cache directory.
   * - cacheKey
     - Optional 
     - {onnx_model_md5}
     - Compiled model directory generated inside the cache directory. Use string to specify the desired name of the compiler model directory. 
       For example: ``'cacheKey': 'resnet50_cache'``.

   * - encryptionKey
     - Optional 
     - None
     - Encryption/Decryption key for the models generated. 


*********************
Environment Variables
*********************

Additionally, use the following environment variables to control the Ryzen AI ONNX Runtime-based deployment.


.. list-table:: 
   :widths: 25 20 20 35
   :header-rows: 1

   * - Environment Variable 
     - Type
     - Default 
     - Description 
   * - XLNX_VART_FIRMWARE
     - Mandatory
     - None
     - Set it to ``C:\path\to\1x4.xclbin`` to use the throughput profile of the IPU. 
       For more details, refer to the :doc:`runtime_setup` page.
   * - XLNX_ENABLE_CACHE
     - Optional
     - 1
     - If unset, the runtime flow ignores the cache directory and recompiles the model.
     
     
******************
Python API Example
******************
 
.. code-block::
 
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


***************
C++ API Example
***************

.. code-block:: 

   // ...
   #include <experimental_onnxruntime_cxx_api.h>
   // include user header files
   // ...

   auto onnx_model_path = "resnet50_pt.onnx"
   Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "resnet50_pt");
   auto session_options = Ort::SessionOptions();

   auto options = std::unorderd_map<std::string,std::string>({});
   options["config_file"] = "/path/to/vaip_config.json";
   options["cacheDir"] = "/path/to/cache/directory";
   options["cacheKey"] = "abcdefg"; // Replace abcdefg with your model name, eg. onnx_model_md5

   // Create an inference session using the Vitis AI execution provider
   session_options.AppendExecutionProvider("VitisAI", options);

   auto session = Ort::Experimental::Session(env, model_name, session_options);

   auto input_shapes = session.GetInputShapes();
   // preprocess input data
   // ...

   // Create input tensors and populate input data
   std::vector<Ort::Value> input_tensors;
   input_tensors.push_back(Ort::Experimental::Value::CreateTensor<float>(
                           input_data.data(), input_data.size(), input_shapes[0]));

   auto output_tensors = session.Run(session.GetInputNames(), input_tensors,
                                      session.GetOutputNames());
   // postprocess output data
   // ...


****************
Model Encryption
****************

To protect customers’ intellectual property, encryption is supported as a session option.
With this enabled, all the XIR and compiled models generated are encrypted using AES256 algorithm.
To enable encryption, you need to pass the encryption key in python as follows:

.. code-block:: python
 
    session = onnxruntime.InferenceSession(
        '[model_file].onnx',
        providers=["VitisAIExecutionProvider"],
        provider_options=[{
            "config_file":"/path/to/vaip_config.json",
            "encryptionKey": "89703f950ed9f738d956f6769d7e45a385d3c988ca753838b5afbc569ebf35b2"
    }])

Here is the cpp version:

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

*********************************
Model Operators Assignment Report
*********************************

Vitis AI EP generates a file named ``vitisai_ep_report.json`` that provides a report on model operator assignments across CPU and IPU. This file is automatically generated in the cache directory, which by default is ``C:\temp\{user}\vaip\.cache\<model_cache_key>`` if no explicit cache location is specified in the code. This report includes device statistics such as the total number of nodes, the number of nodes running on the CPU and DPU. It also presents a list of all operator types in the model, the operators running on the CPU, and those on the DPU. Additionally, the report includes node statistics, such as input to a node, the applied operation, and output from the node.

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
