################################
Model Deployment with Windows ML
################################

Windows Machine Learning (WinML) enables C#, C++, and Python developers to run ONNX AI models locally on Windows PCs through ONNX Runtime, with automatic execution provider management across hardware targets including CPUs, GPUs, and NPUs. You can use models from PyTorch, TensorFlow/Keras, TensorFlow Lite (TFLite), scikit-learn, and other frameworks by converting them to ONNX for ONNX Runtime.

In short, Windows ML provides a shared, Windows-wide ONNX Runtime along with support for dynamically downloading execution providers (EPs).

For more details, see the `Windows ML official documentation <https://learn.microsoft.com/en-us/windows/ai/new-windows-ml/overview>`_.

************************************************
Automatic Execution Providers (EPs) Registration
************************************************

Windows ML will automatically discover, download, and register the latest version of all compatible execution providers.

C++ Example
~~~~~~~~~~~

.. code-block:: cpp

    #include <winrt/Microsoft.Windows.AI.MachineLearning.h>
    #include <win_onnxruntime_cxx_api.h>

    // First we need to create an ORT environment
    Ort::Env env(ORT_LOGGING_LEVEL_ERROR, "WinMLDemo"); // Use an ID of your own choice

    // Get the default ExecutionProviderCatalog
    winrt::Microsoft::Windows::AI::MachineLearning::ExecutionProviderCatalog catalog =
    winrt::Microsoft::Windows::AI::MachineLearning::ExecutionProviderCatalog::GetDefault();

    // Ensure and register all compatible execution providers with ONNX Runtime
    catalog.EnsureAndRegisterAllAsync().get();

Python Example
~~~~~~~~~~~~~~

.. code-block:: python

    # Known issue: import winrt.runtime will cause the TensorRTRTX execution provider to fail registration.
    # As a workaround, please run pywinrt related code in a separate thread.

    # winml.py
    import json

    def _get_ep_paths() -> dict[str, str]:
        from winui3.microsoft.windows.applicationmodel.dynamicdependency.bootstrap import (
            InitializeOptions,
            initialize
        )

        import winui3.microsoft.windows.ai.machinelearning as winml
        eps     = {}
        with initialize(options = InitializeOptions.ON_NO_MATCH_SHOW_UI):
            catalog = winml.ExecutionProviderCatalog.get_default()
            providers = catalog.find_all_providers()
            for provider in providers:
                provider.ensure_ready_async().get()
                eps[provider.name] = provider.library_path
                # DO NOT call provider.try_register in python. That will register to the native env.
        return eps

    if __name__ == "__main__":
        eps = _get_ep_paths()
        print(json.dumps(eps))

    # In your application code
    import subprocess
    import json
    import sys
    from pathlib import Path
    import onnxruntime as ort

    def register_execution_providers():
        worker_script = str(Path(__file__).parent / 'winml.py')
        result = subprocess.check_output([sys.executable, worker_script], text=True)
        paths = json.loads(result)
        for item in paths.items():
            ort.register_execution_provider_library(item[0], item[1])
        _ep_registered = True

    register_execution_providers()


The ``register_execution_providers`` function is used to download and register the latest version of all compatible execution providers.

****************
Execution Policy
****************

The EP selection policy can be configured to use specific execution provider or through general execution policy. For more details, refer to the Windows ML documentation on `Execution Providers <https://learn.microsoft.com/en-us/windows/ai/new-windows-ml/execution-providers>`_.

For example, setting the execution policy to `PREFER_NPU` will prioritize the NPU execution provider if available, with a fallback to CPU execution if an NPU is not present. 

C++ Example
~~~~~~~~~~~

.. code-block:: cpp

    // Configure the session to select an EP and device for MAX_EFFICIENCY which typically
    // will choose an NPU if available with a CPU fallback.
    Ort::SessionOptions sessionOptions;
    sessionOptions.SetEpSelectionPolicy(OrtExecutionProviderDevicePolicy_PREFER_NPU);

Python Example
~~~~~~~~~~~~~~

.. code-block:: python

    # Configure the session to select an EP and device for PREFER_NPU which typically
    # will choose an NPU if available with a CPU fallback.
    options = ort.SessionOptions()
    options.set_provider_selection_policy(ort.OrtExecutionProviderDevicePolicy.PREFER_NPU)
    assert options.has_providers()


Specifying the specific VitisAI EP can be done through the `set_providers` API. For example, setting the execution provider to `VitisAIExecutionProvider` will only use the VitisAI EP for model execution.

C++ Example
~~~~~~~~~~~

.. code-block:: cpp

    #include <iostream>
    #include <iomanip>
    #include <vector>
    #include <stdexcept>
    #include <winml/onnxruntime_cxx_api.h>

    // Assuming you have an Ort::Env named 'env'
    // 1. Enumerate EP devices
    std::vector<Ort::ConstEpDevice> ep_devices = env.GetEpDevices();

    // 2. Collect only ReplaceWithExecutionProvider NPU devices
    std::vector<Ort::ConstEpDevice> selected_ep_devices;
    for (const auto& d : ep_devices) {
        if (std::string(d.EpName()) == "VitisAIExecutionProvider"
            && d.HardwareDevice().Type() == OrtHardwareDeviceType_NPU) {
            selected_ep_devices.push_back(d);
        }
    }
    if (selected_ep_devices.empty()) {
        throw std::runtime_error("VitisAIExecutionProvider is not available on this system.");
    }

    // 3. Configure provider-specific options (varies based on EP)
    // and append the EP with the correct devices (varies based on EP)
    Ort::SessionOptions session_options;
    Ort::KeyValuePairs ep_options;
    ep_options.Add("provider_specific_option", "4");
    session_options.AppendExecutionProvider_V2(env, { selected_ep_devices.front() }, ep_options);


Python Example
~~~~~~~~~~~~~~

.. code-block:: python

    # 1. Enumerate and filter EP devices
    ep_devices = ort.get_ep_devices()
    selected_ep_devices = [
        d for d in ep_devices
        if d.ep_name == "VitisAIExecutionProvider"
        and d.device.type == ort.OrtHardwareDeviceType.NPU
    ]
    if not selected_ep_devices:
        raise RuntimeError("VitisAIExecutionProvider is not available on this system.")

    # 2. Configure provider-specific options (varies based on EP)
    # and append the EP with the correct devices (varies based on EP)
    options = ort.SessionOptions()
    provider_options = {"provider_specific_option": "4"}
    options.add_provider_for_devices([selected_ep_devices[0]], provider_options)




*****************
Model Compilation
*****************

Models may need to be compiled for specific EPs. This is a one-time process that stores the compiled model for subsequent runs:

C++ Example
~~~~~~~~~~~

.. code-block:: cpp

    bool isCompiledModelAvailable = std::filesystem::exists(compiledModelPath);

    if (!isCompiledModelAvailable)
    {
        Ort::ModelCompilationOptions compile_options(env, sessionOptions);
        compile_options.SetInputModelPath(modelPath.c_str());
        compile_options.SetOutputModelPath(compiledModelPath.c_str());

        std::cout << "Starting compile, this may take a few moments..." << std::endl;
        Ort::Status compileStatus = Ort::CompileModel(env, compile_options);
        if (compileStatus.IsOK())
        {
            std::cout << "Model compiled successfully!" << std::endl;
            isCompiledModelAvailable = true;
        }
    }


Python Example
~~~~~~~~~~~~~~

.. code-block:: python

    input_model_path = "path_to_your_model.onnx"
    output_model_path = "path_to_your_compiled_model.onnx"

    model_compiler = ort.ModelCompiler(
        options,
        input_model_path,
        embed_compiled_data_into_model=True,
        external_initializers_file_path=None,
    )
    model_compiler.compile_to_file(output_model_path)
    if not os.path.exists(output_model_path):
        # For some EPs, there might not be a compilation output.
        # In that case, use the original model directly.
        output_model_path = input_model_path



For more details on VitisAIExecution Provider specific `provider_options` as shown in the reference documentation :doc:`Model compilation and deployment <../modelrun>`


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
