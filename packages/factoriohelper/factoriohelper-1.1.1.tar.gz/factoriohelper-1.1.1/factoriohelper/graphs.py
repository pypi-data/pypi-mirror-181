import matplotlib.pyplot
import networkx


class Graph:
    def __init__(self, name=None):
        self.name = None
        self.nodes = dict()
        self.edges = dict()

    def add_node(self, node, id_=None, **attributes):
        if (node, id_) in self.nodes.keys():
            raise ValueError(f"Graph already contains a node {node}:{id_}")
        self.nodes[(node, id_)] = attributes

    def add_edge(self, node1, node2, id_=None, **attributes):
        if (node1, node2, id_) in self.edges.keys():
            raise ValueError(f"Graph already contains an edge {node1}:{node2}:{id_}")
        self.edges[(node1, node2, id_)] = attributes

    def set_node_attributes(self, node, id_=None, **attributes):
        self.nodes[(node, id_)].update(attributes)

    def set_edge_attributes(self, node1, node2, id_=None, **attributes):
        self.edges[(node1, node2, id_)].update(attributes)

    def show(self):
        raise NotImplementedError


class NXGraph(Graph):
    def __init__(self, name):
        super().__init__(name)

    def _create_nxgraph_and_layout(self, prog="neato"):
        nx_graph = networkx.DiGraph()

        for node, attributes in self.nodes.items():
            node, id_ = node
            nx_graph.add_node(node)

        weights = dict()
        for edge, attributes in self.edges.items():
            node1, node2, id_ = edge
            if "weight" in attributes.keys():
                weights[(node1, node2)] = attributes["weight"]
            nx_graph.add_edge(node1, node2)

        positions = networkx.nx_agraph.graphviz_layout(nx_graph, prog=prog)

        return nx_graph, positions, weights

    def _matplotlib_draw(self, ax=None, layout_prog="neato"):
        nx_graph, positions, weights = self._create_nxgraph_and_layout(prog=layout_prog)

        labels = networkx.draw_networkx_labels(nx_graph, positions, ax=ax)
        for _, label in labels.items():
            label.set_fontsize("x-small")
            label.set_in_layout(True)
            label.set_bbox(dict(facecolor="skyblue", alpha=0.1))

        edge_labels = networkx.draw_networkx_edge_labels(nx_graph, positions, edge_labels=weights, rotate=False, ax=ax)
        for _, edge_label in edge_labels.items():
            edge_label.set_fontsize("xx-small")

        networkx.draw_networkx_edges(nx_graph, positions, edge_color="blue", alpha=0.15, width=2, arrows=True, arrowsize=10, node_shape="s", node_size=1000, min_source_margin=10, min_target_margin=30, connectionstyle="arc3", ax=ax)

    def show(self, layout_prog="neato"):
        self._matplotlib_draw(layout_prog=layout_prog)
        matplotlib.pyplot.show()

    def plot_onto(self, ax, layout_prog="neato"):
        self._matplotlib_draw(ax=ax, layout_prog=layout_prog)
