# Categorization

## Goals

This code is part of a larger project at the [Massachusetts Open Cloud](https://github.com/cci-moc/moc-public) aiming to automate decisions about quantity and quality of instrumentation in tracing distributed systems. The Categorization code will group traces that are "similar" based on structure or some other pre-determined quality. Within these groups, variance will be assessed and high variance triggers further instrumentation at points of anomalous system behavior. The idea is that similar traces should behave similarly, and if they don't, further investigation may be warranted. Automating this prodecure escapes the double bind of capturing too little/the wrong information vs. capturing too much information about a system's behavior.

The current status of this code is as mock-up, with useful functionality still being added over time.

## Components

MAIN.py processes a DOT file containing potentially many traces as input. It calls the following modules:
1. **EXTRACT_TRACES.py**, which captures the data from the DOT input, creating a series of trace objects containing metadata. A graph (tree) of nodes and edges is created based on the data read in, and a hash value is calculated for each trace that is a short form of its basic structure.
2. **GROUP_TRACES.py**, which creates a dict based on each trace's hash value from above. Also in this module are a set of functions for processing grouped traces, ex. analyzing the variance in response time per group as well as per edge across traces in a group, and calculating the covariance of response time for each two edges in a group. High variance will indicate anomalous behavior and will be used to trigger further automated action.

Other helper files include:
* **OBJECTIFY.py** - creates a list of trace objects and their metadata.
* **MAKE_DAG.py** and **MAKE_NODES.py** - work together to create a linked list of node objects (supposedly a directed acyclic graph), each pointing to child and parent nodes, representing system interactions / RPCs. The parentless root node is associated with a trace object and the root node's tree represents the structure of that trace.
* **JSON_PARSER.py** - parses a JSON file (such as the output of OSprofiler) into a DOT file for intake by MAIN.py.
* **JSON_DAG.py** - translates a span-model, JSON-format trace file into a DAG-model, DOT-format trace file.
