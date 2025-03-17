****************************
Ryzen AI Linux Compile Flow
****************************

Here is a walk through of compiling a BF16 model on Linux using RyzenAI Linux installer and followed by running inference on windows

Linux Setup
~~~~~~~~~~~
- Download the RyzenAI Software Linux installer :download:`ryzen_ai-1.4.0.tgz <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=ryzen_ai-1.4.0-ea.tgz>`.
- Recommeded RAM 32GB or Higher
- Minimum 8 CPU cores or Higher
- Python 3.10 or Higher
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


**Note** -  We have choosen GTE Model as an example to walk you through the compilation and runtime flow. You can use any Model of your choice and replicate the steps below.


Compiling model on Linux system
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Download the GTE model files in your local linux directory :download:`https://github.com/amd/RyzenAI-SW/tree/main/example/GTE`
- Activate your RyzenAI environment in your linux terminal.
- Navigate to your downloaded model directory

Download the model from Huggingface and convert to Onnx format

.. code-block::

    python download_model.py --model_name "Alibaba-NLP/gte-large-en-v1.5" --output_dir "models"


The script creates a Session that calls VitisAIExecutionProvider to compile your model

.. code-block::

    python run.py --model_path "models/model_quantized_bf16.onnx" --vaiml_compile


**Result**: 

- New folder with Modelname is created locally that contains all compiled model files

- You will observe few operators offloaded to CPU and few offloaded to VAIML (NPU)



Running Model on Windows system
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Linux machines can only support Model compilation and not Model runtime
- After successful model compilation on Linux machine, copy the entire working directory to a STX based Windows machine

Activate your RyzenAI Windows conda environment

.. code-block::

    conda activate <env_name>

The script takes the compiled model and runs the inference on NPU

.. code-block::

    python run.py --model_path "models/model_quantized_bf16.onnx"

**Result**:

- Session is created from compiled model directory

- The session will take texts as inputs and run on NPU hardware to generate text embeddings as outputs.
