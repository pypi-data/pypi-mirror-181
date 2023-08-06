from .constants import LINEAR
from ._exceptions import InvalidGraphError

class AbstractNode:
    """ A single block in the neural network. E.g. could be a single layer, or
        a block composed of multiple layers, such as a transformer block.
    """
    _NAME = 'AbstractNode'

    def __init__(self) -> None:
        """ Sets up the node to have basic functionality, including a name
            attribute based on its type.
        """
        self._name = self._NAME
    
    def get_name(self) -> str:
        return self._name


class AbstractLayer(AbstractNode):
    """ A node representing a single, simple layer of the network. """
    def __init__(self, size: int, activation: str) -> None:
        """ Sets up a node of the given size.
        
        Parameters:
            size: Dimensionality of layer (number of neurons)
            activation: The type of activation function for this layer (see
                        constants.py for options)
        """
        super().__init__()
        self._size = size
        self._activation = activation

    def get_size(self) -> int:
        """ Returns the size of the layer (number of neurons). """
        return self._size
    
    def get_activation(self) -> str:
        """ Returns the type of activation function used in this layer. """
        return self._activation


class InputNode(AbstractLayer):
    """ A node representing the input layer of the network. """
    _NAME = 'input'

    def __init__(self, size: int) -> None:
        """ Sets up an input node of the given size, with a linear activation
            function.
        
        Parameters:
            size: Dimensionality of input layer (i.e. size of the source vocab)
        """
        super().__init__(size, activation=LINEAR)


class OutputNode(AbstractLayer):
    """ A node representing the output layer of the network. """
    _NAME = 'output'


class TransformerNode(AbstractNode):
    """ A node representing an entire transformer block. """
    _NAME = 'transformer'

    def __init__(
        self,
        num_layers: int,
        d_model: int,
        num_heads: int,
        dff: int,
        input_size: int,
        output_size: int,
        dropout: float
    ):
        """ Sets up a transformer node with the given architecture.
        
            Parameters:
                num_layers: The number of layers
                d_model: The dimensionality of the model
                num_heads: Number of heads (for multi-head attention)
                dff: The dimensionality of the feedforward layer
                input_size: Source vocabulary size
                output_size: Target vocabulary size
                dropout: Dropout rate
        """
        super().__init__()

        self._model_info = {
            'num_layers': num_layers,
            'd_model': d_model,
            'num_heads': num_heads,
            'dff': dff,
            'input_size': input_size,
            'output_size': output_size,
            'dropout': dropout,
        }

    def get_info(self) -> dict[str, float]:
        """ Return the information about this transformer's architecture. """
        return self._model_info


class Edge:
    """ A connection from one node to another in the network graph. """
    def __init__(self, from_node: AbstractNode, to_node: AbstractNode) -> None:
        """ Sets up an edge between two nodes.
        
        Parameters:
            from_node: The origin node for this edge.
            to_node: The destination node for this edge.
        """
        self._from = from_node
        self._to = to_node

    def get_from(self) -> AbstractNode:
        """ Returns the node this edge originates from. """
        return self._from
    
    def get_to(self) -> AbstractNode:
        """ Returns the node this edge goes to. """
        return self._to
    
    def change_from(self, new_from: AbstractNode) -> None:
        """ Changes the origin node for this edge to new_from. """
        self._from = new_from
    
    def change_to(self, new_to: AbstractNode) -> None:
        """ Changes the destination node for this edge to new_to. """
        self._to = new_to


class NetworkGraph:
    """ Manages the entire neural network as a graph structure. """
    def __init__(self, nodes: list[AbstractNode], edges: list[Edge]):
        """ Sets up the initial network graph.
        
        Parameters:
            nodes: The nodes in this graph
            edges: The edges in this graph
        """
        self._nodes = nodes
        self._edges = edges
    
    def add_node(self, node: AbstractNode) -> None:
        """ Adds a new node into this graph. """
        self._nodes.append(node)
    
    def add_edge(self, edge: Edge) -> None:
        """ Adds a new edge into this graph. Raises an InvalidGraphError if the
            edge involves unknown nodes.
        
        Parameters:
            edge: The new edge to add.
        """
        if edge.get_from() not in self._nodes or edge.get_to() not in self._nodes:
            raise InvalidGraphError('Edges must be between two known nodes.')
        self._edges.append(edge)
    
    def get_nodes(self) -> list[AbstractNode]:
        """ Returns all nodes currently in the graph. """
        return self._nodes
    
    def get_edges(self) -> list[Edge]:
        """ returns all edges currently in the graph. """
        return self._edges
    
    def get_node_mapping(self) -> dict[str, list[AbstractNode]]:
        """ Returns a mapping between node type names and nodes of that type in
            the graph.
        """
        mapping = {}
        for node in self._nodes:
            mapping[node.get_name()] = mapping.get(node.get_name(), []) + [node]
        return mapping
