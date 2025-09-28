#######################
Stable Diffusion Demo
#######################

Ryzen AI 1.6 provides preview demos of Stable Diffusion image-generation pipelines. The demos cover Image-to-Image and Text-to-Image using SD 1.5, SD 2.1-base, SD 2.1, SDXL-base-1.0, SD-Turbo, SDXL-Turbo, SD 3.0 and SD3.5. 

The models for SD 1.5, SD 2.1-base, SD 2.1, SDXL-base-1.0, SD-Turbo, SDXL-Turbo are available for public download. The SD3.0 / SD3.5 models are only available to confirmed Stability AI licensees.

NOTE: Preview features are features which are still undergoing some optimization and fine-tuning. These features are not in their final form and may change as we continue to work in order to mature them into full-fledged features.


******************
Installation Steps
******************

1. Ensure the latest version of Ryzen AI and NPU drivers are installed. See :doc:`inst`.

2. Copy the GenAI-SD folder from the RyzenAI installation tree to your working area, and then go to the copied folder. For instance:

.. code-block:: 

  xcopy /I /E "C:\Program Files\RyzenAI\1.6.0\GenAI-SD" C:\Temp\GenAI-SD
  cd C:\Temp\GenAI-SD

3. Activate the Conda environment for the Stable Diffusion demo packages:

.. code-block:: 
  conda activate ryzen-ai-1.6.0
  conda env update -f rai_env_update.yaml

4. Download the Stable Diffusion models: 

   - :download:`GenAI-SD-models-v0927.zip <https://amdcloud-my.sharepoint.com/:u:/r/personal/chuanlia_amd_com/Documents/sd3_release/sd_release_zip_file/RAI1.6-py312-v0927/GenAI-SD-models-v0927.zip?csf=1&web=1&e=cyFeEg>`
   - :download:`GenAI-SDXL-models-v0927.zip <https://amdcloud-my.sharepoint.com/:u:/r/personal/chuanlia_amd_com/Documents/sd3_release/sd_release_zip_file/RAI1.6-py312-v0927/GenAI-SDXL-models-v0927.zip?csf=1&web=1&e=9bPRpz>`

5. Extract the downloaded zip files and copy the models in the ``GenAI-SD\models`` folder. After installing all the models, the ``GenAI-SD\models`` folder should contain the following subfolders:

   - sd15   
   - sd15_controlnet
   - sd_21_base
   - sd-2.1-v
   - sd_turbo
   - sd_turbo_bs1
   - sdxl_turbo
   - sdxl_turbo_bs1
   - sdxl-base-1.0

******************
Running the Demos
******************

Activate the conda environment::

  conda activate ryzen-ai-1.6.0

Optionally, set the NPU to high performance mode to maximize performance::

  xrt-smi configure --pmode performance

Refer to the documentation on :ref:`xrt-smi configure <xrt-smi-configure>` for additional information.


Image-to-Image with ControlNet
==============================

The image-to-image demo generates images based on a prompt and a control image for a Canny ControlNet. This demo supports SD 1.5 (512x512).

To run the demo, navigate to the ``GenAI-SD\test`` directory and run the following command:

.. code-block:: 

    python .\run_sd15_controlnet.py --model_id 'stable-diffusion-v1-5' --model_path ..\models\sd15_controlnet\

The demo script uses a predefined prompt and ``ref\control.png`` as the control image. The output image and control image are saved in the ``generated_images`` folder.

The control image can be modified and custom prompts can be provided with the ``--prompt`` option. For instance::

  python run_sd15_controlnet.py --prompt "A red bird on a grey sky"


Text-to-Image
=============

The text-to-image generates images based on text prompts. This demo supports SD 1.5 (512x512), SD 2.1-base (512x512), SD 2.1 (768x768), SDXL-base (1024x1024), SD-Turbo (512x512) and SDXL-Turbo (512x512).

To run the demo, navigate to the ``GenAI-SD\test`` directory and run the following commands to run with each of the supported models:

.. code-block:: 

  python run_sd.py    --model_id 'stable-diffusion-v1-5/stable-diffusion-v1-5' --model_path ..\models\sd15\
  python run_sd.py    --model_id 'stabilityai/stable-diffusion-2-1-base' --model_path ..\models\sd_21_base
  python run_sd.py    --model_id 'stabilityai/stable-diffusion-2-1' --model_path ..\models\sd-2.1-v\
  python run_sd.py    --model_id 'stabilityai/sd-turbo' --model_path ..\models\sd_turbo
  python run_sd.py    --model_id 'stabilityai/sd-turbo' --model_path ..\models\sd_turbo_bs1 --num_images_per_prompt 1
  python run_sd_xl.py --model_id 'stabilityai/sdxl-turbo' --model_path ..\models\sdxl_turbo
  python run_sd_xl.py --model_id 'stabilityai/sdxl-turbo' --model_path ..\models\sdxl_turbo_bs1 --num_images_per_prompt 1
  python run_sd_xl.py --model_id 'stabilityai/stable-diffusion-xl-base-1.0'  --model_path ..\models\sdxl-base-1.0\
  

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

..   conda activate ryzen-ai-1.6.0

.. 3. Copy the GenAI-SD folder from the RyzenAI installation tree to your working area, and then go to the copied folder. For instance:

.. .. code-block:: 

..   xcopy /I /E "%RYZEN_AI_INSTALLATION_PATH%\GenAI-SD" C:\Temp\GenAI-SD
..   cd C:\Temp\GenAI-SD

.. 4. Update the Ryzen AI conda environment and install additional dependencies:

.. .. code-block:: 

..   conda env update -f rai_env_update.yaml
..   pip install "%RYZEN_AI_INSTALLATION_PATH%\atom-1.0-cp312-cp312-win_amd64.whl"
