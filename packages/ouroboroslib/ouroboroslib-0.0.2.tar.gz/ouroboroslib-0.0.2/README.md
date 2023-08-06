# Ouroboroslib

A Graph Abstract Data Type Library. Named after the symbol of a serprent eating its own tail.

## Installation

`pip3 install ouroboroslib`

## Usage

```py
from ouroboroslib import OuroborosGraph

ouroboros = OuroborosGraph(directed=True)
# Each tuple in the edge list is (starting_node, ending_node, edge_value)
ouroboros.overwrite_graph(edge_list=[(1, 2, 7), (2, 3, 10)])
ouroboros.add_node(4)
ouroboros.add_edge(3, 4, value=7)
ouroboros.delete_node(2)
# {(3, 4, 7)} - only 1 edge because node 2 is deleted
edges = ouroboros.tuple_edges()
```
