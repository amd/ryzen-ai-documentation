ONNX Runtime Python Inference
=============================

Model Execution 
-----------------

**Using Directory Structure Format:**

1. Locate your compiled model directory: ``cache_dir/cache_key``

2. Copy the entire ``cache_key`` directory to your target board:

   .. code-block:: bash

      scp -r cache_dir/cache_key user@target-board:/path/to/models/

3. On the target board, point your inference application to the copied directory

4. Verify the ``vaiml_par_0`` subdirectory and all files are present

**Using Flat-Buffer Format (.rai file):**

1. Locate your compiled model file: ``cache_dir/cache_key/cache_key.rai``

2. Copy the ``.rai`` file to your target board:

   .. code-block:: bash

      scp cache_dir/cache_key/cache_key.rai user@target-board:/path/to/models/

3. On the target board, point your inference application to the ``cache_key`` directory that contains the ``.rai`` file

4. The model is loaded using memory-mapped access for efficient inference


Run the Application
-------------------

After copying the compiled model to the board, run the application:

.. code-block:: bash

   python3 <running_script_name>.py

During the execution of the Python script, the ONNX session automatically detects the presence of a pre-compiled model within the current directory, thereby bypassing any model recompilation process.
