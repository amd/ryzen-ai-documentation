###########################
RyzenAI-SW using Windows ML
###########################

Windows Machine Learning (WinML) enables developers to run ONNX AI models on PC via ONNX runtime, with automatic execution provider management for different hardwares i.e. CPUs, GPUs and NPUs.

For more details, refer to the `Windows ML official documentation <https://learn.microsoft.com/en-us/windows/ai/new-windows-ml/overview>`

*************
Prerequisites
*************

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Dependencies
     - Version Requirement
   * - Windows 11
     - version 24H2 (build 26100) or greater
   * - C++
     - C++20 or later
   * - Python
     - 3.10 to 3.12

Installation
~~~~~~~~~~~~

Install the `Windows App SDK <https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/downloads>`
TODO: Provide link to the download and install the SDK

Make sure you install the `1.8.0-Experimental4 version <>`, because the release versions don't contain Windows ML yet.

Features
~~~~~~~~

Windows ML handles the complexity of package management and hardware selection, automatically downloading the latest execution providers compatible with your device's hardware.

1. Dynamically get latest EPs for different hardware
2. Shared ONNX runtime, which reduces the application size
3. Broad Hardware Support across different vendors through ONNX runtime


Download and register the Execution Providers (EPs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Windows ML will automatically discover, download, and register the latest version of all compatible execution providers

C++
~~~

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


Python
~~~~~~

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


The ``register_execution_providers`` function is used to download and register the latest version of all compatible execution providers


*************************
Getting Started Tutorials
*************************

- :doc:`Getting Started Tutorial for Windows ML <model_deployment>` - Uses a custom ResNet model to demonstrate:

  - Model Conversion to QDQ quantized ONNX model using `AI Toolkit <https://code.visualstudio.com/docs/intelligentapps/modelconversion>`
  - `Deployment using Windows ML APIs and ONNX Runtime in C++ <model_deployment>`
  - `Deployment using Windows ML APIs and ONNX Runtime in Python <model_deployment>`


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.

