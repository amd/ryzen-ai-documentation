****************************
Ryzen AI Linux Compile Flow
****************************

BF16 models (CNN or Transformer) require processing power in terms of core count and memory, depending on model size. If a larger model cannot be compiled on a Windows machine due to hardware limitations (e.g., insufficient RAM), an alternative Linux-based compilation flow is supported.

(More info)
RyzenAI software extends beyond Windows to support ONNX models on Linux environment. Under the hood, VAIML compiler runs on CNNs and Transformer architectures and supports full precision (FP32) or Quark Quantized (BF16) input models.
VAIML runs on RyzenAI 1.4 and using Strix Point AI PCs.

- Download the RyzenAI Software Linux installer :download:`ryzen_ai-1.4.0.tgz <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=ryzen_ai-1.4.0-ea.tgz>`.

- Download install script to your Ubuntu (22.04) host

.. code-block::

    tar -xvzf ryzen_ai-1.4.0.tgz -C <EXTRACT TO DIR>
    cd <TARGET DIR>
    chmod a+x install_ryzen_ai_1_4.sh
    cd <TARGET DIR>
    ./install_ryzen_ai_1_4.sh -a yes -p <TARGET PATH TO VENV> -l
    source <TARGET PATH TO VENV>/bin/activate

- Use Docker to install the Ryzen AI Software :download:`ryzen_ai_docker-1.4.0-ea_2025_02_21_3914.tgz <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=ryzen_ai_docker-1.4.0-ea_2025_02_21_3914.tgz>`.

- Installation command:

.. code-block::

    gunzip -c ryzen_ai_docker-1.4.0-ea_2025_02_21_3914.tgz | docker load


- Please refer GTE model to better under the instructions below

``Compiling model on Linux system``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Download the GTE model files in your local linux directory

- Activate your RyzenAI environment from above commands

.. code-block::

    python download_model.py --model_name <> --output_dir <>


This downloads your model under output_dir as model.onnx file

.. code-block::

    python run.py --model_name <>


This script creates a Session that calls VitisAIExecutionProvider to compile your model

The compiled model will be saved under the same directory.

Result: 

    - New folder with Modelname is created locally that contains all compiled model files.

    - You will observe few operators offloaded to CPU and few offloaded to VAIML (NPU)

    - However, there will be an error while attempting to run on NPU. Since Linux machines can only support Model compilation and not Model runtime, so please ignore the error.

``Running Model on Windows system``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have your GTE mnodel compiled on Linux system, copy the whole directory to a STX based Windows Machine

.. code-block::

    Set flexml.dll path (check)

Run the following command

.. code-block::

    python run.py --model_name <>

Result:

    - Session is created from compiled model directory

    - The session will take texts as inputs and run on NPU hardware to generate text embeddings as outputs.
