#######################
Getting Started Example
#######################

This example uses the ResNet-50 model from PyTorch Hub to demonstrate the process of preparing, quantizing, and deploying a model using Ryzen AI.


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
     - The script prepare_model_data.py downloads and extracts the CIFAR10 dataset. The script has an optional flag to re-train a pretrained ResNet50 model using CIFAR10 dataset via transfer learning. The trained ResNet50 model (in .pt and .onnx formats) are provided. 
   * - Trained model
     - ``models/resnet_trained_for_cifar10.onnx``,
       ``models/resnet_trained_for_cifar10.pt``
     - The ResNet50 model trained using CIFAR10 is provided both in .pt and .onnx formats.
   * - Quantization 
     - ``resnet_quantize.py``
     - Convert the model to the IPU-deployable model by performing Post-Training Quantization flow using VitisAI ONNX Quantization.
   * - Deployment - Python
     - ``predict.py``
     -  Run the Quantized model using the ONNX Runtime code. We demonstrate running the model on both CPU and IPU. 
   * - Deployment - C++
     - ``cpp/resnet50/.``
     -  This folder contains the script ``resnet50_cifar.cpp`` that demonstrates running inference using C++ APIs. We additionally provide the infrastructure (required libraries, CMake files and headerfiles) required by the example. 


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

Step 2: Prepare the CIFAR10 dataset for training (optional), quantization and inference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this example, the ResNet-50 model from PyTorch Hub is utilized and trained using the CIFAR-10 dataset.

The ``prepare_model_data.py`` script downloads the CIFAR10 dataset in pickle format (for python) and binary format (for C++). The dataset is used for training (optional), quantization and inference. The script has an optional flag to perform the retraining process on CIFAR10. The training process runs over 500 images for each epoch up to five epochs. The training process takes approximately 30 minutes to complete. 

Run the following command to prepare the dataset:

.. code-block:: 

   python prepare_model_data.py 

* The downloaded CIFAR-10 dataset is saved in the current directory at the following location: ``data/*``.
* The ResNet50 model has been retrained on CIFAR10 and the model artifacts ``resnet_trained_for_cifar10.pt`` and ``resnet_trained_for_cifar10.onnx`` are provided in ``models/``. To generate these files by yourself, follow the instructions in the next step.


[Optional] To retrain the model on CIFAR10, run the following command:

.. code-block:: 

   python prepare_model_data.py --train --num_epochs 5

 
A typical output from the training process looks as follows:

.. code-block::

   Downloading: "https://download.pytorch.org/models/resnet50-11ad3fa6.pth" to C:\Users\JohnDoe/.cache\torch\hub\checkpoints\resnet50-11ad3fa6.pth
   100%|██████████████████████████████████████████████████████████████████████████████| 97.8M/97.8M [02:07<00:00, 805kB/s]
   Epoch [1/5], Step [100/500] Loss: 1.1550
   Epoch [1/5], Step [200/500] Loss: 1.0453
   Epoch [1/5], Step [300/500] Loss: 0.6397
   Epoch [1/5], Step [400/500] Loss: 0.6130
   Epoch [1/5], Step [500/500] Loss: 0.6792
   Epoch [2/5], Step [100/500] Loss: 0.5454
   Epoch [2/5], Step [200/500] Loss: 0.5218
   Epoch [2/5], Step [300/500] Loss: 0.7235
   Epoch [2/5], Step [400/500] Loss: 0.5740
   Epoch [2/5], Step [500/500] Loss: 0.9055
   Epoch [3/5], Step [100/500] Loss: 0.5954
   Epoch [3/5], Step [200/500] Loss: 0.4662
   Epoch [3/5], Step [300/500] Loss: 0.3351
   Epoch [3/5], Step [400/500] Loss: 0.4871
   Epoch [3/5], Step [500/500] Loss: 0.4340
   Epoch [4/5], Step [100/500] Loss: 0.4139
   Epoch [4/5], Step [200/500] Loss: 0.4724
   Epoch [4/5], Step [300/500] Loss: 0.4847
   Epoch [4/5], Step [400/500] Loss: 0.4778
   Epoch [4/5], Step [500/500] Loss: 0.3955
   Epoch [5/5], Step [100/500] Loss: 0.5511
   Epoch [5/5], Step [200/500] Loss: 0.4557
   Epoch [5/5], Step [300/500] Loss: 0.6158
   Epoch [5/5], Step [400/500] Loss: 0.3884
   Epoch [5/5], Step [500/500] Loss: 0.4330
   Accuracy of the model on the test images: 75.27 %


After completing the training process, observe the following output:
 
* The trained ResNet-50 model on the CIFAR-10 dataset is saved at the following location: ``models\resnet_trained_for_cifar10.pt``.
* The trained ResNet-50 model on the CIFAR-10 dataset is saved at the following location in ONNX format: ``models\resnet_trained_for_cifar10.onnx``.

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

1. Visual Studio 2019 or 2022 (Recommended for Visual Studio 2019)
2. cmake (version >= 3.26)
3. opencv (version=4.6.0) required for the resnet50 example

Install OpenCV 
--------------

It is recommended to build OpenCV from the source code and use static build. The default installation localtion is "\install" , the following instruction installs OpenCV in the location "D:\\opencv" as an example. You may first change the directory to where you want to clone the OpenCV repository.

.. code-block:: bash

   git clone https://github.com/opencv/opencv.git -b 4.6.0
   cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DBUILD_SHARED_LIBS=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON -DCMAKE_CONFIGURATION_TYPES=Release -A x64 -T host=x64 -G 'Visual Studio 16 2019' '-DCMAKE_INSTALL_PREFIX=D:\\opencv' '-DCMAKE_PREFIX_PATH=D:\\opencv' -DCMAKE_BUILD_TYPE=Release -DBUILD_opencv_python2=OFF -DBUILD_opencv_python3=OFF -DBUILD_WITH_STATIC_CRT=OFF -B build -S opencv
   cmake --build build --config Release
   cmake --install build --config Release

Build and Run Resnet50 C++ sample
----------------------------------

The C++ source files, CMake list files and related artifacts are provided in the ``cpp/resnet50/*`` folder. The source file ``cpp/resnet50/resnet50_cifar.cpp`` takes 10 images from the CIFAR10 test set, converts them to .png format, preprocesses them, and performs model inference. The example has onnxruntime dependencies, that are provided in ``cpp/resnet50/onnxruntime/*``. 

Run the following command to build the resnet50 example. Assign ``-DOpenCV_DIR`` to the OpenCV installation directory.

.. code-block:: bash

   cd getting_started_resnet/cpp
   cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DBUILD_SHARED_LIBS=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON -DCMAKE_CONFIGURATION_TYPES=Release -A x64 -T host=x64 -DCMAKE_INSTALL_PREFIX=. -DCMAKE_PREFIX_PATH=. -B build -S resnet50 -DOpenCV_DIR="C:/opencv" -G "Visual Studio 16 2019"

This should generate the build directory with the ``resnet50_cifar.sln`` solution file along with other project files. Open the solution file using Visual Studio 2019 and build to compile. You can also use the command line to open the solution file in Visual Studio. 

.. code-block:: bash 

   devenv build/resnet50_cifar.sln

After compilation, the executable should be generated in ``build/Release/resnet50_cifar.exe``. We will copy this application over to the directory with the onnxruntime DLLs that were provided: 

.. code-block:: bash 

   copy build/Release/resnet50_cifar.exe resnet50/onnxruntime/bin/.

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

   cpp\resnet50\onnxruntime\bin\resnet50_cifar.exe models\resnet.qdq.U8S8.onnx cpu None

Typical output: 

.. code-block:: bash 

      model name:models\resnet.qdq.U8S8.onnx
   ep:cpuInput Node Name/Shape (1):
           input : -1x3x32x32
   Output Node Name/Shape (1):
           output : -1x10
   curr file: ./images/cifar_image_0.png
   
   input_tensor shape: 1x3x32x32
   Running model...done
   output_tensor_shape: 1x10
   score[3]    =  0.979557     text: cat
   score[6]    =  0.0123308    text: frog
   score[5]    =  0.0066002    text: dog
   score[2]    =  0.00089324   text: bird
   score[4]    =  0.000421937  text: deer
   curr file: ./images/cifar_image_1.png
   
   .
   .
   .
   .
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

- Ensure that the ``XLNX_VART_FIRMWARE`` environment variable is correctly pointing to the XCLBIN file included in the ONNX Vitis AI Execution Provider package. For more information, see the :ref:`installation instructions <set-vart-envar>`.

- Copy the ``vaip_config.json`` runtime configuration file from the Vitis AI Execution Provider package to the current directory. For more information, see the :ref:`installation instructions <copy-vaip-config>`. The ``vaip_config.json`` is used by the ``predict.py`` script to configure the Vitis AI Execution Provider.

To run the model on the IPU, we will pass the ipu flag and the vaip_config.json file as arguments to the C++ application. Use the following command to run the model on the IPU: 

.. code-block:: bash 

   cpp\resnet50\onnxruntime\bin\resnet50_cifar.exe models\resnet.qdq.U8S8.onnx ipu vaip_config.json

Typical output: 

   model name:models\resnet.qdq.U8S8.onnx
   ep:ipuWARNING: Logging before InitGoogleLogging() is written to STDERR
   I20231116 14:49:23.608762 92092 vitisai_compile_model.cpp:304] Vitis AI EP Load ONNX Model Success
   I20231116 14:49:23.608762 92092 vitisai_compile_model.cpp:305] Graph Input Node Name/Shape (1)
   I20231116 14:49:23.608762 92092 vitisai_compile_model.cpp:309]   input : [-1x3x32x32]
   I20231116 14:49:23.608762 92092 vitisai_compile_model.cpp:315] Graph Output Node Name/Shape (1)
   I20231116 14:49:23.608762 92092 vitisai_compile_model.cpp:319]   output : [-1x10]
   I20231116 14:49:24.227304 92092 pass_imp.cpp:366] save const info to "C:\\temp\\savsrini\\vaip\\.cache\\c13917fcfb7de23b99be18a8d7588e62\\const_info_before_const_folding.txt"
   I20231116 14:49:24.337621 92092 pass_imp.cpp:275] save fix info to "C:\\temp\\savsrini\\vaip\\.cache\\c13917fcfb7de23b99be18a8d7588e62\\fix_info.txt"
   I20231116 14:49:24.337621 92092 pass_imp.cpp:366] save const info to "C:\\temp\\savsrini\\vaip\\.cache\\c13917fcfb7de23b99be18a8d7588e62\\const_info_after_const_folding.txt"
   I20231116 14:49:24.337621 92092 pass_imp.cpp:393] save const info to "C:\\temp\\savsrini\\vaip\\.cache\\c13917fcfb7de23b99be18a8d7588e62\\const.bin"
   I20231116 14:49:29.816938 92092 compile_pass_manager.cpp:352] Compile mode: aie
   I20231116 14:49:29.816938 92092 compile_pass_manager.cpp:353] Debug mode: performance
   I20231116 14:49:29.816938 92092 compile_pass_manager.cpp:357] Target architecture: AMD_AIE2_Nx4_Overlay
   I20231116 14:49:29.816938 92092 compile_pass_manager.cpp:523] Graph name: main_graph, with op num: 439
   I20231116 14:49:29.816938 92092 compile_pass_manager.cpp:536] Begin to compile...
   W20231116 14:49:33.973276 92092 RedundantOpReductionPass.cpp:663] xir::Op{name = /avgpool/GlobalAveragePool_output_0_DequantizeLinear_Output_vaip_315, type = pool-fix}'s input and output is unchanged, so it will be removed.
   I20231116 14:49:34.134106 92092 PartitionPass.cpp:5648] xir::Op{name = output_, type = fix2float} is not supported by current target. Target name: AMD_AIE2_Nx4_Overlay, target type: IPU_PHX. Assign it to CPU.
   I20231116 14:49:35.301882 92092 compile_pass_manager.cpp:548] Total device subgraph number 3, CPU subgraph number 1
   I20231116 14:49:35.301882 92092 compile_pass_manager.cpp:557] Total device subgraph number 3, DPU subgraph number 1
   I20231116 14:49:35.301882 92092 compile_pass_manager.cpp:613] Compile done.
   I20231116 14:49:35.367611 92092 anchor_point.cpp:428] before optimization:
   
   input_DequantizeLinear_Output <-- identity@ --
   input_QuantizeLinear_Output <-- identity@fuse_DPU --
   input_QuantizeLinear_Output
   after optimization:
   
   input_QuantizeLinear_Output_vaip_426 <-- identity@combine_empty --
   input_QuantizeLinear_Output
   I20231116 14:49:35.367611 92092 anchor_point.cpp:428] before optimization:
   
   output <-- identity@ --
   output_QuantizeLinear_Output <-- identity@fuse_DPU --
   output_QuantizeLinear_Output
   after optimization:
   
   output_QuantizeLinear_Output_vaip_427 <-- identity@combine_empty --
   output_QuantizeLinear_Output
   2023-11-16 14:49:35.4696161 [W:onnxruntime:, session_state.cc:1169 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
   2023-11-16 14:49:35.4751682 [W:onnxruntime:, session_state.cc:1171 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
   I20231116 14:49:35.523561 92092 custom_op.cpp:133]  Vitis AI EP running 400 Nodes
   Input Node Name/Shape (1):
           input : -1x3x32x32
   Output Node Name/Shape (1):
           output : -1x10
   curr file: ./images/cifar_image_0.png
   
   input_tensor shape: 1x3x32x32
   Running model...done
   output_tensor_shape: 1x10
   score[3]    =  0.982167     text: cat
   score[6]    =  0.0109109    text: frog
   score[5]    =  0.00584018   text: dog
   score[2]    =  0.00069751   text: bird
   score[4]    =  0.0002566    text: deer
   curr file: ./images/cifar_image_1.png
   .
   .
   .
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
