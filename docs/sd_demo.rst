#######################
Stable Diffusion Demo
#######################

Ryzen AI 1.5 provides preview demos of Stable Diffusion image-generation pipelines. The demos cover Image-to-Image and Text-to-Image using SD 1.5, SD 2.1-base, SD-Turbo, SDXL-Turbo and SD 3.0. 

The models for SD 1.5, SD 2.1-base, SD-Turbo, SDXL-Turbo are available for public download. The SD 3.0 models are only available to confirmed Stability AI licensees.

NOTE: Preview features are features which are still undergoing some optimization and fine-tuning. These features are not in their final form and may change as we continue to work in order to mature them into full-fledged features.


******************
Installation Steps
******************

1. Ensure the latest version of Ryzen AI and NPU drivers are installed. See :doc:`inst`.

2. Copy the GenAI-SD folder from the RyzenAI installation tree to your working area, and then go to the copied folder. For instance:

.. code-block:: 

  xcopy /I /E "C:\Program Files\RyzenAI\1.5.0\GenAI-SD" C:\Temp\GenAI-SD
  cd C:\Temp\GenAI-SD

3. Create a Conda environment for the Stable Diffusion demo packages:

.. code-block:: 

  conda update -n base -c defaults conda
  conda env create --file=env.yaml

4. Download the Stable Diffusion models: 

   - :download:`GenAI-SD-models-v0613-v0711.zip <https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=GenAI-SD-models-v0613-v0711.zip>`
   - :download:`GenAI-SDXL-turbo-models-v0613-v0711.zip <https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=GenAI-SDXL-turbo-models-v0613-v0711.zip>`

5. Extract the downloaded zip files and copy the models in the ``GenAI-SD\models`` folder. After installing all the models, the ``GenAI-SD\models`` folder should contain the following subfolders:

   - sd15_controlnet
   - sd_15
   - sd_21_base
   - sd_turbo
   - sdxl_turbo


******************
Running the Demos
******************

Activate the conda environment::

  conda activate ryzenai-stable-diffusion

Optionally, set the NPU to high performance mode to maximize performance::

  xrt-smi configure --pmode performance

Refer to the documentation on :ref:`xrt-smi configure <xrt-smi-configure>` for additional information.


Image-to-Image with ControlNet
==============================

The image-to-image demo generates images based on a prompt and a control image for a Canny ControlNet. This demo supports SD 1.5 (512x512).

To run the demo, navigate to the ``GenAI-SD\test`` directory and run the following command:

.. code-block:: 

    python .\run_sd15_controlnet.py

The demo script uses a predefined prompt and ``ref\control.png`` as the control image. The output image and control image are saved in the ``generated_images`` folder.

The control image can be modified and custom prompts can be provided with the ``--prompt`` option. For instance::

  python run_sd15_controlnet.py --prompt "A red bird on a grey sky"


Text-to-Image
=============

The text-to-image generates images based on text prompts. This demo supports SD 1.5 (512x512), SD 2.1-base (768x768), SD-Turbo (512x512) and SDXL-Turbo (512x512).

To run the demo, navigate to the ``GenAI-SD\test`` directory and run the following commands to run with each of the supported models:

.. code-block:: 

  python run_sd.py    --model_id 'stable-diffusion-v1-5/stable-diffusion-v1-5' --model_path ..\models\sd_15
  python run_sd.py    --model_id 'stabilityai/stable-diffusion-2-1-base' --model_path ..\models\sd_21_base
  python run_sd.py    --model_id 'stabilityai/sd-turbo' --model_path ..\models\sd_turbo
  python run_sd_xl.py --model_id 'stabilityai/sdxl-turbo' --model_path ..\models\sdxl_turbo


The demo script uses a predefined prompt for each of the models. The output images are saved in the ``generated_images`` folder. 

Custom prompts can be provided with the ``--prompt`` option. For instance::

  python run_sd.py --model_id 'stabilityai/stable-diffusion-2-1-base' --model_path ..\models\sd_21_base  --prompt "A bouquet of roses, impressionist style"


..
  ------------
  #####################################
  License
  #####################################

  Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.




.. 1. Ensure the latest version of Ryzen AI and NPU drivers are installed. See :doc:`inst`.

.. 2. Activate the installed Ryzen AI conda environment:

.. .. code-block:: 

..   conda activate ryzen-ai-1.5.0

.. 3. Copy the GenAI-SD folder from the RyzenAI installation tree to your working area, and then go to the copied folder. For instance:

.. .. code-block:: 

..   xcopy /I /E "%RYZEN_AI_INSTALLATION_PATH%\GenAI-SD" C:\Temp\GenAI-SD
..   cd C:\Temp\GenAI-SD

.. 4. Update the Ryzen AI conda environment and install additional dependencies:

.. .. code-block:: 

..   conda env update -f rai_env_update.yaml
..   pip install "%RYZEN_AI_INSTALLATION_PATH%\atom-1.0-cp310-cp310-win_amd64.whl"
..   pip install opencv-python==4.11.0.86
..   pip install accelerate==0.32.0
