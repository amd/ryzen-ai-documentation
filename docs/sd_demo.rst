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

8. After installating all the models, the ``GenAI-SD\models`` folder should contain the following subfolders:

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



Image-to-Image with ControNet
=============================

Supported models: SD15 (512x512)

Navigate to the ``GenAI-SD\test`` directory and run the following command:

.. code-block:: 

    python .\run_sd15_controlnet.py

Results are saved into the ``generated_images`` folder.  



Text-to-Image
=============

Supported models: SD15 SD-Turbo (512x512), SDXL-Turbo (512x512), SD2.1-base (768x768)

Navigate to the ``GenAI-SD\test`` directory and run the following commands:

.. code-block:: 

    python .\run_sd.py --model_id 'stabilityai/sd_15'      --model_path ..\models\sd_15
    python .\run_sd.py --model_id 'stabilityai/sd_21_base' --model_path ..\models\sd_21_base
    python .\run_sd.py --model_id 'stabilityai/sd_turbo'   --model_path ..\models\sd_turbo
    python .\run_sd.py --model_id 'stabilityai/sdxl_turbo' --model_path ..\models\sdxl_turbo

Results are saved into the ``generated_images`` folder.  

