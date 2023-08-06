# ExecFlow SDK

ExecFlowSDK is designed to accelerate the development of AiiDA/ExecFlow plugins.

The ExecFlowSDK facilitates a fully semantic and seamless integration of third-party tools with ExecFlow, such as external data sources, simulation tools and other knowledge sources. Since ExecFlow is based on AiiDA and exploits the provenance capabilities that AiiDA, the ExecFlowSDK must facilitate storage of data provenance as part of the plugin development (e.g., configuration parameters of a transformation pipeline).

The current version of the SDK include the following main components:

* Integration of OTEAPI pipelines as AiiDA processes.
* Code generation for exporting AiiDA Data Nodes to DLite/SOFT data models to support semantic mappings.
* Workflow generator utility which, based on EMMO Workflows, can generate AiiDA workflows on-the-fly.

The ExecFlowSDK is an expert tool for developers and enrich AiiDA workflows, processes and data with semantics based on EMMO. The SDK is specialized and geared towards working with EMMC embraced technologies for semantic representation, interoperability, and interfaces.

The SDK extends the current AiiDA development process enabling OpenModel to fully utilize the build-in provenance system.

## Build documentation

Searchable HTML Documentation can be generated from the project.
Enable your favourite virtual environment and ensure dependencies are installed:

```shell
pip install -e .[docs]
```

Run sphinx-build from the project folder.
The target folder here is set to `public`.

```shell
sphinx-build docs public
```
