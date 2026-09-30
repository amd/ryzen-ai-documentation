#####################################
Stable Diffusion Demo (Medusa M1.0.0)
#####################################

Medusa M1.0.0 provides NPU-tuned Stable Diffusion pipelines for the Medusa platform.
Models are public Hugging Face repositories. Each repository follows the Hugging Face
model license (HF LIC) on its model card.

M1.0.0 runs each pipeline at the default resolution in `m100-supported-models`_. Dynamic
resolution is planned for M1.0.1. The DynRes preset grids in
:ref:`Dynamic resolution (DynRes) <dynres>` belong to Ryzen AI 1.8.0 (:doc:`sd_demo`).


******************
Installation Steps
******************

Medusa M1.0.0 uses the Ryzen AI 1.8.0 GenAI-SD environment: the same conda environment,
``GenAI-SD`` tree, and ``run.py`` entry point. Follow the Installation Steps in
:doc:`sd_demo`, then pass a Medusa ``--model_id`` from this page.

.. _m100-supported-models:

****************
Supported models
****************

Each row lists the application, the default resolution, and the Hugging Face
``model_id``. FLUX.2-klein-4B text-to-image and both image-to-image modes (one input
and two inputs) share one repository. Segmind-Vega text-to-image and image-to-image
also share one repository. Commands are in `m100-running-demos`_.

.. list-table::
   :header-rows: 1
   :widths: 8 18 12 22 35

   * - Notes
     - Model
     - App
     - Default resolution / DynRes
     - ``model_id`` (AMD Hub; ``stabilityai`` equivalent where applicable)
   * -
     - SD1.5
     - t2i
     - 512x512
     - `amd/stable-diffusion-1.5-amdnpu-medusa <https://huggingface.co/amd/stable-diffusion-1.5-amdnpu-medusa>`_
   * -
     - FLUX.2-klein-4B
     - t2i
     - 1024x1024
     - `amd/FLUX.2-klein-4B-amdnpu-medusa <https://huggingface.co/amd/FLUX.2-klein-4B-amdnpu-medusa>`_
   * -
     - FLUX.2-klein-4B (1 input)
     - i2i
     - 1024x1024
     - `amd/FLUX.2-klein-4B-amdnpu-medusa <https://huggingface.co/amd/FLUX.2-klein-4B-amdnpu-medusa>`_
   * -
     - FLUX.2-klein-4B (2 inputs)
     - i2i
     - 1024x1024
     - `amd/FLUX.2-klein-4B-amdnpu-medusa <https://huggingface.co/amd/FLUX.2-klein-4B-amdnpu-medusa>`_
   * -
     - Segmind-Vega
     - t2i
     - 1024x1024
     - `amd/segmind-vega-amdnpu-medusa <https://huggingface.co/amd/segmind-vega-amdnpu-medusa>`_
   * -
     - Segmind-Vega
     - i2i
     - 1024x1024
     - `amd/segmind-vega-amdnpu-medusa <https://huggingface.co/amd/segmind-vega-amdnpu-medusa>`_
   * -
     - SDXL-Turbo
     - t2i
     - 512x512
     - `amd/sdxl-turbo-amdnpu-medusa <https://huggingface.co/amd/sdxl-turbo-amdnpu-medusa>`_
   * -
     - SDXL-base
     - t2i
     - 1024x1024
     - `amd/sdxl-base-amdnpu-medusa <https://huggingface.co/amd/sdxl-base-amdnpu-medusa>`_
   * -
     - SSD-1B
     - t2i
     - 1024x1024
     - `amd/SSD-1B-amdnpu-medusa <https://huggingface.co/amd/SSD-1B-amdnpu-medusa>`_
   * -
     - DreamShaper XL Lightning
     - t2i
     - 1024x1024
     - `amd/dreamshaper-xl-lightning-amdnpu-medusa <https://huggingface.co/amd/dreamshaper-xl-lightning-amdnpu-medusa>`_
   * -
     - Playground v2.5
     - t2i
     - 1024x1024
     - `amd/playground-v2.5-1024px-aesthetic-amdnpu-medusa <https://huggingface.co/amd/playground-v2.5-1024px-aesthetic-amdnpu-medusa>`_
   * -
     - FLUX.1-Schnell
     - t2i
     - 1024x1024
     - `amd/FLUX.1-schnell-amdnpu-medusa <https://huggingface.co/amd/FLUX.1-schnell-amdnpu-medusa>`_
   * -
     - SD3.5-Medium
     - t2i
     - 1024x1024
     - `amd/stable-diffusion-3.5-medium-amdnpu-medusa <https://huggingface.co/amd/stable-diffusion-3.5-medium-amdnpu-medusa>`_

.. _m100-running-demos:

******************
Running the Demos
******************

From the ``GenAI-SD\test`` directory, these examples use ``run.py`` with a Medusa
``--model_id``. M1.0.0 runs at the default resolution listed in `m100-supported-models`_.

Text-to-Image
=============

.. code-block:: powershell

   python .\run.py --model_id amd/stable-diffusion-1.5-amdnpu-medusa
   python .\run.py --model_id amd/sdxl-turbo-amdnpu-medusa
   python .\run.py --model_id amd/sdxl-base-amdnpu-medusa
   python .\run.py --model_id amd/segmind-vega-amdnpu-medusa
   python .\run.py --model_id amd/dreamshaper-xl-lightning-amdnpu-medusa
   python .\run.py --model_id amd/SSD-1B-amdnpu-medusa
   python .\run.py --model_id amd/playground-v2.5-1024px-aesthetic-amdnpu-medusa
   python .\run.py --model_id amd/FLUX.1-schnell-amdnpu-medusa
   python .\run.py -C None --model_id amd/stable-diffusion-3.5-medium-amdnpu-medusa -H 1024 -W 1024 -n 50

FLUX.2-klein-4B
===============

Text-to-image, one-input image edit, and two-input image edit share
``amd/FLUX.2-klein-4B-amdnpu-medusa``.
One input uses a single ``--edit_image_path``; two inputs pass both images to the same flag.

.. code-block:: powershell

   python .\run.py --model_id amd/FLUX.2-klein-4B-amdnpu-medusa -H 1024 -W 1024 -n 4 --prompt "A beautiful anime girl with long silver hair and blue eyes, wearing a flowing white dress.Standing in a field of flowers under golden sunset.Soft warm lighting, gentle breeze, petals floating in the air.Highly detailed, delicate face, clean line art, vibrant colors, dreamy atmosphere."
   python .\run.py --model_id amd/FLUX.2-klein-4B-amdnpu-medusa -H 1024 -W 1024 -n 4 --prompt "Change the dress to red" --edit_image_path ./assets/flux2_img2.png
   python .\run.py --model_id amd/FLUX.2-klein-4B-amdnpu-medusa -H 1024 -W 1024 -n 4 --prompt "Replace the astronaut in image 1 with the girl in image 2" --edit_image_path ./assets/flux2_img1.png ./assets/flux2_img2.png

Segmind-Vega
============

Image-to-image without a ControlNet path:

.. code-block:: powershell

   python .\run.py --model_id amd/segmind-vega-amdnpu-medusa --control_image_path .\assets\controlimg_input_1024x1024.png --strength 0.95
