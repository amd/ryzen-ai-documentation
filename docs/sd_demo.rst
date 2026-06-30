#######################
Stable Diffusion Demo
#######################

Ryzen AI 1.8.0 provides preview demos of Stable Diffusion image-generation pipelines.
The demos cover **Image-to-Image** (ControlNet: Canny, Pose, Tile, Depth; plus Segmind-Vega
i2i without ControlNet) and **Text-to-Image** for SD1.5, SD-Turbo, SDXL-base, SDXL-Turbo,
Segmind-Vega, DreamShaper XL Lightning, SSD-1B, Playground v2.5, FLUX.1-Schnell,
FLUX.2-klein-4B, SD3.0, and SD3.5, with **inpainting** where noted for SD3.0.

Models are fetched from Hugging Face on first use (see :doc:`inst` for Ryzen AI and driver
setup). SD3.0 and SD3.5 models require Hugging Face authentication and may also require
acceptance of the model license before they can be downloaded.


******************
Installation Steps
******************

1. Ensure the latest version of Ryzen AI and NPU drivers are installed. See :doc:`inst`.

2. The GenAI-SD folder is located in the RyzenAI installation tree. Navigate to the
   folder and run the following command:

   .. code-block:: powershell

      conda activate ryzen-ai-1.8.0
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

******************
Running the Demos
******************

Activate the conda environment (see also `installation-steps`_):

.. code-block:: powershell

   conda activate ryzen-ai-1.8.0

Optionally, set the NPU to high performance mode to maximize performance:

.. code-block:: powershell

   xrt-smi configure --pmode performance

Refer to the documentation on :ref:`xrt-smi configure <xrt-smi-configure>` for additional options.

From the ``GenAI-SD\test`` directory unless noted otherwise. All examples use the unified
entry point ``run.py`` and pass ``--model_id`` with the Hugging Face model identifier.
For more details, refer to the ``README.md`` file in the ``GenAI-SD`` directory.

Image-to-Image with ControlNet
==============================

The image-to-image demo generates images from a **prompt** plus a **control image**
(ControlNet types such as Canny, pose, tile, or depth for SD3.x, selected with ``-C``).
SD3.x often defaults to 512x512; override resolution with ``-W`` and ``-H`` as in the
examples below. SD3.x DynRes presets are summarized in `supported-models`_ and
`Dynamic resolution (DynRes) <dynres>`_.

To run a minimal Canny example:

.. code-block:: powershell

   python run.py -C canny --model_id stabilityai/stable-diffusion-3-medium-amdnpu

The demo can use ``.\ref\canny.jpg`` as the control image unless you override
``--control_image_path``. Outputs are written to ``generated_images`` by default,
unless ``--output_path`` is specified. You can redirect the output directory to
a location where your user account has write permissions, for example:
``--output_path C:\Users\<username>\Documents\generated_images``.


**SD1.5 ControlNet Canny (i2i-canny)**

.. code-block:: powershell

   python .\run.py --model_id amd/sd1.5-controlnet-canny-amdnpu

**Segmind-Vega (i2i, no ControlNet path)**

.. code-block:: powershell

   python .\run.py --model_id amd/segmind-vega-amdnpu --control_image_path .\assets\controlimg_input_1024x1024.png --strength 0.95

**SD3.0 ControlNet (canny / pose / tile / depth)**

.. code-block:: powershell

   python .\run.py -C canny --model_id stabilityai/stable-diffusion-3-medium-amdnpu --prompt "Anime style illustration of a girl wearing a suit. A moon in sky. In the background we see heavy rain approaching. text 'InstantX' on image" -H 1024 -W 1024 --control_image_path .\ref\canny.jpg -n 50
   python .\run.py -C pose --model_id stabilityai/stable-diffusion-3-medium-amdnpu --prompt "Anime style illustration of a girl wearing a suit. A moon in sky. In the background we see heavy rain approaching. text 'InstantX' on image" -H 1024 -W 1024 --control_image_path .\ref\pose.jpg -n 50
   python .\run.py -C tile --model_id stabilityai/stable-diffusion-3-medium-amdnpu --prompt "Anime style illustration of a girl wearing a suit. A moon in sky. In the background we see heavy rain approaching. text 'InstantX' on image" -H 1024 -W 1024 --control_image_path .\ref\tile.jpg -n 50
   python .\run.py -C depth --model_id stabilityai/stable-diffusion-3-medium-amdnpu -H 1024 -W 1024 --control_image_path .\assets\depth.jpeg -n 50

**SD3.5 ControlNet Canny (i2i-canny)**

After copying SD3.0 Canny ControlNet into the SD3.5 layout as required:

.. code-block:: powershell

   python .\run.py -C canny --model_id stabilityai/stable-diffusion-3.5-medium-amdnpu --prompt "Anime style illustration of a girl wearing a suit. A moon in sky. In the background we see heavy rain approaching. text 'InstantX' on image" -H 1024 -W 1024 --control_image_path .\ref\canny.jpg -n 50


For SD3 and SD3.5 models, pass ``-O1`` (or ``--optimize_o1``) to enable a performance optimization preset that skips selected DiT denoising steps to improve inference performance.

Text-to-Image
=============

The text-to-image demo generates images from **text prompts only** (no control image).
It covers SD1.5 (512-class), SD-Turbo and SDXL-Turbo (512-class), SDXL-base, Segmind-Vega,
DreamShaper XL Lightning, SSD-1B, Playground v2.5, FLUX.1-Schnell, FLUX.2-klein-4B, and
SD3.0 / SD3.5 with ``-C None``. Use ``-H``, ``-W``, and ``-n`` when the pipeline supports
them.

.. code-block:: powershell

   python .\run.py --model_id amd/stable-diffusion-1.5-amdnpu
   python .\run.py --model_id stabilityai/sd-turbo-amdnpu
   python .\run.py --model_id stabilityai/sdxl-turbo-amdnpu
   python .\run.py --model_id stabilityai/sdxl-base-amdnpu
   python .\run.py --model_id amd/segmind-vega-amdnpu
   python .\run.py --model_id amd/dreamshaper-xl-lightning-amdnpu
   python .\run.py --model_id amd/SSD-1B-amdnpu
   python .\run.py --model_id amd/playground-v2.5-1024px-aesthetic-amdnpu
   python .\run.py --model_id amd/FLUX.1-schnell-amdnpu
   python .\run.py --model_id amd/FLUX.2-klein-4B-amdnpu
   python .\run.py -C None --model_id stabilityai/stable-diffusion-3-medium-amdnpu -H 1024 -W 1024 -n 50
   python .\run.py -C None --model_id stabilityai/stable-diffusion-3.5-medium-amdnpu -H 1024 -W 1024 -n 50

Custom prompts can be supplied with ``--prompt``. For example:

.. code-block:: powershell

   python .\run.py --model_id stabilityai/stable-diffusion-1.5-amdnpu --prompt "Photo of an ultra realistic sailing ship, dramatic light, pale sunrise, cinematic lighting, battered, low angle, trending on artstation, 4k, hyper realistic, focused, extreme details"

Inpainting
==========

**SD3.0 (``-C Inpainting``)** uses a base image and ``--control_mask_path`` (URLs or local
paths). This extends the image-conditioned flows above with an explicit mask channel.

.. code-block:: powershell

   python .\run.py --model_id stabilityai/stable-diffusion-3-medium-amdnpu -C Inpainting --prompt "A cat is sitting next to a puppy" --n_prompt "deformed, distorted, disfigured, poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, mutated hands and fingers, disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation, NSFW" -n 28 --controlnet_conditioning_scale 0.95 --control_image_path "https://huggingface.co/alimama-creative/SD3-Controlnet-Inpainting/resolve/main/images/dog.png" --control_mask_path "https://huggingface.co/alimama-creative/SD3-Controlnet-Inpainting/resolve/main/images/dog_mask.png" --seed 42

*****************************************
Running with AMD Stable Diffusion Sandbox
*****************************************

AMD SD Sandbox is a framework for running Stable Diffusion (SD) models accelerated by
AMD Ryzen AI hardware. It provides an easy-to-use interface for evaluating, comparing,
and deploying multiple SD pipelines.

Please go to the `AMD SD Sandbox GitHub repository <https://github.com/amd/sd-sandbox>`_
for more information.

..
   ------------
   #####################################
   License
   #####################################

   Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_.
   Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_
   for the full license text and copyright notice.
