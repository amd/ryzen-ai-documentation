Linux Installation Guide
============================================


Overview
--------

This section describes how to install **AMD Ryzen™ AI 1.9 Software** on Linux using the ``setup_ryzen_ai.sh`` installer script.

A standard installation performs the following steps:

.. list-table::
   :header-rows: 1
   :widths: 10 90

   * - Step
     - Action
   * - 1
     - Installs the C++ runtime into ``/opt/amd/ryzen-ai`` (requires ``sudo``).
   * - 2
     - Creates a Python virtual environment at ``~/ryzen-ai-venv``.
   * - 3
     - Installs the Ryzen AI Python packages and their dependencies.
   * - 4
     - Configures the virtual environment with the required library paths.
   * - 5
     - Verifies the available ONNX Runtime providers.

Prerequisites
-------------

Ensure the following requirements are met before you begin.

System Requirements
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Requirement
     - Details
   * - **Operating system**
     - A supported Linux distribution. Ubuntu 22.04 or newer is recommended.
   * - **Python**
     - Python 3.12 and the corresponding virtual-environment package
   * - **Disk space**
     - At least 20 GB free
   * - **NPU driver stack**
     - XRT installed at ``/opt/xilinx/xrt`` (required for NPU access)
   * - **Runtime package**
     - The Ryzen AI 1.9 runtime ``.deb`` package
   * - **Package access**
     - Access to the AMD Ryzen AI Python package index, **or** a directory containing the required wheels

.. _install-python-312:

Install Python 3.12
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   sudo apt update
   sudo apt install python3.12 python3.12-venv

License Agreements
------------------

Before installing, review and accept the following license agreements:

- `AMD End User License Agreement <https://account.amd.com/content/dam/account/en/licenses/download/amd-end-user-license-agreement.pdf>`_
- `Third Party EULA <https://account.amd.com/content/dam/account/en/licenses/download/ryzen-ai-1-9-0-linux-tpn-license.pdf>`_

Acceptance is indicated at install time by passing ``-a yes`` to the installer.

Quick Start
-----------

View Built-in Help
~~~~~~~~~~~~~~~~~~

Display all supported installer options:

.. code-block:: bash

   ./setup_ryzen_ai.sh -h

If the script is not executable, run it through Bash:

.. code-block:: bash

   bash setup_ryzen_ai.sh -h

Standard Installation
~~~~~~~~~~~~~~~~~~~~~

Make the script executable, then run it with the path to the runtime package:

.. code-block:: bash

   chmod +x setup_ryzen_ai.sh
   ./setup_ryzen_ai.sh -a yes -d ./ryzen-ai-runtime_1.9.0-1_amd64.deb

.. note::

   Replace the ``.deb`` filename with the name of the package you received.

Installer Options
-----------------

.. list-table::
   :header-rows: 1
   :widths: 15 40 10 35

   * - Option
     - Description
     - Required
     - Default
   * - ``-a <yes>``
     - Agree to the AMD and Third Party EULAs
     - Yes
     - —
   * - ``-d <path>``
     - Path to the Ryzen AI runtime ``.deb`` file
     - Yes
     - —
   * - ``-p <path>``
     - Virtual environment path
     - No
     - ``~/ryzen-ai-venv``
   * - ``-c <path>``
     - Custom C++ runtime installation path
     - No
     - ``/opt/amd/ryzen-ai``
   * - ``-w <dir>``
     - Local directory containing Python wheels
     - No
     - —
   * - ``-i <url>``
     - Ryzen AI package index or wheel URL
     - No
     - ``https://pypi.amd.com/simple/``
   * - ``-n <name>``
     - Virtual environment prompt name
     - No
     - ``ryzen-ai``
   * - ``-y``
     - Skip confirmation prompts
     - No
     - —
   * - ``-h``
     - Show help
     - No
     - —

Installation Scenarios
----------------------

Installation Without ``sudo``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To extract the C++ runtime to a user-writable directory, use ``-c``:

.. code-block:: bash

   ./setup_ryzen_ai.sh \
     -a yes \
     -d ./ryzen-ai-runtime_1.9.0-1_amd64.deb \
     -c "$HOME/ryzen-ai-runtime"

The script places the runtime under the selected directory and configures the virtual environment to use it.

Installation from a Custom Python Package URL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``-i`` to provide a custom Python package index or URL that hosts the Ryzen AI wheels:

.. code-block:: bash

   ./setup_ryzen_ai.sh \
     -a yes \
     -d ./ryzen-ai-runtime_1.9.0-1_amd64.deb \
     -i https://packages.example.com/ryzen-ai/simple/

The default package index is:

.. code-block:: text

   https://pypi.amd.com/simple/

How the ``-i`` value is interpreted:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Value
     - Treated as
   * - URL ending in ``/simple/``
     - Python package index
   * - Other HTTP URL
     - Directory of wheel files
   * - Local directory path
     - Directory of wheel files

Example using a local directory:

.. code-block:: bash

   ./setup_ryzen_ai.sh \
     -a yes \
     -d ./ryzen-ai-runtime_1.9.0-1_amd64.deb \
     -i path/to/ryzen-ai-wheels

Installation from Local Python Wheels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the Ryzen AI wheels are already available locally, use ``-w``:

.. code-block:: bash

   ./setup_ryzen_ai.sh \
     -a yes \
     -d ./ryzen-ai-runtime_1.9.0-1_amd64.deb \
     -w ./wheels

The ``wheels`` directory must contain ``.whl`` files. The installer also obtains the required CPU versions of PyTorch and torchvision.

Installation to a Custom Virtual Environment Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``-p`` to place the virtual environment somewhere other than the default ``~/ryzen-ai-venv``:

.. code-block:: bash

   ./setup_ryzen_ai.sh \
     -a yes \
     -d ./ryzen-ai-runtime_1.9.0-1_amd64.deb \
     -p "$HOME/venvs/ryzen-ai"

The ``-p`` path can be any location the current user can write to. For a system path such as ``/opt/venvs/ryzen-ai``, create the directory and grant the current user access first:

.. code-block:: bash

   sudo mkdir -p /opt/venvs/ryzen-ai
   sudo chown -R "$USER":"$USER" /opt/venvs
   ./setup_ryzen_ai.sh \
     -a yes \
     -d ./ryzen-ai-runtime_1.9.0-1_amd64.deb \
     -p /opt/venvs/ryzen-ai

After installation, activate the custom environment using the same path:

.. code-block:: bash

   source /opt/venvs/ryzen-ai/bin/activate

Activate and Verify the Installation
------------------------------------

Activate the Environment
~~~~~~~~~~~~~~~~~~~~~~~~

Activate the default environment:

.. code-block:: bash

   source "$HOME/ryzen-ai-venv/bin/activate"

Check ONNX Runtime Providers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python -c "import onnxruntime; print(onnxruntime.get_available_providers())"

``VitisAIExecutionProvider`` should appear in the output when XRT and the NPU runtime are configured correctly.

Run the Quick Test
~~~~~~~~~~~~~~~~~~

Run the quick test from the installed runtime directory:

.. code-block:: bash

   cd /opt/amd/ryzen-ai/quicktest
   python3 quicktest.py

.. note::

   For a custom C++ runtime installation (``-c``), use the corresponding runtime path instead.

Deactivate the Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   deactivate

Important Notes
---------------

- **Existing environments:** If the virtual environment already exists, the installer asks whether it should be overwritten. Use ``-y`` to skip this prompt.
- **XRT dependency:** If XRT is not installed at ``/opt/xilinx/xrt/setup.sh``, the installation may complete, but NPU access will not work until XRT is installed and available.

Troubleshooting
---------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Symptom
     - Resolution
   * - ``python3.12 not found``
     - Install ``python3.12`` and ``python3.12-venv`` (see :ref:`install-python-312`).
   * - ``.deb file not found``
     - Check the path passed to ``-d``.
   * - Insufficient disk space
     - Free space on the filesystem that contains the runtime installation.
   * - ``VitisAIExecutionProvider`` not listed
     - Confirm XRT is installed, re-activate the virtual environment, and check ``LD_LIBRARY_PATH``.
   * - No wheels found
     - Confirm that the directory passed to ``-w`` contains Python wheel (``.whl``) files.
