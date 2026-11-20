#######################
Stable Diffusion
#######################

Ryzen AI 1.9.5 includes preview Stable Diffusion demos that run on the AMD NPU.
The demos cover image-to-image (ControlNet Canny, pose, tile, and depth, plus
Segmind-Vega without ControlNet), text-to-image, and SD3.0 inpainting.
Commands for each pipeline are in :doc:`sd_demo`. Medusa (MDS) uses a separate
set of ``-medusa`` models; see :ref:`medusa-models`.

Models download from Hugging Face on first use. SD3.0 and SD3.5 also require a
Hugging Face login, and you may need to accept the license on the model card
before the download starts. Each repository is covered by the Hugging Face
license on its model card. Ryzen AI and NPU driver setup are in :doc:`inst`.


.. _installation-steps:

******************
Installation Steps
******************

1. Install the latest Ryzen AI software and NPU drivers. See :doc:`inst`.

2. The installer creates two directories under ``C:\Program Files\RyzenAI``:

   * ``ryzen-ai-1.9.5`` is the Python virtual environment. Activate it with
     ``Scripts\Activate.ps1`` in PowerShell, or ``Scripts\activate.bat`` in
     Command Prompt.
   * ``1.9.5`` is the runtime. ``RYZEN_AI_INSTALLATION_PATH`` points here.
     ``GenAI-SD`` is ``C:\Program Files\RyzenAI\1.9.5\GenAI-SD``. Run the
     examples from ``GenAI-SD\test``.

   .. code-block:: powershell

      & "C:\Program Files\RyzenAI\ryzen-ai-1.9.5\Scripts\Activate.ps1"
      $env:RYZEN_AI_INSTALLATION_PATH = "C:\Program Files\RyzenAI\1.9.5"
      cd "$env:RYZEN_AI_INSTALLATION_PATH\GenAI-SD\test"

3. On first use, ``run.py`` downloads each model into ``GenAI-SD\models``.
   ``C:\Program Files`` is often read-only, so set
   ``RYZENAI_GENAI_SD_MODELS_ROOT`` to a folder you can write to. Models are
   then downloaded to, and loaded from, that folder.

   .. code-block:: powershell

      $env:RYZENAI_GENAI_SD_MODELS_ROOT = "D:\sd_models"

   Pass ``--output_path`` to store generated images outside the install tree,
   for example ``--output_path C:\Users\<username>\Documents\generated_images``.
   You can instead copy the whole ``GenAI-SD`` directory to a writable location
   and run ``run.py`` from that copy.

   These are the model repositories. Resolution and ``model_id`` details are
   in `supported-models`_.

   - `SD1.5 <https://huggingface.co/amd/stable-diffusion-1.5-amdnpu>`_
   - `SD1.5 ControlNet Canny <https://huggingface.co/amd/sd1.5-controlnet-canny-amdnpu>`_
   - `SD-Turbo <https://huggingface.co/stabilityai/sd-turbo-amdnpu>`_
   - `SDXL-Turbo <https://huggingface.co/stabilityai/sdxl-turbo-amdnpu>`_
   - `SDXL-base <https://huggingface.co/stabilityai/sdxl-base-amdnpu>`_
   - `Segmind-Vega <https://huggingface.co/amd/segmind-vega-amdnpu>`_
   - `DreamShaper XL Lightning <https://huggingface.co/amd/dreamshaper-xl-lightning-amdnpu>`_
   - `SSD-1B <https://huggingface.co/amd/SSD-1B-amdnpu>`_
   - `Playground v2.5 1024px <https://huggingface.co/amd/playground-v2.5-1024px-aesthetic-amdnpu>`_
   - `FLUX.1-Schnell <https://huggingface.co/amd/FLUX.1-schnell-amdnpu>`_
   - `FLUX.2-klein-4B <https://huggingface.co/amd/FLUX.2-klein-4B-amdnpu>`_
   - `SD3.0 <https://huggingface.co/stabilityai/stable-diffusion-3-medium-amdnpu>`_
   - `SD3.5 <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium-amdnpu>`_

   Medusa (MDS) repositories use the ``-medusa`` suffix. Z-Image-Turbo and
   FLUX.3-Klein are Medusa-only. See `Medusa (MDS) models`_.

   - `SD1.5 <https://huggingface.co/amd/stable-diffusion-1.5-amdnpu-medusa>`_
   - `FLUX.2-Klein-4B <https://huggingface.co/amd/FLUX.2-klein-4B-amdnpu-medusa>`_
   - `FLUX.3-Klein <https://huggingface.co/amd/flux-3-image-klein-amdnpu-medusa>`_
   - `Z-Image-Turbo <https://huggingface.co/amd/Z-Image-Turbo-amdnpu-medusa>`_
   - `Segmind-Vega <https://huggingface.co/amd/segmind-vega-amdnpu-medusa>`_
   - `SDXL-Turbo <https://huggingface.co/amd/sdxl-turbo-amdnpu-medusa>`_
   - `SDXL-Base <https://huggingface.co/amd/sdxl-base-amdnpu-medusa>`_
   - `SSD-1B <https://huggingface.co/amd/SSD-1B-amdnpu-medusa>`_
   - `DreamShaper XL Lightning <https://huggingface.co/amd/dreamshaper-xl-lightning-amdnpu-medusa>`_
   - `Playground v2.5 <https://huggingface.co/amd/playground-v2.5-1024px-aesthetic-amdnpu-medusa>`_
   - `FLUX.1-Schnell <https://huggingface.co/amd/FLUX.1-schnell-amdnpu-medusa>`_
   - `SD3.5-Medium <https://huggingface.co/amd/stable-diffusion-3.5-medium-amdnpu-medusa>`_


.. _supported-models:

******************
Supported models
******************

The first table lists each non-Medusa pipeline's task, default resolution,
dynamic-resolution (DynRes) presets, and the Hugging Face ``model_id`` to pass
as ``--model_id``. Where a cell gives both an ``amd`` id and a ``stabilityai``
id, either one works. Medusa repositories are in `Medusa (MDS) models`_.

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
     - ``amd/stable-diffusion-1.5-amdnpu``
   * - New
     - SD1.5
     - i2i-canny
     - 512x512
     - ``amd/sd1.5-controlnet-canny-amdnpu``
   * -
     - SD-Turbo
     - t2i
     - 512x512
     - ``amd/sd-turbo-amdnpu`` (or ``stabilityai/sd-turbo-amdnpu``)
   * -
     - SDXL-Turbo
     - t2i
     - 512x512, 5x DynRes
     - ``amd/sdxl-turbo-amdnpu`` (or ``stabilityai/sdxl-turbo-amdnpu``)
   * -
     - SDXL-base
     - t2i
     - 1024x1024, 20x DynRes
     - ``amd/sdxl-base-amdnpu`` (or ``stabilityai/sdxl-base-amdnpu``)
   * -
     - Segmind-Vega
     - t2i / i2i
     - 1024x1024
     - ``amd/segmind-vega-amdnpu``
   * - New
     - DreamShaper XL Lightning
     - t2i
     - 1024x1024, 20x DynRes
     - ``amd/dreamshaper-xl-lightning-amdnpu``
   * - New
     - SSD-1B
     - t2i
     - 1024x1024, 20x DynRes
     - ``amd/SSD-1B-amdnpu``
   * - New
     - Playground v2.5
     - t2i
     - 1024x1024, 20x DynRes
     - ``amd/playground-v2.5-1024px-aesthetic-amdnpu``
   * - New
     - FLUX.1-Schnell
     - t2i
     - 1024x1024, 20x DynRes
     - ``amd/FLUX.1-schnell-amdnpu``
   * - New
     - FLUX.2-klein-4B
     - t2i
     - 1024x1024
     - ``amd/FLUX.2-klein-4B-amdnpu``
   * -
     - SD3.0
     - t2i / ControlNet / Depth / Canny / Pose / Tile
     - 512x512 (t2i default), 20x DynRes where applicable
     - ``stabilityai/stable-diffusion-3-medium-amdnpu``
   * - New
     - SD3.0
     - i2i-inpainting
     - 1024x1024
     - ``stabilityai/stable-diffusion-3-medium-amdnpu``
   * -
     - SD3.5
     - t2i / ControlNet
     - 512x512 (t2i default), 20x DynRes where applicable
     - ``stabilityai/stable-diffusion-3.5-medium-amdnpu``
   * -
     - SD3.5-ControlNet (Canny)
     - i2i-canny
     - 512x512, 20x DynRes
     - Uses SD3.5 weights plus SD3.0 Canny ControlNet assets (see below)

A DynRes count is the number of width and height presets that pipeline accepts.
The pairs are listed in `Dynamic resolution (DynRes)`_.

.. _medusa-supported-models:

Medusa (MDS) models
===================

On Medusa (MDS), pass a ``model_id`` that ends with ``-medusa``. Z-Image-Turbo
and FLUX.3-Klein are available only on Medusa. Default steps are the ``-n``
value. Commands are in :ref:`medusa-models`.

.. list-table:: Medusa M1.0.3-Beta models
   :header-rows: 1
   :widths: 17 13 11 13 8 10 28

   * - Model
     - App
     - Default resolution
     - Dynamic resolution
     - Preemption
     - Default steps (``-n``)
     - Hugging Face ``model_id``
   * - SD1.5
     - t2i
     - 512x512
     - No
     - No
     - 20
     - `amd/stable-diffusion-1.5-amdnpu-medusa <https://huggingface.co/amd/stable-diffusion-1.5-amdnpu-medusa>`_
   * - FLUX.2-Klein-4B
     - t2i, i2i (1 or 2 inputs)
     - 1024x1024
     - Yes (20 and 11 resolutions)
     - Yes
     - 4
     - `amd/FLUX.2-klein-4B-amdnpu-medusa <https://huggingface.co/amd/FLUX.2-klein-4B-amdnpu-medusa>`_
   * - FLUX.3-Klein
     - t2i
     - 1024x1024
     - No
     - No
     - 16
     - `amd/flux-3-image-klein-amdnpu-medusa <https://huggingface.co/amd/flux-3-image-klein-amdnpu-medusa>`_
   * - Z-Image-Turbo
     - t2i
     - 1024x1024
     - No
     - No
     - 9
     - `amd/Z-Image-Turbo-amdnpu-medusa <https://huggingface.co/amd/Z-Image-Turbo-amdnpu-medusa>`_
   * - Segmind-Vega
     - t2i, i2i
     - 1024x1024
     - No
     - Yes
     - 50
     - `amd/segmind-vega-amdnpu-medusa <https://huggingface.co/amd/segmind-vega-amdnpu-medusa>`_
   * - SDXL-Turbo
     - t2i
     - 512x512
     - Yes (5 resolutions)
     - Yes
     - 1
     - `amd/sdxl-turbo-amdnpu-medusa <https://huggingface.co/amd/sdxl-turbo-amdnpu-medusa>`_
   * - SDXL-Base
     - t2i
     - 1024x1024
     - Yes (20 resolutions)
     - Yes
     - 50
     - `amd/sdxl-base-amdnpu-medusa <https://huggingface.co/amd/sdxl-base-amdnpu-medusa>`_
   * - SSD-1B
     - t2i
     - 1024x1024
     - Yes (20 resolutions)
     - Yes
     - 50
     - `amd/SSD-1B-amdnpu-medusa <https://huggingface.co/amd/SSD-1B-amdnpu-medusa>`_
   * - DreamShaper XL Lightning
     - t2i
     - 1024x1024
     - Yes (20 resolutions)
     - Yes
     - 50
     - `amd/dreamshaper-xl-lightning-amdnpu-medusa <https://huggingface.co/amd/dreamshaper-xl-lightning-amdnpu-medusa>`_
   * - Playground v2.5
     - t2i
     - 1024x1024
     - Yes (20 resolutions)
     - Yes
     - 50
     - `amd/playground-v2.5-1024px-aesthetic-amdnpu-medusa <https://huggingface.co/amd/playground-v2.5-1024px-aesthetic-amdnpu-medusa>`_
   * - FLUX.1-Schnell
     - t2i
     - 1024x1024
     - Yes (20 resolutions)
     - Yes
     - 4
     - `amd/FLUX.1-schnell-amdnpu-medusa <https://huggingface.co/amd/FLUX.1-schnell-amdnpu-medusa>`_
   * - SD3.5-Medium
     - t2i
     - 1024x1024
     - Yes (20 resolutions)
     - Yes
     - 8
     - `amd/stable-diffusion-3.5-medium-amdnpu-medusa <https://huggingface.co/amd/stable-diffusion-3.5-medium-amdnpu-medusa>`_

.. _dynres:

Dynamic resolution (DynRes)
===========================

Pass width and height with ``-W`` and ``-H``. For example, 1152x928 is
``-W 1152 -H 928``. Every side is a multiple of 32, and the batch size is 1.

SDXL-Turbo accepts the 5 resolutions below. Every other DynRes pipeline accepts
the 20. Medusa FLUX.2-Klein-4B also accepts the 11 sizes after that table, for
text-to-image and for image-to-image. The Medusa model table in
:ref:`medusa-supported-models` shows which set each Medusa model uses.

**5 resolutions (SDXL-Turbo)**

512x512, 512x384, 384x512, 512x288, and 288x512 (width x height). These five
sizes are the 512 column of the table below.

**20 resolutions**

Four base sizes, with the same five aspect ratios at each size:

.. list-table:: 20 resolutions (width x height)
   :header-rows: 1
   :widths: 14 18 18 18 22

   * - Aspect (WxH)
     - Base 512x512
     - Base 640x640
     - Base 768x768
     - Base 1024x1024
   * - 1:1
     - 512x512
     - 640x640
     - 768x768
     - 1024x1024
   * - 4:3
     - 512x384
     - 640x480
     - 768x576
     - 1024x768
   * - 3:4
     - 384x512
     - 480x640
     - 576x768
     - 768x1024
   * - 16:9
     - 512x288
     - 640x384
     - 768x448
     - 1024x576
   * - 9:16
     - 288x512
     - 384x640
     - 448x768
     - 576x1024

**11 resolutions (Medusa FLUX.2-Klein-4B)**

These sizes are in addition to the 20 above.

.. list-table:: 11 resolutions (width x height)
   :header-rows: 1
   :widths: 25 25 25 25

   * - 1024x1024
     - 928x1152
     - 1152x928
     - 896x1216
   * - 1216x896
     - 864x1280
     - 1280x864
     - 768x1376
   * - 1376x768
     - 672x1600
     - 1600x672
     -

**SD3.5 Canny ControlNet.** Copy the SD3.0 Canny ControlNet files into the
SD3.5 model layout, as described in the GenAI-SD release notes. Then run the
Canny example with ``--model_id stabilityai/stable-diffusion-3.5-medium-amdnpu``.

********************
Deploy Models on NPU
********************

Commands for each model are in :doc:`sd_demo`.
