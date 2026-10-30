###########
AI Analyzer
###########

AMD AI Analyzer is a tool that supports analysis and visualization of model compilation and inference on Ryzen AI.

Installation
~~~~~~~~~~~~

If you installed the Ryzen AI software using automatic installer, AI Analyzer is already installed in the conda environment.

If you manually installed the software, you need to install the AI Analyzer wheel file in your environment.


.. code-block::

   python -m pip install %RYZEN_AI_INSTALLATION_PATH%\aianalyzer-<version>.whl


.. note::

AI Analyzer currently supports BF16 Models only. INT8 model analysis is not supported in this version, but we plan to expand support in a future release.

Enabling Profiling and Visualization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The user can enable Profiling and Visualization by passing additional provider options to the ONNXRuntime Inference Session.

.. code-block::

   provider_options = [{
                'config_file': 'vaip_config.json',
                'cacheDir': str(cache_dir),
                'cacheKey': 'modelcachekey',
                'ai_analyzer_visualization': True,
                'ai_analyzer_profiling': True,
            }]
   session = ort.InferenceSession(model.SerializeToString(), providers=providers,
                               provider_options=provider_options)


The ``ai_analyzer_profiling`` flag enables generation of artifacts related to the inference profile. The ``ai_analyzer_visualization`` flag enables generation of artifacts related to graph partitions and operator fusion. The system generates these artifacts as JSON files in the current run directory.

AI Analyzer also supports native ONNX Runtime profiling, which you can use to analyze the parts of the session that run on the CPU. You can enable ONNX Runtime profiling through session options and pass it along with the provider options, as shown here:

.. code-block::

   # Configure session options for profiling
   sess_options = ort.SessionOptions()
   sess_options.enable_profiling = True

   provider_options = [{
                'config_file': 'vaip_config.json',
                'cacheDir': str(cache_dir),
                'cacheKey': 'modelcachekey',
                'ai_analyzer_visualization': True,
                'ai_analyzer_profiling': True,
            }]

  session = ort.InferenceSession(model.SerializeToString(), sess_options, providers=providers,
                               provider_options=provider_options)


Launching AI Analyzer
~~~~~~~~~~~~~~~~~~~~~

After the compiler generates the artifacts, you can invoke `aianalyzer` through the command line as follows:


.. code-block::

    aianalyzer <logdir> <additional options>


**Positional Arguments**

``logdir``: Path to the folder containing generated artifacts

Additional Options

``-v``, ``--version``: Show the version info and exit.

``-b ADDR``, ``--bind ADDR``: Hostname or IP address on which to listen, default is 'localhost'.

``-p PORT``, ``--port PORT``: TCP port on which to listen, default is '8000'.

``-n``, ``--no-browser``: Prevents the opening of the default url in the browser.

``-t TOKEN``, ``--token TOKEN``: Token used for authenticating first-time connections to the server. The default is to generate a new, random token. Setting to an empty string disables authentication altogether, which is not recommended.


Features
~~~~~~~~

AI Analyzer provides visibility into how the compiler compiles and executes your AI model on Ryzen AI hardware. Its two main use cases are:

Analyzing how the compiler partitions and maps the model onto Ryzen AI's CPU and NPU accelerator
2. Profiling model performance as it executes inferencing workloads

When launched, the AI Analyzer server scans the folder specified with the logdir argument. It detects and loads all files relevant to compilation and/or

You can instruct the AI Analyzer server to either start a browser on the same host or return a URL. You can then load that URL into a browser on any host.


User Interface
~~~~~~~~~~~~~~

AI Analyzer has the following three sections as seen in the left-panel navigator:

PARTITIONING - The compiler assigned a breakdown of your model to execute inference across CPU and NPU.
2. NPU INSIGHTS - A detailed look at how the compiler optimizes your model for inference execution on NPU
3. PERFORMANCE - A breakdown of inference execution through the model


The following sections describe these sections in more detail:



PARTITIONING
@@@@@@@@@@@@

This section comprises two pages: Summary and Graph

**Summary**

The Summary page shows how the compiler assigns model operators to Ryzen's CPU and NPU, with charts of GigaOp (GOP) offloading by operator type.

There is also table titled "CPU Because" that shows the reasons why certain operators were not offloaded to the NPU.

**Graph**

The graph page shows an interactive diagram of the partitioned ONNX model, showing graphically how the compiler assigns the layers to the Ryzen hardware.



Toolbar

- You can choose to show/hide individual NPU partitions, if any, with the **Filter by Partition** button
- You can show or hide a panel that displays properties for selected objects through the **Show Properties** toggle button
- You can show or hide the model table through the **Show Table** toggle button.
- Settings

  - Show Processor separates operators that run on CPU and NPU respectively
  - Show Partition separates operators running on the NPU by their respective NPU partition, if any
  - Show Instance Name displays the full hierarchical name for the operators in the ONNX model

All objects in the graph have properties that you can view to the right of the graph.



*Model Table*

This table following the graph lists all objects in the partitioned ONNX model:

- Processor (NPU or CPU)
- Function (Layer)
- Operator
- Ports
- NPU Partitions


NPU INSIGHTS
@@@@@@@@@@@@

This section comprises three pages: Summary, Original Graph, and Optimized Graph.



**Summary**

The Summary page gives an overview of how your model was mapped to the AMD Ryzen NPU. Charts display statistics on the number of operators and total GMACs that have been mapped to the NPU (and, if necessary, back to the CPU via the `Failsafe CPU` mechanism). The statistics are shown per operator type and NPU partition.



**Original Graph**

This is an interactive graph representing your model, lowered to supported NPU primitive operators and divided into partitions if necessary. As with the PARTITIONING graph, a companion table lists all model elements and supports cross-probing with the graph view. The objects in both the graph and the table also cross-probe with the PARTITIONING graph.

Toolbar

You can choose to show/hide individual NPU partitions, if any, with the **Filter by Partition** button
The user can show or hide a panel that displays properties for selected objects using the **Show Properties** toggle button.
The user can show or hide a code viewer showing the MLIR source code with cross-probing by clicking the **Show Code View** button.
You can show and hide the following table using the **Show Table** toggle button.
You can access display options for the graph with the **Settings** button.



**Optimized Graph**

This page shows the final model that is mapped to the NPU after all transformations and optimizations such as fusion and chaining. It also reports the operators that had to be moved back to the CPU through the `Failsafe CPU` mechanism. As usual, there is a companion table below that contains all of the graph's elements, and cross-selection is supported to and from the PARTITIONING graph and the Original Graph.

Toolbar

You can choose to show/hide individual NPU partitions, if any, with the **Filter by Partition** button
The user can show or hide the panel that displays properties for selected objects using the **Show Properties** toggle button.
The following table can be shown and hidden by the user using the **Show Table** toggle button.
The user can access the display options for the graph with the **Settings** button.


PERFORMANCE
@@@@@@@@@@@

Use this section to view the performance of your model on RyzenAI when running one or more inferences. It comprises two pages: Summary and Timeline.



**Summary**

The performance summary page displays several overall statistics for the inference(s), along with charts that break down operator runtime by operator.
When you enable the ONNX Runtime profiler, you see the total inference time—including layers executed on the CPU.
When you enable NPU profiling with the `ai_analyzer_profiling` flag, the tool displays additional NPU‑specific statistics, including GOP and MAC efficiency, and a chart showing runtime per NPU operator type.

The clock frequency field shows the assumed NPU clock frequency, but it is editable. When you change the frequency, the system adjusts all timestamp data—collected as clock cycles but displayed in time units—accordingly.

**Timeline**

The Performance timeline shows a layer-by-layer breakdown of your model's execution.  The upper section is a graphical depiction of layer execution across a timeline, while the lower section shows the same information in tabular format. It is important to note that the Timeline page shows one inference at a time, so if you have captured profiling data for two or more inferences, you can choose which one to display with the **Inferences** chooser.


Within each inference, you can examine the overall model execution or the detailed NPU execution data by using the **Partition** chooser.



Toolbar

The **Show Properties** toggle button can show or hide the panel that displays properties for selected objects.
You can show and hide the following table using the **Show Table** toggle button.
You can download the graphical timeline to SVG using the **Export to SVG** button.


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.

