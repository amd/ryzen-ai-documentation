############################
OnnxRuntime GenAI (OGA) Flow
############################

Ryzen AI Software supports deploying LLMs on Ryzen AI PCs using the native ONNX Runtime Generate (OGA) C++ or Python API. The OGA API is the lowest-level API available for building LLM applications on a Ryzen AI PC. It supports the following execution modes:

- Hybrid execution mode: This mode uses both the NPU and iGPU to achieve the best TTFT and TPS during the prefill and decode phases.
- NPU-only execution mode: This mode uses the NPU exclusively for both the prefill and decode phases.

************************
Supported Configurations
************************

The Ryzen AI OGA flow supports Strix and Krackan Point processors. Phoenix (PHX) and Hawk (HPT) processors are not supported.


************
Requirements
************

- Install NPU Drivers and Ryzen AI MSI installer. See :doc:`inst` for more details.
- Install GPU device driver: Ensure GPU device driver https://www.amd.com/en/support is installed
- Install Git for Windows (needed to download models from HF): https://git-scm.com/downloads

********************
Pre-optimized Models
********************


AMD provides a set of pre-optimized LLMs ready to be deployed with Ryzen AI Software and the supporting runtime for hybrid and/or NPU-only execution. These include popular architectures such as Llama-2, Llama-3, Mistral, DeepSeek Distill models, Qwen-2, Qwen-2.5, Qwen-3, Gemma-2, Phi-3, Phi-3.5, and Phi-4. For the detailed list of supported models, visit :doc:`model_list`

Hugging Face collection of hybrid models: https://huggingface.co/collections/amd/ryzen-ai-16-hybrid-llm-68d9c3ed502f871223bfa882

Hugging Face collection of NPU models: https://huggingface.co/collections/amd/ryzen-ai-16-npu-llm-68d9c927223939cb596c592b

************************************
Changes Compared to Previous Release
************************************

- OGA version is updated to v0.9.2 (Ryzen AI 1.6) from v0.7.0 (Ryzen AI 1.5).
- Starting with the 1.6 release, a new set of hybrid models is published. Hybrid models from earlier releases are not compatible with this version. If you are using Ryzen AI 1.6, please download the updated models.
- Previously published NPU-only models continue to run, but for higher performance download the new NPU-only models published with 1.6.
- Context length support is improved from 2K to 4K tokens (combined input and output).


*******************
Compatible OGA APIs
*******************

Pre-optimized hybrid or NPU LLMs can be executed using the official OGA C++ and Python APIs. The current release is compatible with OGA version 0.9.2.
For detailed documentation and examples, refer to the official OGA repository:
🔗 https://github.com/microsoft/onnxruntime-genai/tree/rel-0.9.2


***************************
LLMs Test Programs
***************************

The Ryzen AI installation includes test programs (in C++ and Python) that can be used to run LLMs and understand how to integrate them in your application.

The steps for deploying the pre-optimized models using the sample programs are described in the following sections.

Steps to run C++ program and sample python script.
==================================================

1. (Optional) Enable Performance Mode

To run LLMs in best performance mode, follow these steps:

- Go to ``Windows`` → ``Settings`` → ``System`` → ``Power``, and set the power mode to **Best Performance**.
- Open a terminal and run:

  .. code-block:: bat

     cd C:\Windows\System32\AMD
     xrt-smi configure --pmode performance

2. Activate the Ryzen AI 1.6.0 Conda Environment and install ``torch`` library.

Run the following commands:

.. code-block:: bash

   conda activate ryzen-ai-1.6.0
   pip install torch==2.7.1

This step is required for running the python script.

.. note::

   For the C++ program, if you choose not to activate the Conda environment, open a Windows Command Prompt and manually set the environment variable before continuing:

   ``set RYZEN_AI_INSTALLATION_PATH=C:\\Program Files\\RyzenAI\\1.6.0``

3. Apply RyzenAI 1.6.0 Patch (Windows Only)

**Steps**
   1. Download and extract `ryzenai-1.6.0-patch.zip` from the link here `https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=ryzenai-1.6.0-patch.zip`
   2. Open an **Administrator** Command Prompt or PowerShell in the extracted folder.
   3. Run:

      .. code-block:: bash

         python ryzenai-1.6.0-patch.py --install-path "C:\Program Files\RyzenAI\1.6.0"
         

C++ Program
===========
Use the ``model_benchmark.exe`` executable to test LLMs and identify DLL dependencies for C++ applications.

1. Set Up a working directory and copy required Files

.. code-block:: bat

   mkdir llm_run
   cd llm_run

   :: Copy the sample C++ executable
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\model_benchmark.exe" .

   :: Copy the sample prompt file
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\amd_genai_prompt.txt" .

   :: Copy required DLLs
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime-genai.dll" .
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime.dll" .
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\ryzen_mm.dll" .
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnx_custom_ops.dll" .
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\libutf8_validity.dll" .
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\abseil_dll.dll" .
   xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\DirectML.dll" .

2. Download model from Hugging Face

.. code-block:: bash

   :: Install Git LFS if you haven't already: https://git-lfs.com
   git lfs install

   :: Clone the model repository
   git clone https://huggingface.co/amd/Llama-2-7b-chat-hf-onnx-ryzenai-hybrid

3. Run ``model_benchmark.exe``

.. code-block:: bash

   .\model_benchmark.exe -i <path_to_model_dir> -f <prompt_file> -l <list_of_prompt_lengths>

   :: Example:
   .\model_benchmark.exe -i Llama-2-7b-chat-hf-onnx-ryzenai-hybrid -f amd_genai_prompt.txt -l "1024"


.. note:: 

   The sample test application model_benchmark.exe accepts -l for input token length and -g for output token length. In Ryzen AI 1.6, models support up to 4096 tokens in total (input + output). By default, -g is set to 128. If the input length is close to 4096, you must adjust -g so the sum of input and output tokens does not exceed 4096. For example, -l 4000 -g 96 is valid (4000 + 96 ≤ 4096), while -l 4000 -g 128 will exceed the limit and result in an error.

Python Script
=============

1. Navigate to your working directory and download model.

.. code-block:: bash

   :: Install Git LFS if you haven't already: https://git-lfs.com
   git lfs install

   :: Clone the model repository
   git clone https://huggingface.co/amd/Llama-2-7b-chat-hf-onnx-ryzenai-hybrid

2. Run sample python script

.. code-block::

     python "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\run_model.py" -m <model_folder> -l <max_length>

     :: Example command
     python "%RYZEN_AI_INSTALLATION_PATH%\LLM\example\run_model.py" -m "Llama-2-7b-chat-hf-onnx-ryzenai-hybrid" -l 256


.. note:: 

   Some models may return non-printable characters in their output (for example, Qwen models), which can cause a crash while printing the output text. To avoid this, modify the provided script %RYZEN_AI_INSTALLATION_PATH%\\LLM\\example\\run_model.py by adding a text sanitization function and updating the print statement as shown below.

   Add sanitize_string function:

   .. code-block:: 
      
      def sanitize_string(input_string):
         return input_string.encode("charmap", "ignore").decode("charmap")


   Update line 80 to print sanitized output:

   .. code-block:: 

      print("Output:", sanitize_string(output_text))


   This sanitization fix will be included in the run_model.py script in the next release.


**************************************
Building C++ Applications
**************************************

A complete example including C++ source and build instructions is available in the RyzenAI-SW repository: https://github.com/amd/RyzenAI-SW/tree/main/example/llm/oga_api

****************
LLM Config Files
****************

Each OGA model folder contains a ``genai_config.json`` file. This file contains various configuration settings for the model. The ``session_option`` section is where information about specific runtime dependencies is specified. Within this section, the ``custom_ops_library`` option sets the path to the ``onnx_custom_ops.dll`` file for Hybrid and NPU models.

The following sample shows the defaults for the AMD pre-optimized OGA LLMs:

.. code-block:: json

       "session_options": {
           "log_id": "onnxruntime-genai",
           "custom_ops_library": "onnx_custom_ops.dll",
           ...


The paths is relative to the folder where the program is run from. The model throws an error if the ``onnx_custom_ops.dll`` file cannot be found at the specified location. Replacing the relative path with an absolute path to this file allows running the program from any location.


***********************
Using Fine-Tuned Models
***********************

It is also possible to run fine-tuned versions of the pre-optimized OGA models.

To do this, the fine-tuned models must first be prepared for execution with the OGA flow. For instructions on how to do this, refer to the page about :doc:`oga_model_prepare`.

After a fine-tuned model has been prepared for execution, it can be deployed by following the steps described previously in this page.

*****************************
Running LLM via pip install
*****************************

In addition to the full RyzenAI software stack, we also provide standalone wheel files for the users who prefer using their own environment. To prepare an environment for running the Hybrid and NPU-only LLM independently, perform the following steps:

1. Create a new python environment and activate it.

.. code-block:: bash

   conda create -n <env_name> python=3.12 -y
   conda activate <env_name>

2. Install onnxruntime-genai wheel file.

.. code-block:: bash

   pip install onnxruntime-genai-directml-ryzenai==0.9.2 --extra-index-url=https://pypi.amd.com/simple

3. Navigate to your working directory and download the desired Hybrid/NPU model

.. code-block:: bash

   cd working_directory
   git clone <link_to_model>

4. Run the Hybrid or NPU model.
