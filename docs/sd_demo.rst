#######################
Running Models on NPU
#######################

Activate the Python virtual environment (see also `installation-steps`_):

.. code-block:: powershell

   $env:RYZEN_AI_INSTALLATION_PATH = "C:\Program Files\RyzenAI\ryzen-ai-1.9.0"
   & "$env:RYZEN_AI_INSTALLATION_PATH\Scripts\Activate.ps1"

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
