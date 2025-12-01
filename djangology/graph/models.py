from django.db import models
import networkx as nx


# We use the networkx multidigraph
# https://networkx.org/documentation/latest/reference/classes/multidigraph.html#networkx.MultiDiGraph

class Entity(models.Model):
    label = models.CharField(max_length=255, null=True, blank=True, db_index=True, help_text='Entity Label')

    def store_networkx_graph(self, nx_graph):

        # get and store all nodes of the graph
        for node, data in nx_graph.nodes(data=True):
            dj_node = Account.objects.create(label=node, graph=self)
            dj_node.save()

        # get and store all edges of the graph
        for u, v, k, d in nx_graph.edges(keys=True, data=True):
            dj_u = Account.objects.get(label=u)
            dj_v = Account.objects.get(label=v)
            dj_edge = Transaction.objects.create(label=d['label'], graph=self, weight=d['weight'].tolist(), source=dj_u,
                                                 target=dj_v)
            dj_edge.save()

    def get_networkx_graph(self):
        """
        Compile accounts and transactions into a networkx_graph
        :return:
        """
        graph = nx.MultiDiGraph()

        # get all nodes of the graph
        nodes = self.node_set.all()
        for node in nodes:
            graph.add_node(node.label)

        # get all edges of the graph
        edges = self.edge_set.all()
        for edge in edges:
            graph.add_edge(edge.source.label, edge.target.label, label=edge.label, weight=edge.weight)

        return graph


class Account(models.Model):
    """
    Graph node (vertex).
    """
    label = models.CharField(max_length=255, blank=True, db_index=True, help_text='Account Label')
    graph = models.ForeignKey(Entity, null=True, blank=True, on_delete=models.CASCADE,
                              help_text='Entity to which the Account belongs')

    def __str__(self):
        return self.label or f"Node {self.pk}"

    class Meta:
        indexes = [
            models.Index(fields=["label"]),
        ]


class Transaction(models.Model):
    """
    Directed edge with vector weights
    """
    label = models.CharField(
        max_length=100,
        blank=True,
        help_text="edge label",
        db_index=True,
    )
    graph = models.ForeignKey(Entity, null=True, blank=True, on_delete=models.CASCADE,
                              help_text='Entity to which the Transaction belongs')

    source = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="out_edges",
        help_text="the source account of the transaction",
        db_index=True,
    )
    target = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        help_text="the target account of the transaction",
        related_name="in_edges",
        db_index=True,
    )
    weight = models.JSONField(null=True, blank=True, help_text="The vector of weights associated with the transaction")

    def __str__(self):
        k = f" ({self.label})" if self.label else ""
        return f"{self.source} -> {self.target}{k}"

    class Meta:
        indexes = [
            models.Index(fields=["source", "target"]),
            models.Index(fields=["target", "source"]),
            models.Index(fields=["label"]),
        ]
