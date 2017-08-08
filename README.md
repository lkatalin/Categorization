# Categorization

## Goals

This code is part of a larger project at the [Massachusetts Open Cloud](https://github.com/cci-moc/moc-public) aiming to automate decisions about quantity and quality of instrumentation in tracing distributed systems. The Categorization code will group traces that are "similar" based on structure or some other pre-determined quality. Within these groups, variance will be assessed and high variance triggers further instrumentation at points of anomalous system behavior. The idea is that similar traces should behave similarly, and if they don't, further investigation may be warranted. Automating this prodecure escapes the double bind of capturing too little/the wrong information vs. capturing too much information about a system's behavior.

The current status of this code is as mock-up, with useful functionality still being added over time.

## Components

MAIN.py processes a DOT file containing potentially many traces as input. It calls the following modules:
1. **EXTRACT_TRACES.py**, which captures the data from the DOT input, creating a series of trace objects containing metadata. A graph (tree) of nodes and edges is created based on the data read in, and a hash value is calculated for each trace that is a short form of its basic structure.
2. **GROUP_TRACES.py**, which creates a dict based on each trace's hash value from above. Also in this module are a set of functions for processing grouped traces, ex. analyzing the average of and the variance in total response times per structure-group.
3. **EDGE_DATA.py**, which analyzes structure-groups of traces for latency and variance per edge and outputs a covariance matrix of each two edges' response time covariance in a structure-group. High variance will indicate anomalous behavior and will be used to trigger further automated action.

Other helper files include:
* **OBJECTIFY.py** - creates a list of trace objects and their metadata.
* **MAKE_DAG.py** and **MAKE_NODES.py** - work together to create a linked list of node objects (supposedly a directed acyclic graph), each pointing to child and parent nodes, representing system interactions / RPCs. The parentless root node is associated with a trace object and the root node's tree represents the structure of that trace.
* **JSON_PARSER.py _(deprecated - use JSON_DAG.py instead)_** - parses a JSON file (such as the output of OSprofiler) into a DOT file for intake by MAIN.py. Should work as input for main.py, but does not control for concurrency or other important time relationships.
* **JSON_DAG.py** - translates a span-model, JSON-format trace file into a DAG-model, DOT-format trace file.

## Usage

### Option 1: JSON
1. Generate a span-style JSON file with OSProfiler, named `file.json`. (All OSProfiler outputs will be span-style.)
2. Run `python json_dag.py file.json` to output a DAG-style DOT file to stdout, or run `python json_dag.py file.json to-file` to output the same to a file. The file will be named `base_id.dot` where `base_id` is the base ID of the trace, and the file will be generated in the same directory as the one in which `main.py` resides.
3. Run `python main.py base_id.dot` on the file generated in Step 2.

Alternatively: Combine steps 2 and 3 above by running `python json_dag.py file.json | python main.py`.

### Option 2: DOT
If you already have a DAG-style DOT file, skip to Step 3 above by running `python main.py yourfile.dot`.

Currently, `main.py` does not output to a file, only to `stdout`.

## Try it
Download this code and run 'python main.py' on the DOT files in `/samples` or run `python json\_dag.py [filename.json] | python main.py` on the JSON files in `/samples`.
