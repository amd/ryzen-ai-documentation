
INT8 Quantization with AMD Quark
================================

:doc:`Model Quantization <model_quantization>` section gives an overview of Ryzen AI quantization using the AMD Quark tool.

This section demonstrates how to perform INT8 quantization using AMD Quark 0.13 (see :ref:`install-quark`), and using the quantized INT8 model in AMD Ryzen™ AI.

For BF16 quantization, Quark does not need to be invoked explicitly. The Vitis AI compiler automatically handles the FP32 to BF16 quantization process.

Basic Example: Quantizing ResNet50
----------------------------------

The following steps outline the process for quantizing a ResNet50 ONNX model.

	**1. Download the ONNX Model**

		On your host machine, download the ResNet50 ONNX float model from the `onnxmodelzoo <https://huggingface.co/onnxmodelzoo>`__ model zoo:

		.. code-block::

			cd <Working Path>
			wget -P models https://huggingface.co/onnxmodelzoo/resnet50-v1-12/resolve/main/resnet50-v1-12.onnx
			

	**2. Prepare Calibration Data & Validation Data**

	Create a folder for calibration data and download sample images (PNG or JPG). For example, use images from `microsoft/onnxruntime-inference-examples <https://github.com/microsoft/onnxruntime-inference-examples/tree/main/quantization/image_classification/cpu/test_images>`__ as a quick start.

	.. code-block::

		mkdir calib_data
		wget -O calib_data/daisy.jpg https://github.com/microsoft/onnxruntime-inference-examples/blob/main/quantization/image_classification/cpu/test_images/daisy.jpg?raw=true

	And prepare some pictures for validation:

	.. code-block::

		mkdir val_data
		wget -O val_data/daisy.jpg https://github.com/microsoft/onnxruntime-inference-examples/blob/main/quantization/image_classification/cpu/test_images/daisy.jpg?raw=true
		wget -O val_data/rose.jpg https://github.com/microsoft/onnxruntime-inference-examples/blob/main/quantization/image_classification/cpu/test_images/rose.jpg?raw=true
		wget -O val_data/tulip.jpg https://github.com/microsoft/onnxruntime-inference-examples/blob/main/quantization/image_classification/cpu/test_images/tulip.jpg?raw=true


	**3. Create the Quantization Script**

	Create a file *quantize.py* with the following contents:

	.. code-block::

		import os
		import cv2
		import numpy as np
		import onnx
		from torchvision import transforms
		from onnxruntime.quantization import CalibrationDataReader

		def get_model_input_name(input_model_path: str) -> str:
			model = onnx.load(input_model_path)
			model_input_name = model.graph.input[0].name
			return model_input_name

		class ImageDataReader(CalibrationDataReader):

			def __init__(self, calibration_image_folder: str, input_name: str):
				self.enum_data = None

				self.input_name = input_name

				self.data_list = self._preprocess_images(
						calibration_image_folder)

			def _preprocess_images(self, image_folder: str):
				data_list = []
				img_names = [f for f in os.listdir(image_folder) if f.endswith('.png') or f.endswith('.jpg')]
				for name in img_names:
					input_image = cv2.imread(os.path.join(image_folder, name))
					# Resize the input image. Because the size of Resnet50 is 224.
					input_image = cv2.resize(input_image, (224, 224))
					input_data = np.array(input_image).astype(np.float32)
					# Custom Pre-Process
					input_data = input_data.transpose(2, 0, 1)
					input_size = input_data.shape
					if input_size[1] > input_size[2]:
						input_data = input_data.transpose(0, 2, 1)
					input_data = np.expand_dims(input_data, axis=0)
					input_data = input_data / 255.0
					data_list.append(input_data)

				return data_list

			def get_next(self):
				if self.enum_data is None:
					self.enum_data = iter([{self.input_name: data} for data in self.data_list])
				return next(self.enum_data, None)

			def rewind(self):
				self.enum_data = None

		from quark.onnx.quantization.config import Config, get_default_config
		from quark.onnx import ModelQuantizer
		from onnxruntime.quantization import QuantType

		quant_config = get_default_config("VINT8")
		quant_config.enable_npu_cnn = True

		# Set up quantization with a specified configuration
		quantization_config = Config(global_quant_config=quant_config)
		quantizer = ModelQuantizer(quantization_config)

		float_model_path = "models/resnet50-v1-12.onnx"
		quantized_model_path = "models/resnet50-v1-12_quantized.onnx"
		calib_data_path = "calib_data"
		model_input_name = get_model_input_name(float_model_path)
		calib_data_reader = ImageDataReader(calib_data_path, model_input_name)

		# Quantize the ONNX model and save to specified path
		quantizer.quantize_model(float_model_path, quantized_model_path, calibration_data_reader=calib_data_reader)

	**4. Run Quark Quantizer**


	Use the *quantize.py* created above and run quantization:

	.. code-block::

		pip install opencv-python torch torchvision 
		python3 quantize.py

	Example output:

	.. code-block:: text

		+----------------------+--------------------------------------+
		| Op Type              | Float Model                          |
		+======================+======================================+
		| Conv                 | 53                                   |
		| BatchNormalization   | 53                                   |
		| Relu                 | 49                                   |
		| MaxPool              | 1                                    |
		| Add                  | 16                                   |
		| GlobalAveragePool    | 1                                    |
		| Flatten              | 1                                    |
		| Gemm                 | 1                                    |
		+----------------------+--------------------------------------+
		| Quantized model path | models/resnet50-v1-12_quantized.onnx |
		+----------------------+--------------------------------------+

		+-------------------+------------+----------+----------+
		| Op Type           | Activation | Weights  | Bias     |
		+===================+============+==========+==========+
		| Conv              | INT8(53)   | INT8(53) | INT8(53) |
		| Relu              | INT8(49)   |          |          |
		| MaxPool           | INT8(1)    |          |          |
		| Add               | INT8(16)   |          |          |
		| GlobalAveragePool | INT8(1)    |          |          |
		| Flatten           | INT8(1)    |          |          |
		| Gemm              | INT8(1)    | INT8(1)  | INT8(1)  |
		+-------------------+------------+----------+----------+

	The output quantized model is saved to *models/resnet50-v1-12_quantized.onnx*. And then go next steps to do Vitis AI compilation.

	.. note::
	   The *ImageDataReader* function in *quantize.py* is specific to ResNet50 model. For other models, it needs to be modified according to the model requirements.

	**5. Compile the Quantized Model with Vitis AI compiler**

	Create the file *compile.py* with the following contents:

	.. code-block::

		import onnxruntime

		provider_options_dict = {
			"config_file": 'vitisai_config.json',
			"cache_dir":   'my_cache_dir',
			"cache_key":   'resnet50-v1-12_quantized',
			"log_level":   'info',
			"target": "VAIML"
		}

		session = onnxruntime.InferenceSession(
			'models/resnet50-v1-12_quantized.onnx',
			providers=["VitisAIExecutionProvider"],
			provider_options=[provider_options_dict]
		)

	Create configuration file *vitisai_config.json* with:

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
				 "vaiml_config": {
					"optimize_level": 2
				}
			 }
		 ],
		 "target": "VAIML",
		 "targets": [
		    {
		        "name": "VAIML",
		        "pass": [
		            "init",
		            "vaiml_partition"
		        ]
		    }
		 ]
		}

	Run Vitis AI compilation with the following command:

	.. code-block::

		python3 compile.py

	It takes time to compile the model. After compilation you get the following output:
	
	.. code-block::

		subpartition path = my_cache_dir/resnet50-v1-12_quantized/vaiml_par_0/0
		INFO: [VAIP-VAIML-PASS] No. of Operators : 
		INFO:  VAIML     491
		INFO: [VAIP-VAIML-PASS] No. of Subgraphs : 
		INFO:    NPU     1
		INFO: [VAIP-VAIML-PASS] For detailed compilation results, please refer to my_cache_dir/resnet50-v1-12_quantized/final-vaiml-pass-summary.txt

	
	You can get more details about the compilation results by displaying the content of`my_cache_dir/resnet50-v1-12_quantized/final-vaiml-pass-summary.txt` :

	.. code-block::

		--------- Final Summary of VAIML Pass ----------
		OS: Linux X64
		VAIP commit: bd5c863c3084e7534f5cd59173c631bb8fa07491
		Model: /Resnet/models/resnet50-v1-12_quantized.onnx
		Model signature: 5633833a66fc76d4758bcb34d9f75ee3
		Device: stx
		Model data type: int8 quantized
		Device data type: int8
		Number of operators in the model: 493
		GOPs of the model: 8.09703
		Number of operators supported by VAIML: 491 (99.594%)
		GOPs supported by VAIML: 8.096 (99.993%)
		Number of subgraphs supported by VAIML: 1
		Number of operators offloaded by VAIML: 491 (99.594%)
		GOPs offloaded by VAIML: 8.096 (99.993%)
		Number of subgraphs offloaded by VAIML: 1
		Number of subgraphs with compilation errors (fall back to CPU): 0
		Number of subgraphs above max number of subgraphs allowed(7): 0 (fall back to CPU)
		Stats for offloaded subgraphs
		Subgraph vaiml_par_0 stats: 
		    Type: npu
		    Operators: 491 (99.594%)
		    GOPs : 8.096 (99.993%)  OPs: 8,096,419,216


	**6. Run Inference**

	Create the file *runmodel_pre_cpu.py* with the following contents:

	.. code-block::

		import numpy as np
		import onnxruntime as ort
		import os
		import cv2
		from torchvision import transforms

		onnx_model='models/resnet50-v1-12.onnx'
		onnx_model_vint8 ='models/resnet50-v1-12_quantized.onnx'

		# CPU session
		cpu_session = ort.InferenceSession(
		    onnx_model,
		    providers=["CPUExecutionProvider"]
		)

		# CPU session with VINT8 quantized model
		cpu_session_vint8 = ort.InferenceSession(
		    onnx_model_vint8,
		    providers=["CPUExecutionProvider"]
		)

		# You can define your preprocess method
		def preprocess_image(image_path):
		    transform = transforms.Compose([
		        transforms.ToPILImage(),
		        transforms.Resize((224, 224)),
		        transforms.ToTensor(),
		        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
		    ])

		    image = cv2.imread(image_path)
		    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		    image = transform(image)
		    image = image.unsqueeze(0)
		    image = image.numpy()
		    return image

		input_folder="val_data"
		def run_inference(session, output_dir="output_cpu"):
		    files = sorted([f for f in os.listdir(input_folder) if f.endswith(".jpg")])
		    input_name = session.get_inputs()[0].name
		    runs=0
		    for i,f in enumerate(files):
		        runs+=1
		        fp = os.path.join(input_folder, f)
		        image = preprocess_image(fp)
		        os.makedirs("input", exist_ok=True)
		        np.save(f"input/input_{i}.npy", image)
		        outputs = session.run(None, {input_name:image})
		        # Create outpu directory if it doesn't exist
		        os.makedirs(output_dir, exist_ok=True)
		        for idx, out in enumerate(outputs):
		            np.save(f"{output_dir}/output_{i}_{idx}.npy", out)

		run_inference(cpu_session,"output_cpu")
		run_inference(cpu_session_vint8,"output_cpu_vint8")

	Run following command:

	.. code-block::

		python3 runmodel_pre_cpu.py

	It runs inferences on CPU and save input numpy vectors for NPU processing. Next, create file *runmodel.py* with the following contents:

	.. code-block::

		import numpy as np
		import onnxruntime as ort
		import os

		onnx_model_vint8 ='models/resnet50-v1-12_quantized.onnx'

		provider_options_dict = {
		    "config_file": 'vitisai_config.json',
		    "cache_dir":   'my_cache_dir',
		    "cache_key":   'resnet50-v1-12_quantized',
		    "log_level":   'info',
			"target": "VAIML"
		}

		# NPU session
		npu_session = ort.InferenceSession(
		    onnx_model_vint8,
		    providers=["VitisAIExecutionProvider"],
		    provider_options=[provider_options_dict]
		)

		input_folder="input"
		output_folder="output_npu"
		files = sorted([f for f in os.listdir(input_folder) if f.endswith(".npy")])
		input_name = npu_session.get_inputs()[0].name
		for i,f in enumerate(files):
		    fp = os.path.join(input_folder, f)
		    image = np.load(fp)
		    outputs = npu_session.run(None, {input_name:image})
		    # Create outpu directory if it doesn't exist
		    os.makedirs(output_folder, exist_ok=True)
		    for idx, out in enumerate(outputs):
		        np.save(f"{output_folder}/output_{i}_{idx}.npy", out)
		print("Inference done")

	On the board, run inference with the following command:

	.. code-block::

		python3 runmodel.py
		
	The script runs three inferences of the model and displays messages similar to the following:
	
	.. code-block::

		Inference done
		
	If you want to see detailed NPU execution logs, set the environment variable `DEBUG_LOG_LEVEL=info` before running the script:
 
 	.. code-block::

		export DEBUG_LOG_LEVEL=info
		python runmodel.py
 

 	The output includes the number of VAIML operators and the number of NPU-executed subgraphs:
 
	 .. code-block::
	
		I20380419 04:55:16.083313  2046 stat.cpp:193] [Vitis AI EP] No. of Operators :
		I20380419 04:55:16.083366  2046 stat.cpp:204]  VAIML   491 
		I20380419 04:55:16.083384  2046 stat.cpp:204] VITIS_EP_CPU     2 
		I20380419 04:55:16.083395  2046 stat.cpp:213] 
		I20380419 04:55:16.083404  2046 stat.cpp:218] [Vitis AI EP] No. of Subgraphs :
		I20380419 04:55:16.083410  2046 stat.cpp:226]    NPU     1 
		I20380419 04:55:16.083419  2046 stat.cpp:229] Actually running on NPU      1
		I20380419 04:55:16.088616  2046 vitisai_compile_model.cpp:1477] AVG CPU Usage 93.3333%
		I20380419 04:55:16.088671  2046 vitisai_compile_model.cpp:1478] Peak Working Set size 129.445 MB
		2038-04-19 04:55:16.093139780 [W:onnxruntime:, session_state.cc:1316 VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
		2038-04-19 04:55:16.093185510 [W:onnxruntime:, session_state.cc:1318 VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
		[2038-04-19 04:55:16.146] [console] [info] [FLEXMLRT] /proj/aiebuilds/IPU/ONNX-EP/IPU/Vitis-AI-IPU-ONNX_EP/RAI_1_7_VAI_RT_BUILD/2242/arm/flexml_rt/src/FlexMLClient.cpp:1269 FlexMLRT Git Hash: 512d4e65
		Inference done
		
	**7. Evaluation**

	Quark provides a tool to compare the differences between different inference results using L2 Loss and other metrics. For example, run following command:

	.. code-block::

		python3 -m quark.onnx.tools.evaluate --baseline_results_folder output_cpu_vint8 --quantized_results_folder output_npu

	Example output:

	.. code-block::

		Mean cos similarity: 0.9987082481384277
		Min cos similarity: 0.9984074831008911
		Mean l2 distance: 3.657916784286499
		Max l2 distance: 4.2315778732299805
		Mean psnr: 38.722272316614784
		Min psnr: 36.79283380508423
		Mean ssim: 0.9994073510169983
		Min ssim: 0.9993097186088562

	In addition to the built-in evaluation capabilities, you can also develop and integrate domain specific post-processing scripts. These scripts can be tailored to specific use cases, enabling more detailed comparison of results or the computation of custom accuracy metrics.

Quantization Using Random Data
-------------------------------

To use random data rather than calibration images, replace *quantize.py* with the following. When no calibration data reader is provided, the ``VINT8`` configuration calibrates with random data automatically:

.. code-block::

	import os
	import cv2
	import numpy as np
	from torchvision import transforms

	from quark.onnx.quantization.config import Config, get_default_config
	from quark.onnx import ModelQuantizer
	from onnxruntime.quantization import QuantType

	quant_config = get_default_config("VINT8")
	quant_config.enable_npu_cnn = True

	# Set up quantization with a specified configuration
	quantization_config = Config(global_quant_config=quant_config)
	quantizer = ModelQuantizer(quantization_config)
	float_model_path = "models/resnet50-v1-12.onnx"
	quantized_model_path = "models/resnet50-v1-12_quantized.onnx"
	# Quantize the ONNX model and save to specified path
	quantizer.quantize_model(float_model_path, quantized_model_path, calibration_data_reader=None)

Execute:

.. code-block::

	python3 quantize.py

Other steps remain same for quantization with calibration data or random data.

For more information about Quark quantization, refer to https://quark.docs.amd.com/latest/.
