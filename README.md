## GraphSpace Python Client

A Python library for the GraphSpace REST API. It simplifies the process of authentication, request construction, and response parsing for Python developers using the GraphSpace API. This clientlib is built and tested on Python 2.7.

### Installation

Install graphspace_python from PyPI using:

```
    pip install graphspace_python
```

### Usage

The library uses a client object to query against the API.

#### Add a Graph to GraphSpace

```
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace

graphspace = GraphSpace('user1@example.com', 'user1')

# Users can change the host for the API ENDPOINTS.
# graphspace.set_api_host('localhost:8000') 

graph1 = GSGraph()
graph1.set_name('My Sample Graph')
graph1.add_node('a', popup='sample node popup text', label='A')
graph1.add_node_style('a', shape='ellipse', color='red', width=90, height=90)
graph1.add_node('b', popup='sample node popup text', label='B')
graph1.add_node_style('b', shape='ellipse', color='blue', width=40, height=40)

graph1.add_edge('a', 'b', directed=True, popup='sample edge popup')
graph1.add_edge_style('a', 'b', directed=True, edge_style='dotted')
graph1.set_data(data={
    'description': 'my sample graph'
})
graph1.set_tags(['sample'])
graphspace.post_graph(graph1)
```


#### Get a Graph from GraphSpace

```
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace

graphspace = GraphSpace('user1@example.com', 'user1')

# Users can change the host for the API ENDPOINTS.
# graphspace.set_api_host('localhost:8000') 

graphspace.get_graph('My Sample Graph')
```

#### Make a graph publicly viewable on GraphSpace

```
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace

graphspace = GraphSpace('user1@example.com', 'user1')

# Users can change the host for the API ENDPOINTS.
# graphspace.set_api_host('localhost:8000') 

graphspace.make_graph_public('My Sample Graph')
```

#### Make a graph privately viewable on GraphSpace

```
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace

graphspace = GraphSpace('user1@example.com', 'user1')

# Users can change the host for the API ENDPOINTS.
# graphspace.set_api_host('localhost:8000') 

graphspace.make_graph_private('My Sample Graph')
```

#### Update a graph on GraphSpace

```
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace

graphspace = GraphSpace('user1@example.com', 'user1')

# Users can change the host for the API ENDPOINTS.
# graphspace.set_api_host('localhost:8000') 

graph1 = GSGraph()
graph1.add_node('a', popup='sample node popup text', label='A updated')
graph1.add_node_style('a', shape='ellipse', color='green', width=90, height=90)
graph1.add_node('b', popup='sample node popup text', label='B updated')
graph1.add_node_style('b', shape='ellipse', color='yellow', width=40, height=40)

graph1.add_edge('a', 'b', directed=True, popup='sample edge popup')
graph1.add_edge_style('a', 'b', directed=True, edge_style='dotted')
graph1.set_data(data={
    'description': 'my sample graph'
})

graphspace.update_graph('My Sample Graph', graph=graph1, is_public=1)
```

#### Delete a Graph from GraphSpace

```
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace

graphspace = GraphSpace('user1@example.com', 'user1')

# Users can change the host for the API ENDPOINTS.
# graphspace.set_api_host('localhost:8000') 

graphspace.delete_graph('My Sample Graph')
```
