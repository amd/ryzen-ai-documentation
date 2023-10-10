########################
Getting Started Tutorial
########################

This example uses the ResNet-50 model from PyTorch Hub to demonstrate the process of preparing, quantizing, and deploying a model using Ryzen AI.

The following are the steps and the required files to run the example. 

- The source code files can be downloaded from `this link <https://github.com/amd/RyzenAI-SW/tree/main/tutorial/getting_started_resnet>`_.

|
|

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
     - Train to prepare a model for the example. The training process adopts the transfer learning technique to train a pre-trained ResNet-50 model with the CIFAR-10 dataset. 
   * - Quantization 
     - ``resnet_quantize.py``
     - Convert the model to the IPU-deployable model by performing Post-Training Quantization flow using VitisAI ONNX Quantization.
   * - Deployment
     - ``predict.py``
     -  Run the Quantized model using the ONNX Runtime code. We demonstrate running the model on both CPU and IPU. 


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

Step 2: Prepare the Model and the Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this example, the ResNet-50 model from PyTorch Hub is utilized and trained using the CIFAR-10 dataset.

The ``prepare_model_data.py`` script downloads the ResNet-50 model from the PyTorch Hub. The script also downloads the CIFAR10 dataset and uses it to retrain the model using the transfer learning technique. The training process runs over 500 images for each epoch up to five epochs. The training process takes approximately 30 minutes to complete. At the end of the training, the trained model is used for the subsequent steps.

Run the following command to start the training:
 
.. code-block:: 

   python prepare_model_data.py --num_epochs 5

 
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
* The downloaded CIFAR-10 dataset is saved in the current directory at the following location: ``data\cifar-10-batches-py\*``.

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
        activation_type=QuantType.QInt8,
        weight_type=QuantType.QInt8,
        enable_dpu=True, 
        extra_options={'ActivationSymmetric': True} 
    )

The parameters of this function are:

* **input_model_path**: (String) The file path of the model to be quantized.
* **output_model_path**: (String) The file path where the quantized model will be saved.
* **dr**: (Object or None) Calibration data reader that enumerates the calibration data and producing inputs for the original model. In this example, CIFAR10 dataset is used for calibration during the quantization process.
* **quant_format**: (String) Specifies the quantization format of the model. In this example we have used the QDQ quant format.
* **calibrate_method**: (String) In this example this parameter is set to ``vai_q_onnx.PowerOfTwoMethod.MinMSE`` to apply power-of-2 scale quantization. 
* **activation_type**: (String) Data type of activation tensors after quantization. In this example, it's set to QInt8 (Quantized Integer 8).
* **weight_type**: (String) Data type of weight tensors after quantization. In this example, it's set to QInt8 (Quantized Integer 8).
* **enable_dpu**: (Boolean) Determines whether to generate a quantized model that is suitable for the DPU. If set to True, the quantization process will create a model that is optimized for DPU computations.
* **extra_options**: (Dict or None) Dictionary of additional options that can be passed to the quantization process. In this example, ``ActivationSymmetric`` is set to True i.e., calibration data for activations is symmetrized. 

|
|

Step 4: Deploy the Model  
~~~~~~~~~~~~~~~~~~~~~~~~

The ``predict.py`` script is used to deploy the model. It extracts the first ten images from the CIFAR-10 test dataset and converts them to the .png format. The script then reads all those ten images and classifies them by running the quantized ResNet-50 model on CPU or IPU. 

Deploy the Model on the CPU
===========================

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
====================================

To successfully run the model on the IPU, run the following setup steps:

- Ensure that the ``XLNX_VART_FIRMWARE`` environment variable is correctly pointing to the XCLBIN file included in the ONNX Vitis AI Execution Provider package. For more information, see the :ref:`installation instructions <set-vart-envar>`.

.. code-block::

   set XLNX_VART_FIRMWARE=C:\path\to\1x4.xclbin

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

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
