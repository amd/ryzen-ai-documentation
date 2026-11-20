#######################
Running Models on NPU
#######################

Activate the Ryzen AI environment and change to ``GenAI-SD\test`` before you run
the examples. Directory layout and the model cache are described in
:ref:`installation-steps`.

.. code-block:: powershell

   & "C:\Program Files\RyzenAI\ryzen-ai-1.9.5\Scripts\Activate.ps1"
   $env:RYZEN_AI_INSTALLATION_PATH = "C:\Program Files\RyzenAI\1.9.5"
   cd "$env:RYZEN_AI_INSTALLATION_PATH\GenAI-SD\test"

To raise NPU performance, switch to performance mode:

.. code-block:: powershell

   xrt-smi configure --pmode performance

Other modes are documented in :ref:`xrt-smi configure <xrt-smi-configure>`.

Each example calls ``run.py`` and passes a Hugging Face model id with
``--model_id``. Flag details are in the ``README.md`` file in the ``GenAI-SD``
directory.

Medusa M1.0.3-Beta adds its own public NPU models, including Z-Image-Turbo and
FLUX.3-Klein, plus dynamic resolution and NPU preemption. See
:ref:`medusa-models`.

Image-to-Image with ControlNet
===============================

Image-to-image generation takes a prompt and a control image. For SD3.x, select
the ControlNet type with ``-C`` (``canny``, ``pose``, ``tile``, or ``depth``).
SD3.x defaults to 512x512; set another size with ``-W`` and ``-H``. Presets are
listed in :ref:`supported-models` and :ref:`Dynamic resolution (DynRes) <dynres>`.

A minimal Canny run:

.. code-block:: powershell

   python run.py -C canny --model_id stabilityai/stable-diffusion-3-medium-amdnpu

If you omit ``--control_image_path``, this example uses ``.\ref\canny.jpg``.
Images are written to ``generated_images`` unless you set ``--output_path``,
for example ``--output_path C:\Users\<username>\Documents\generated_images``.


**SD1.5 ControlNet Canny (i2i-canny)**

.. code-block:: powershell

   python run.py --model_id amd/sd1.5-controlnet-canny-amdnpu

**Segmind-Vega (i2i, no ControlNet path)**

.. code-block:: powershell

   python run.py --model_id amd/segmind-vega-amdnpu --control_image_path .\assets\controlimg_input_1024x1024.png --strength 0.95

**SD3.0 ControlNet (canny / pose / tile / depth)**

.. code-block:: powershell

   python run.py -C canny --model_id stabilityai/stable-diffusion-3-medium-amdnpu --prompt "Anime style illustration of a girl wearing a suit. A moon in sky. In the background we see heavy rain approaching. text 'InstantX' on image" -H 1024 -W 1024 --control_image_path .\ref\canny.jpg -n 50
   python run.py -C pose --model_id stabilityai/stable-diffusion-3-medium-amdnpu --prompt "Anime style illustration of a girl wearing a suit. A moon in sky. In the background we see heavy rain approaching. text 'InstantX' on image" -H 1024 -W 1024 --control_image_path .\ref\pose.jpg -n 50
   python run.py -C tile --model_id stabilityai/stable-diffusion-3-medium-amdnpu --prompt "Anime style illustration of a girl wearing a suit. A moon in sky. In the background we see heavy rain approaching. text 'InstantX' on image" -H 1024 -W 1024 --control_image_path .\ref\tile.jpg -n 50
   python run.py -C depth --model_id stabilityai/stable-diffusion-3-medium-amdnpu -H 1024 -W 1024 --control_image_path .\assets\depth.jpeg -n 50

**SD3.5 ControlNet Canny (i2i-canny)**

After copying SD3.0 Canny ControlNet into the SD3.5 layout as required:

.. code-block:: powershell

   python run.py -C canny --model_id stabilityai/stable-diffusion-3.5-medium-amdnpu --prompt "Anime style illustration of a girl wearing a suit. A moon in sky. In the background we see heavy rain approaching. text 'InstantX' on image" -H 1024 -W 1024 --control_image_path .\ref\canny.jpg -n 50


For SD3 and SD3.5, ``-O1`` (or ``--optimize_o1``) skips selected DiT denoising steps and shortens inference.

Text-to-Image
=============

Text-to-image generation uses a text prompt and no control image. The examples
below cover SD1.5, SD-Turbo, and SDXL-Turbo at 512x512; SDXL-base, Segmind-Vega,
DreamShaper XL Lightning, SSD-1B, Playground v2.5, FLUX.1-Schnell, and
FLUX.2-klein-4B at their default sizes; and SD3.0 / SD3.5 with ``-C None``.
Add ``-H``, ``-W``, and ``-n`` when the pipeline accepts them.

.. code-block:: powershell

   python run.py --model_id amd/stable-diffusion-1.5-amdnpu
   python run.py --model_id stabilityai/sd-turbo-amdnpu
   python run.py --model_id stabilityai/sdxl-turbo-amdnpu
   python run.py --model_id stabilityai/sdxl-base-amdnpu
   python run.py --model_id amd/segmind-vega-amdnpu
   python run.py --model_id amd/dreamshaper-xl-lightning-amdnpu
   python run.py --model_id amd/SSD-1B-amdnpu
   python run.py --model_id amd/playground-v2.5-1024px-aesthetic-amdnpu
   python run.py --model_id amd/FLUX.1-schnell-amdnpu
   python run.py --model_id amd/FLUX.2-klein-4B-amdnpu
   python run.py -C None --model_id stabilityai/stable-diffusion-3-medium-amdnpu -H 1024 -W 1024 -n 50
   python run.py -C None --model_id stabilityai/stable-diffusion-3.5-medium-amdnpu -H 1024 -W 1024 -n 50

Pass a custom prompt with ``--prompt``:

.. code-block:: powershell

   python run.py --model_id stabilityai/stable-diffusion-1.5-amdnpu --prompt "Photo of an ultra realistic sailing ship, dramatic light, pale sunrise, cinematic lighting, battered, low angle, trending on artstation, 4k, hyper realistic, focused, extreme details"

Inpainting
==========

SD3.0 inpainting (``-C Inpainting``) takes a base image and a mask.
``--control_image_path`` and ``--control_mask_path`` accept a local path or a URL.

.. code-block:: powershell

   python run.py --model_id stabilityai/stable-diffusion-3-medium-amdnpu -C Inpainting --prompt "A cat is sitting next to a puppy" --n_prompt "deformed, distorted, disfigured, poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, mutated hands and fingers, disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation, NSFW" -n 28 --controlnet_conditioning_scale 0.95 --control_image_path "https://huggingface.co/alimama-creative/SD3-Controlnet-Inpainting/resolve/main/images/dog.png" --control_mask_path "https://huggingface.co/alimama-creative/SD3-Controlnet-Inpainting/resolve/main/images/dog_mask.png" --seed 42

Running with AMD Stable Diffusion Sandbox
==========================================

AMD SD Sandbox runs Stable Diffusion pipelines on AMD Ryzen AI hardware. Use it
to evaluate, compare, and deploy several pipelines from one interface.

See the `AMD SD Sandbox GitHub repository <https://github.com/amd/sd-sandbox>`_.

.. _medusa-models:

Medusa platform models (M1.0.3-Beta)
=====================================

Medusa M1.0.3-Beta provides NPU-tuned Stable Diffusion pipelines for the Medusa
platform. The models are public Hugging Face repositories, and each one follows
the Hugging Face license on its model card.

What is new in M1.0.3-Beta:

* **New models:** Z-Image-Turbo and FLUX.3-Klein. Both are text-to-image only, at 1024x1024.
* **Dynamic resolution:** most pipelines accept several resolutions and aspect ratios. See :ref:`Dynamic resolution (DynRes) <dynres>`.
* **Preemption:** most pipelines can yield the NPU to another workload. A request waits at most 100 ms at DPM1 (480 MHz). See `Preemption`_.
* **Model cache:** set ``RYZENAI_GENAI_SD_MODELS_ROOT`` to download and load models from another directory. See :ref:`installation-steps`.

.. _medusa-installation:

Installation steps (Medusa)
---------------------------

Install Medusa M1.0.3-Beta with the Ryzen AI 1.9.5 installer. Activate the
environment and set the model cache as described in :ref:`installation-steps`.
``run.py`` is in ``GenAI-SD\test``.

.. note::

   **One installer for several platforms.** The same Ryzen AI installer supports
   STX, KRK, GPT, and MDS. On Medusa (MDS), use a repository whose ``model_id``
   ends with ``-medusa``. See `Supported models (Medusa)`_.

.. tip::

   **Disable VBS for better performance.** Windows Virtualization-based Security (VBS)
   adds overhead to NPU workloads. Turning VBS off improves SD pipeline performance by
   **about 3% to 20%**, depending on the model and resolution.

   To turn VBS off, open **Windows Security > Device security > Core isolation**, set
   **Memory integrity** to **Off**, and restart the PC. Then check ``msinfo32``: the
   "Virtualization-based security" line must no longer show "Running". If it does, disable
   VBS through your organization's policy or with ``bcdedit /set hypervisorlaunchtype off``,
   and restart the PC again.

   VBS is a Windows security feature. Disable it only on systems where this trade-off is
   acceptable.

.. _medusa-supported-models:

Supported models (Medusa)
-------------------------

Each row lists the task, the default resolution, whether dynamic resolution and
preemption are supported, the default number of denoising steps (``-n``), and the
Hugging Face ``model_id`` to pass as ``--model_id``. The width and height presets
are listed in :ref:`Dynamic resolution (DynRes) <dynres>`. Models that support both
text-to-image and image-to-image share one repository. Commands are in
`Running Medusa Models (M1.0.3-Beta)`_.

.. list-table:: Medusa M1.0.3-Beta supported models
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
   * - **FLUX.3-Klein** (new)
     - t2i
     - 1024x1024
     - No
     - No
     - 16
     - `amd/flux-3-image-klein-amdnpu-medusa <https://huggingface.co/amd/flux-3-image-klein-amdnpu-medusa>`_
   * - **Z-Image-Turbo** (new)
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

.. _medusa-preemption:

Preemption
----------

Models marked "Yes" in the Preemption column can be interrupted so the NPU can
run another workload, then resumed. SD1.5, FLUX.3-Klein, and Z-Image-Turbo do
not support preemption in M1.0.3-Beta.

A preemption request waits at most 100 ms at DPM1 (480 MHz).

.. _medusa-running:

Running Medusa Models (M1.0.3-Beta)
-----------------------------------

Run the commands below from ``GenAI-SD\test`` after activating the environment
(:ref:`installation-steps`). ``--model_id`` is required.

.. code-block:: powershell

   python run.py --model_id <model_id> [optional_flags]

``python run.py --help`` lists every flag and its default. ``-n`` sets the number
of denoising steps. A pipeline uses its default resolution unless you pass
``-H`` and ``-W`` (see :ref:`Dynamic resolution (DynRes) <dynres>`).

If the model is not cached yet, ``run.py`` downloads it from Hugging Face into
``GenAI-SD\models``, or into ``$env:RYZENAI_GENAI_SD_MODELS_ROOT`` when that
variable is set. Images are saved under ``GenAI-SD\test\generated_images`` unless
you set ``--output_path``.

**Text-to-Image**

.. code-block:: powershell

   python run.py --model_id "amd/stable-diffusion-1.5-amdnpu-medusa" -n 50 --prompt "a beautiful landscape"
   python run.py --model_id "amd/sdxl-turbo-amdnpu-medusa" -n 4 -H 512 -W 512 --guidance_scale 0.0 --prompt "a beautiful landscape"
   python run.py --model_id "amd/sdxl-base-amdnpu-medusa" -n 30 -H 1024 -W 1024 --prompt "a beautiful landscape"
   python run.py --model_id "amd/segmind-vega-amdnpu-medusa" -n 9 -H 1024 -W 1024 --prompt "a cozy European cafe terrace on a rainy evening"
   python run.py --model_id "amd/dreamshaper-xl-lightning-amdnpu-medusa" -n 50 -H 1024 -W 1024 --prompt "a majestic dragon flying above snow-covered mountains at sunset"
   python run.py --model_id "amd/SSD-1B-amdnpu-medusa" -n 30 -H 1024 -W 1024 --prompt "a red sports car beside a mountain lake at sunrise"
   python run.py --model_id "amd/playground-v2.5-1024px-aesthetic-amdnpu-medusa" -n 30 -H 1024 -W 1024 --prompt "a young woman sitting at a Paris cafe during golden hour"
   python run.py --model_id "amd/FLUX.1-schnell-amdnpu-medusa" -n 4 -H 1024 -W 1024
   python run.py --model_id "amd/stable-diffusion-3.5-medium-amdnpu-medusa" -n 30 -H 1024 -W 1024

**Dynamic resolution**

Pass any size from :ref:`Dynamic resolution (DynRes) <dynres>` with ``-H`` and ``-W``:

.. code-block:: powershell

   python run.py --model_id "amd/sdxl-turbo-amdnpu-medusa" -n 4 -H 512 -W 384 --guidance_scale 0.0 --prompt "a beautiful landscape"
   python run.py --model_id "amd/sdxl-base-amdnpu-medusa" -n 30 -H 576 -W 1024 --prompt "a beautiful landscape"
   python run.py --model_id "amd/FLUX.1-schnell-amdnpu-medusa" -n 4 -H 768 -W 1024
   python run.py --model_id "amd/stable-diffusion-3.5-medium-amdnpu-medusa" -n 30 -H 480 -W 640
   python run.py --model_id "amd/FLUX.2-klein-4B-amdnpu-medusa" -n 4 -H 928 -W 1152 --prompt "a beautiful landscape"
   python run.py --model_id "amd/FLUX.2-klein-4B-amdnpu-medusa" -n 4 -H 768 -W 1024 --prompt "Change the dress to red" --edit_image_path ".\assets\flux2_img2.png"

**Z-Image-Turbo**

.. code-block:: powershell

   python run.py --model_id "amd/Z-Image-Turbo-amdnpu-medusa" -H 1024 -W 1024 -n 9 --seed 42 --prompt "Young Chinese woman in red Hanfu, intricate embroidery. Impeccable makeup, red floral forehead pattern. Elaborate high bun, golden phoenix headdress, red flowers, beads. Holds round folding fan with lady, trees, bird. Soft-lit outdoor night background, silhouetted tiered pagoda, blurred colorful distant lights."

**FLUX.2-Klein-4B and FLUX.3-Klein**

FLUX.2-Klein-4B text-to-image, one-image edit, and two-image edit share one
repository. Pass one path to ``--edit_image_path`` for a single input, or two
paths for two inputs. FLUX.3-Klein is text-to-image only.

.. code-block:: powershell

   python run.py --model_id "amd/FLUX.2-klein-4B-amdnpu-medusa" -H 1024 -W 1024 -n 4 --prompt "A beautiful anime girl with long silver hair and blue eyes, wearing a flowing white dress. Standing in a field of flowers under golden sunset. Soft warm lighting, gentle breeze, petals floating in the air. Highly detailed, delicate face, clean line art, vibrant colors, dreamy atmosphere."
   python run.py --model_id "amd/FLUX.2-klein-4B-amdnpu-medusa" -H 1024 -W 1024 -n 4 --prompt "Change the dress to red" --edit_image_path ".\assets\flux2_img2.png"
   python run.py --model_id "amd/FLUX.2-klein-4B-amdnpu-medusa" -H 1024 -W 1024 -n 4 --prompt "Replace the astronaut in image 1 with the girl in image 2" --edit_image_path ".\assets\flux2_img1.png" ".\assets\flux2_img2.png"

   python run.py --model_id "amd/flux-3-image-klein-amdnpu-medusa" -H 1024 -W 1024 --prompt "A beautiful anime girl with long silver hair and blue eyes, wearing a flowing white dress, standing in a field of flowers under a golden sunset."

**Segmind-Vega (i2i, no ControlNet path)**

Segmind-Vega can edit an image from a control image passed with
``--control_image_path``. ``--strength`` sets how strongly that image influences
the result.

.. code-block:: powershell

   python run.py --model_id "amd/segmind-vega-amdnpu-medusa" --control_image_path .\assets\controlimg_input_1024x1024.png --strength 0.95 --prompt "a cozy European cafe terrace on a rainy evening"

.. note::

   ``test\assets`` holds images for several examples. Medusa commands use only the
   paths shown above.

Output logs
-----------

Each run prints:

* the resolution (``Using resolution from args: {height, width}``)
* the effective configuration (``prompt``, ``n_prompt``, ``num_inference_steps``,
  ``num_images_per_prompt``, ``guidance_scale``, ``control_image_path``,
  ``strength``, ``seed``, and related fields)
* a progress bar for the denoising steps
* a Model Load Summary with each component (tokenizer, text encoder, scheduler,
  UNet or transformer, VAE decoder), its device (CPU, GPU, or NPU), load time in
  seconds, and memory in MB
* total load time and memory, grouped by device
* pipeline execution time
* an ``[Image saved] <path>`` line for each image
