
#######################
Getting Started Example
#######################

This example uses a fine-tuned version of the ResNet model (using the CIFAR10 dataset) to demonstrate the process of preparing, quantizing, and deploying a model using Ryzen AI.


The following are the steps and the required files to run the example. The files can be downloaded from `here <https://github.com/amd/ryzen-ai-documentation/tree/main/example/resnet50>`_.


.. list-table:: 
   :widths: 20 25 25
   :header-rows: 1

   * - Steps 
     - Files Used
     - Description
   * - Installation
     - ``requirements.txt``
     - Install the necessary package for this example.
   * - Preparation
     - ``prepare_model_data.py``,
       ``resnet_utils.py``
     - The script ``prepare_model_data.py`` prepares the model and the data for the rest of the tutorial.

       1. To prepare the model the script converts pre-trained PyTorch model to ONNX format.
       2. To prepare the necessary data the script downloads and extract CIFAR10 dataset. 

       Optionally, the script can be used to retrain the ResNet model from PyTorch hub using CIFAR10 dataset. However, this retrained model, resnet_trained_for_cifar10.pt is already provided in this tutorial to skip the retraining process
   * - Trained model
     - ``models/resnet_trained_for_cifar10.onnx``,
       ``models/resnet_trained_for_cifar10.pt``
     - The ResNet model trained using CIFAR10 is provided both in .pt format.
   * - Quantization 
     - ``resnet_quantize.py``
     - Convert the model to the IPU-deployable model by performing Post-Training Quantization flow using VitisAI ONNX Quantization.
   * - Deployment - Python
     - ``predict.py``
     -  Run the Quantized model using the ONNX Runtime code. We demonstrate running the model on both CPU and IPU. 
   * - Deployment - C++
     - ``cpp/resnet_cifar/.``
     -  This folder contains the source code ``resnet_cifar.cpp`` that demonstrates running inference using C++ APIs. We additionally provide the infrastructure (required libraries, CMake files and headerfiles) required by the example. 


|
|

Step 1: Install Packages
~~~~~~~~~~~~~~~~~~~~~~~~

* Ensure that the Ryzen AI Software Platform is correctly installed. For more details, see the :ref:`installation instructions <inst.rst>`.

* This example requires a couple of additional packages. Run the following command to install them:


.. code-block:: 

   python -m pip install -r requirements.txt

|
|

Step 2: Prepare the CIFAR10 dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this example, we utilize the a custom ResNet model finetuned using the CIFAR-10 dataset.

The ``prepare_model_data.py`` script downloads the CIFAR10 dataset in pickle format (for python) and binary format (for C++). This dataset will be used in the subsequent steps for quantization and inference. The script also exports the provided PyTorch model into ONNX format. The following snippet from the script shows how the ONNX model is exported: 

.. code-block:: 

    dummy_inputs = torch.randn(1, 3, 32, 32)
    input_names = ['input']
    output_names = ['output']
    dynamic_axes = {'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
    tmp_model_path = str(models_dir / "resnet_trained_for_cifar10.onnx")
    torch.onnx.export(
            model,
            dummy_inputs,
            tmp_model_path,
            export_params=True,
            opset_version=13,
            input_names=input_names,
            output_names=output_names,
            dynamic_axes=dynamic_axes,
        )

Note that the supported batch size on Ryzen AI is 1, and the opset version is 13. 

Run the following command to prepare the dataset:

.. code-block:: 

   python prepare_model_data.py 

* The downloaded CIFAR-10 dataset is saved in the current directory at the following location: ``data/*``.
* The ResNet model has been retrained on CIFAR10 and the PyTorch model ``resnet_trained_for_cifar10.pt`` is provided in ``models/``.

|
|

Step 3: Quantize the Model
~~~~~~~~~~~~~~~~~~~~~~~~~~

Quantizing AI models from floating-point to 8-bit integers reduces computational power and the memory footprint required for inference. For model quantization, you can either use Vitis AI quantizer or Microsoft Olive. This example utilizes the Vitis AI ONNX quantizer workflow. Quantization tool takes the pre-trained float32 model from the previous step (``resnet_trained_for_cifar10.onnx``) and produces a quantized model.

.. code-block::

   python resnet_quantize.py

This will generate quantized model using QDQ quant format and UInt8 activation type and Int8 weight type. After the run is complete, the quantized ONNX model ``resnet.qdq.U8S8.onnx`` is saved to models/resnet.qdq.U8S8.onnx. 

The ``resnet_quantize.py`` file has ``quantize_static`` function (line 95) that applies static quantization to the model. 

.. code-block::

   from onnxruntime.quantization import QuantFormat, QuantType
   import vai_q_onnx

   vai_q_onnx.quantize_static(
        input_model_path,
        output_model_path,
        dr,
        quant_format=QuantFormat.QDQ,
        calibrate_method=vai_q_onnx.PowerOfTwoMethod.MinMSE,
        activation_type=QuantType.QUInt8,
        weight_type=QuantType.QInt8,
        enable_dpu=True, 
        extra_options={'ActivationSymmetric': True} 
    )

The parameters of this function are:

* **input_model_path**: (String) The file path of the model to be quantized.
* **output_model_path**: (String) The file path where the quantized model will be saved.
* **dr**: (Object or None) Calibration data reader that enumerates the calibration data and producing inputs for the original model. In this example, CIFAR10 dataset is used for calibration during the quantization process.
* **quant_format**: (String) Specifies the quantization format of the model. In this example we have used the QDQ quant format.
* **calibrate_method**:(String) In this example this parameter is set to ``vai_q_onnx.PowerOfTwoMethod.MinMSE`` to apply power-of-2 scale quantization. 
* **activation_type**: (String) Data type of activation tensors after quantization. In this example, it's set to QUInt8 (Quantized Unsigned Int 8).
* **weight_type**: (String) Data type of weight tensors after quantization. In this example, it's set to QInt8 (Quantized Int 8).

|
|

Step 4: Deploy the Model  
~~~~~~~~~~~~~~~~~~~~~~~~

We demonstrate deploying the quantized model using both Python and C++ APIs. 

* :ref:`Deployment - Python <_dep-python>`
* :ref:`Deployment - C++ <_dep-cpp>`

.. _dep-python:

Deployment - Python
===========================

The ``predict.py`` script is used to deploy the model. It extracts the first ten images from the CIFAR-10 test dataset and converts them to the .png format. The script then reads all those ten images and classifies them by running the quantized ResNet-50 model on CPU or IPU. 

Deploy the Model on the CPU
----------------------------

By default, ``predict.py`` runs the model on CPU. 

.. code-block::
  
        > python predict.py

Typical output

.. code-block:: 

        Image 0: Actual Label cat, Predicted Label cat
        Image 1: Actual Label ship, Predicted Label ship
        Image 2: Actual Label ship, Predicted Label airplane
        Image 3: Actual Label airplane, Predicted Label airplane
        Image 4: Actual Label frog, Predicted Label frog
        Image 5: Actual Label frog, Predicted Label frog
        Image 6: Actual Label automobile, Predicted Label automobile
        Image 7: Actual Label frog, Predicted Label frog
        Image 8: Actual Label cat, Predicted Label cat
        Image 9: Actual Label automobile, Predicted Label automobile
        
                
Deploy the Model on the Ryzen AI IPU
------------------------------------

To successfully run the model on the IPU, run the following setup steps:

- Ensure that the ``XLNX_VART_FIRMWARE`` environment variable is correctly pointing to the XCLBIN file included in the ONNX Vitis AI Execution Provider package. For more information, see the :ref:`installation instructions <set-vart-envar>`.

- Copy the ``vaip_config.json`` runtime configuration file from the Vitis AI Execution Provider package to the current directory. For more information, see the :ref:`installation instructions <copy-vaip-config>`. The ``vaip_config.json`` is used by the ``predict.py`` script to configure the Vitis AI Execution Provider.


The following section of the ``predict.py`` script shows how ONNX Runtime is configured to deploy the model on the Ryzen AI IPU:


.. code-block::

  parser = argparse.ArgumentParser()
  parser.add_argument('--ep', type=str, default ='cpu',choices = ['cpu','ipu'], help='EP backend selection')
  opt = parser.parse_args()
  
  providers = ['CPUExecutionProvider']
  provider_options = [{}]

  if opt.ep == 'ipu':
     providers = ['VitisAIExecutionProvider']
     cache_dir = Path(__file__).parent.resolve()
     provider_options = [{
                'config_file': 'vaip_config.json',
                'cacheDir': str(cache_dir),
                'cacheKey': 'modelcachekey'
                }]

  session = ort.InferenceSession(model.SerializeToString(), providers=providers,
                                 provider_options=provider_options)


Run the ``predict.py`` with the ``--ep ipu`` switch to run the ResNet-50 model on the Ryzen AI IPU:


.. code-block::

    >python predict.py --ep ipu

Typical output

.. code-block:: 

  I20230803 19:29:01.962848 13180 vitisai_compile_model.cpp:274] Vitis AI EP Load ONNX Model Success
  I20230803 19:29:01.970893 13180 vitisai_compile_model.cpp:275] Graph Input Node Name/Shape (1)
  I20230803 19:29:01.970893 13180 vitisai_compile_model.cpp:279]   input : [-1x3x32x32]
  I20230803 19:29:01.970893 13180 vitisai_compile_model.cpp:285] Graph Output Node Name/Shape (1)
  I20230803 19:29:01.970893 13180 vitisai_compile_model.cpp:289]   output : [-1x10]
  I20230803 19:29:01.970893 13180 vitisai_compile_model.cpp:165] use cache key modelcachekey
  2023-08-03 19:29:02.0303033 [W:onnxruntime:, session_state.cc:1169 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
  2023-08-03 19:29:02.0363239 [W:onnxruntime:, session_state.cc:1171 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
  I20230803 19:29:02.108831 13180 custom_op.cpp:126]  Vitis AI EP running 348 Nodes
  !!! Warning: fingerprint of xclbin file C:\Windows\System32\AMD\1x4.xclbin doesn't match subgraph subgraph_/fc/fc.1/Relu_output_0(TransferMatMulToConv2d)

  Image 0: Actual Label cat, Predicted Label deer
  Image 1: Actual Label ship, Predicted Label ship
  Image 2: Actual Label ship, Predicted Label ship
  Image 3: Actual Label airplane, Predicted Label ship
  Image 4: Actual Label frog, Predicted Label deer
  Image 5: Actual Label frog, Predicted Label horse
  Image 6: Actual Label automobile, Predicted Label frog
  Image 7: Actual Label frog, Predicted Label deer
  Image 8: Actual Label cat, Predicted Label deer
  Image 9: Actual Label automobile, Predicted Label ship


.. _dep-cpp:

Deployment - C++
===========================

Prerequisites
-------------

1. Visual Studio 2019 Community edition, ensure "Desktop Development with C++" is installed
2. cmake (version >= 3.26)
3. opencv (version=4.6.0) required for the custom resnet example

Install OpenCV 
--------------

It is recommended to build OpenCV from the source code and use static build. The default installation localtion is "\install" , the following instruction installs OpenCV in the location "C:\\opencv" as an example. You may first change the directory to where you want to clone the OpenCV repository.

.. code-block:: bash

   git clone https://github.com/opencv/opencv.git -b 4.6.0
   cd opencv
   cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DBUILD_SHARED_LIBS=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON -DCMAKE_CONFIGURATION_TYPES=Release -A x64 -T host=x64 -G "Visual Studio 16 2019" "-DCMAKE_INSTALL_PREFIX=C:\opencv" "-DCMAKE_PREFIX_PATH=C:\opencv" -DCMAKE_BUILD_TYPE=Release -DBUILD_opencv_python2=OFF -DBUILD_opencv_python3=OFF -DBUILD_WITH_STATIC_CRT=OFF -B build
   cmake --build build --config Release
   cmake --install build --config Release

Build and Run Custom Resnet C++ sample
----------------------------------

The C++ source files, CMake list files and related artifacts are provided in the ``cpp/resnet_cifar/*`` folder. The source file ``cpp/resnet_cifar/resnet_cifar.cpp`` takes 10 images from the CIFAR10 test set, converts them to .png format, preprocesses them, and performs model inference. The example has onnxruntime dependencies, that are provided in ``cpp/resnet_cifar/onnxruntime/*``. 

Run the following command to build the resnet example. Assign ``-DOpenCV_DIR`` to the OpenCV installation directory.

.. code-block:: bash

   cd getting_started_resnet/cpp
   cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DBUILD_SHARED_LIBS=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON -DCMAKE_CONFIGURATION_TYPES=Release -A x64 -T host=x64 -DCMAKE_INSTALL_PREFIX=. -DCMAKE_PREFIX_PATH=. -B build -S resnet_cifar -DOpenCV_DIR="C:/opencv" -G "Visual Studio 16 2019"

This should generate the build directory with the ``resnet_cifar.sln`` solution file along with other project files. Open the solution file using Visual Studio 2019 and build to compile. You can also use "Developer Command Prompt for VS 2019" to open the solution file in Visual Studio.

.. code-block:: bash 

   devenv build/resnet_cifar.sln

After compilation, the executable should be generated in ``build/Release/resnet_cifar.exe``. We will copy this application over to the directory with the onnxruntime DLLs that were provided: 

.. code-block:: bash 

   xcopy build\Release\resnet_cifar.exe resnet_cifar\onnxruntime\bin\

Now to deploy our model, we will go back to the parent directory (getting_started_resnet) of this example:

.. code-block:: bash 

   cd ../

The C++ application that was generated takes 3 arguments: 

#. Path to the quantized ONNX model generated in Step 3 
#. The execution provider of choice (cpu or ipu) 
#. vaip_config.json (pass None if running on CPU) 


Deploy the Model on the CPU
****************************

To run the model on the CPU, use the following command: 

.. code-block:: bash 

   cpp\resnet_cifar\onnxruntime\bin\resnet_cifar.exe models\resnet.qdq.U8S8.onnx cpu None

Typical output: 

.. code-block:: bash 

   model name:models\resnet.qdq.U8S8.onnx
   ep:cpu
   Input Node Name/Shape (1):
           input : -1x3x32x32
   Output Node Name/Shape (1):
           output : -1x10
   Final results:
   Predicted label is cat and actual label is cat
   Predicted label is ship and actual label is ship
   Predicted label is ship and actual label is ship
   Predicted label is airplane and actual label is airplane
   Predicted label is frog and actual label is frog
   Predicted label is frog and actual label is frog
   Predicted label is truck and actual label is automobile
   Predicted label is frog and actual label is frog
   Predicted label is cat and actual label is cat
   Predicted label is automobile and actual label is automobile

Deploy the Model on the IPU
****************************

To successfully run the model on the IPU:

- Ensure that the ``XLNX_VART_FIRMWARE`` environment variable is correctly pointing to the XCLBIN file included in the ONNX Vitis AI Execution Provider package. If you installed Ryzen-AI software by automatic installer, the IPU binary path is already set, however if you did the installation manually, ensure the IPU binary path is set using the following command: 
.. code-block:: bash 

   set XLNX_VART_FIRMWARE=path\to\RyzenAI\installation\ryzen-ai-sw-1.0\ryzen-ai-sw-1.0\voe-4.0-win_amd64\1x4.xclbin


- Copy the ``vaip_config.json`` runtime configuration file from the Vitis AI Execution Provider package to the current directory. For more information, see the :ref:`installation instructions <copy-vaip-config>`. The ``vaip_config.json`` is used by the source file ``resnet_cifar.cpp`` to configure the Vitis AI Execution Provider.

The following code block from reset_cifar.cpp shows how ONNX Runtime is configured to deploy the model on the Ryzen AI IPU:

.. code-block:: bash 

    auto session_options = Ort::SessionOptions();

    auto config_key = std::string{ "config_file" };
 
    if(ep=="ipu")
    {
    auto options =
        std::unordered_map<std::string, std::string>{ {config_key, json_config} };
    session_options.AppendExecutionProvider("VitisAI", options);
    }

    auto session = Ort::Experimental::Session(env, model_name, session_options);

To run the model on the IPU, we will pass the ipu flag and the vaip_config.json file as arguments to the C++ application. Use the following command to run the model on the IPU: 

.. code-block:: bash 

   cpp\resnet_cifar\onnxruntime\bin\resnet_cifar.exe models\resnet.qdq.U8S8.onnx ipu vaip_config.json

Typical output: 

.. code-block:: bash 

   model name:models\resnet.qdq.U8S8.onnx
   ep:ipu
   WARNING: Logging before InitGoogleLogging() is written to STDERR
   I20231117 11:22:16.366518 105724 vitisai_compile_model.cpp:304] Vitis AI EP Load ONNX Model Success
   I20231117 11:22:16.366518 105724 vitisai_compile_model.cpp:305] Graph Input Node Name/Shape (1)
   I20231117 11:22:16.366518 105724 vitisai_compile_model.cpp:309]          input : [-1x3x32x32]
   I20231117 11:22:16.366518 105724 vitisai_compile_model.cpp:315] Graph Output Node Name/Shape (1)
   I20231117 11:22:16.366518 105724 vitisai_compile_model.cpp:319]          output : [-1x10]
   I20231117 11:22:17.189302 105724 pass_imp.cpp:366] save const info to "C:\\temp\\savsrini\\vaip\\.cache\\c13917fcfb7de23b99be18a8d7588e62\\const_info_before_const_folding.txt"
   I20231117 11:22:17.317427 105724 pass_imp.cpp:275] save fix info to "C:\\temp\\savsrini\\vaip\\.cache\\c13917fcfb7de23b99be18a8d7588e62\\fix_info.txt"
   I20231117 11:22:17.317427 105724 pass_imp.cpp:366] save const info to "C:\\temp\\savsrini\\vaip\\.cache\\c13917fcfb7de23b99be18a8d7588e62\\const_info_after_const_folding.txt"
   I20231117 11:22:17.317427 105724 pass_imp.cpp:393] save const info to "C:\\temp\\savsrini\\vaip\\.cache\\c13917fcfb7de23b99be18a8d7588e62\\const.bin"
   I20231117 11:22:24.488317 105724 compile_pass_manager.cpp:352] Compile mode: aie
   I20231117 11:22:24.488317 105724 compile_pass_manager.cpp:353] Debug mode: performance
   I20231117 11:22:24.488317 105724 compile_pass_manager.cpp:357] Target architecture: AMD_AIE2_Nx4_Overlay
   I20231117 11:22:24.513685 105724 compile_pass_manager.cpp:523] Graph name: main_graph, with op num: 439
   I20231117 11:22:24.513685 105724 compile_pass_manager.cpp:536] Begin to compile...
   W20231117 11:22:30.609391 105724 RedundantOpReductionPass.cpp:663] xir::Op{name = /avgpool/GlobalAveragePool_output_0_DequantizeLinear_Output_vaip_315, type = pool-fix}'s input and output is unchanged, so it will be removed.
   I20231117 11:22:30.848696 105724 PartitionPass.cpp:5648] xir::Op{name = output_, type = fix2float} is not supported by current target. Target name: AMD_AIE2_Nx4_Overlay, target type: IPU_PHX. Assign it to CPU.
   I20231117 11:22:32.471781 105724 compile_pass_manager.cpp:548] Total device subgraph number 3, CPU subgraph number 1
   I20231117 11:22:32.471781 105724 compile_pass_manager.cpp:557] Total device subgraph number 3, DPU subgraph number 1
   I20231117 11:22:32.471781 105724 compile_pass_manager.cpp:613] Compile done.
   I20231117 11:22:32.563076 105724 anchor_point.cpp:428] before optimization:
   
   input_DequantizeLinear_Output <-- identity@ --
   input_QuantizeLinear_Output <-- identity@fuse_DPU --
   input_QuantizeLinear_Output
   after optimization:
   
   input_QuantizeLinear_Output_vaip_426 <-- identity@combine_empty --
   input_QuantizeLinear_Output
   I20231117 11:22:32.563076 105724 anchor_point.cpp:428] before optimization:
   
   output <-- identity@ --
   output_QuantizeLinear_Output <-- identity@fuse_DPU --
   output_QuantizeLinear_Output
   after optimization:
   
   output_QuantizeLinear_Output_vaip_427 <-- identity@combine_empty --
   output_QuantizeLinear_Output
   2023-11-17 11:22:32.7183935 [W:onnxruntime:, session_state.cc:1169 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
   2023-11-17 11:22:32.7282487 [W:onnxruntime:, session_state.cc:1171 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
   I20231117 11:22:32.799844 105724 custom_op.cpp:133]  Vitis AI EP running 400 Nodes
   Input Node Name/Shape (1):
           input : -1x3x32x32
   Output Node Name/Shape (1):
           output : -1x10
   Final results:
   Predicted label is cat and actual label is cat
   Predicted label is ship and actual label is ship
   Predicted label is ship and actual label is ship
   Predicted label is ship and actual label is airplane
   Predicted label is frog and actual label is frog
   Predicted label is frog and actual label is frog
   Predicted label is truck and actual label is automobile
   Predicted label is frog and actual label is frog
   Predicted label is cat and actual label is cat
   Predicted label is automobile and actual label is automobile
..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
