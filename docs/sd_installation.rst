#######################
Stable Diffusion
#######################

Ryzen AI 1.8.0 provides preview demos of Stable Diffusion image-generation pipelines.
The demos cover **Image-to-Image** (ControlNet: Canny, Pose, Tile, Depth; plus Segmind-Vega
i2i without ControlNet) and **Text-to-Image** for SD1.5, SD-Turbo, SDXL-base, SDXL-Turbo,
Segmind-Vega, DreamShaper XL Lightning, SSD-1B, Playground v2.5, FLUX.1-Schnell,
FLUX.2-klein-4B, SD3.0, and SD3.5, with **inpainting** where noted for SD3.0.

Models are fetched from Hugging Face on first use (see :doc:`inst` for Ryzen AI and driver
setup). SD3.0 and SD3.5 models require Hugging Face authentication and might also require
acceptance of the model license before they can be downloaded.


******************
Installation Steps
******************

1. Ensure the latest version of Ryzen AI and NPU drivers are installed. See :doc:`inst`.

2. The GenAI-SD folder is located in the RyzenAI installation tree. Navigate to the
   folder and run the following command:

   .. code-block:: powershell

      & "$env:RYZEN_AI_INSTALLATION_PATH\venv\Scripts\Activate.ps1"
      cd "$env:RYZEN_AI_INSTALLATION_PATH\GenAI-SD"

3. Models are downloaded from Hugging Face on first use and cached under
   ``GenAI-SD\models`` or ``$env:RYZENAI_GENAI_SD_MODELS_ROOT``. See `supported-models`_
   for the full list; primary entry points include:

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


.. _supported-models:

******************
Supported models
******************

The following summarizes default application mode, typical resolution /
dynamic-resolution (DynRes) notes, and the recommended Hugging Face ``model_id`` on
AMD NPU-tuned repos.

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
     - Uses SD3.5 AMD weights plus SD3.0 Canny ControlNet assets (see below)

In the Supported models table, the **DynRes** column counts how many dynamic-resolution
presets a pipeline exposes (for example 5x or 20x). The following material spells out which
width x height pairs are in scope.

.. _dynres:

.. rubric:: Dynamic resolution (DynRes)

**Original dynamic-resolution requirements**

These are the classic fixed pairs (per model class) before the expanded preset grid.

* **DynRes 5x:** 512x512, 288x512, 512x288, 384x512, 512x384.
* **DynRes 20x:**

.. list-table:: New DynRes combinations (batch size 1; align to multiple of 32 as required)
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

Public model pages follow the Hugging Face model license (HF LIC) for each repo.

**SD3.5 Canny ControlNet setup:** copy the SD3.0 Canny ControlNet files into the SD3.5
model layout as required by your GenAI-SD tree (per release notes), then run the Canny
example with ``--model_id amd/stable-diffusion-3.5-medium-amdnpu``.

********************
Deploy Models on NPU
********************

This page elaborates on running Stable Diffusion Models on NPU: :doc:`sd_demo`

..
   ------------
   #####################################
   License
   #####################################

   Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_.
   Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_
   for the full license text and copyright notice.
