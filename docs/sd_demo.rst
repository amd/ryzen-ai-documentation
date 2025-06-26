#######################
Stable Diffusion Demo
#######################

**TODO**: Add short introduction

******************
Installation Steps
******************

1. Ensure the latest version of Ryzen AI and NPU drivers are installed. See :doc:`inst`.

2. Activate the installed Ryzen AI conda environment:

.. code-block:: 

  conda activate ryzen-ai-1.5.0

3. Copy the GenAI-SD folder from the RyzenAI installation tree to your working area, and then go to the copied folder. For instance:

.. code-block:: 

  xcopy /I /E "%RYZEN_AI_INSTALLATION_PATH%\GenAI-SD" C:\Temp\GenAI-SD
  cd C:\Temp\GenAI-SD

4. Update the Ryzen AI conda environment:

.. code-block:: 

  conda env update -f rai_env_update.yaml

5. Install additional dependencies:

.. code-block:: 

  pip install "%RYZEN_AI_INSTALLATION_PATH%\atom-1.0-cp310-cp310-win_amd64.whl"
  pip install opencv-python

6. Download the Stable Diffusion models, scheduler and tokenizer configure files from HuffingFace **TODO**: Add link when ready

**NOTE**: For AMD internal testing, use the follwing download links:

🔗 https://amdcloud-my.sharepoint.com/:u:/r/personal/chuanlia_amd_com/Documents/sd3_release/sd_release_zip_file/RAI1.5-v0613/GenAI-SD-models-v0613.zip?csf=1&web=1&e=DFaL6j

🔗 https://amdcloud-my.sharepoint.com/:u:/r/personal/chuanlia_amd_com/Documents/sd3_release/sd_release_zip_file/RAI1.5-v0613/GenAI-SDXL-turbo-models-v0613.zip?csf=1&web=1&e=hHUgMr

7. Copy the downloaded models in the ``GenAI-SD\models`` folder. 

8. After installing all the models, the ``GenAI-SD\models`` folder should contain the following subfolders:

   - sd15_controlnet
   - sd_15
   - sd_21_base
   - sd_turbo
   - sdxl_turbo


******************
Running the Demos
******************

Optional: to maximize performance, you can set the NPU to high performance mode by running:

.. code-block:: 

    xrt-smi configure --pmode performance

Refer to the documentation on :ref:`xrt-smi configure <xrt-smi-configure>` for additional information.



Image-to-Image with ControlNet
==============================

The image-to-image demo generates images based a prompt and a control image. This demo supports SD 1.5 (512x512).

To run the demo, navigate to the ``GenAI-SD\test`` directory and run the following command:

.. code-block:: 

    python .\run_sd15_controlnet.py

The demo script uses a predefined prompt and uses ``ref\control.png`` as the control image. The output image is saved in the ``generated_images`` folder. 

The control image can be modified and custom prompts can be provided with the ``--prompt`` option. For instance::

  python .\run_sd15_controlnet.py --prompt "A red bird on a grey sky"


Text-to-Image
=============

The text-to-image generates images based on text prompts. This demo supports SD 1.5 (512x512), SD 2.1-base (768x768), SD-Turbo (512x512) and SDXL-Turbo (512x512).

To run the demo, navigate to the ``GenAI-SD\test`` directory and run the following commands to run with each of the supported models:

.. code-block:: 

  python .\run_sd.py --model_id 'stable-diffusion-v1-5/stable-diffusion-v1-5' --model_path ..\models\sd_15
  python .\run_sd.py --model_id 'stabilityai/sd-turbo' --model_path ..\models\sd_turbo
  python .\run_sd.py --model_id 'stabilityai/stable-diffusion-2-1-base' --model_path ..\models\sd_21_base
  python .\run_sd_xl.py --model_id 'stabilityai/sdxl-turbo' --model_path ..\models\sdxl_turbo


The demo script uses a predefined prompt for each of the models. The output images are saved in the ``generated_images`` folder. 

Custom prompts can be provided with the ``--prompt`` option. For instance::

  C:\Temp\GenAI-SD-v0613\test>python .\run_sd.py --model_id 'stabilityai/stable-diffusion-2-1-base' --model_path ..\models\sd_21_base  --prompt "A bouquet of roses, impressionist style"


