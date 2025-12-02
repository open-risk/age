from django.db import models
import networkx as nx


# We use the networkx multidigraph
# https://networkx.org/documentation/latest/reference/classes/multidigraph.html#networkx.MultiDiGraph

class Entity(models.Model):
    label = models.CharField(max_length=255, null=True, blank=True, db_index=True, help_text='Entity Label')

    def store_networkx_graph(self, nx_graph):

        # get and store all nodes of the graph
        for account, data in nx_graph.nodes(data=True):
            dj_account = Account.objects.create(label=account, graph=self)
            dj_account.save()

        # get and store all edges of the graph
        for u, v, k, d in nx_graph.edges(keys=True, data=True):
            dj_u = Account.objects.get(label=u, graph=self)
            dj_v = Account.objects.get(label=v, graph=self)
            dj_edge = Transaction.objects.create(label=k, graph=self, weight=d['weight'].tolist(), source=dj_u, target=dj_v)
            dj_edge.save()

    def get_networkx_graph(self):
        """
        Compile accounts and transactions into a networkx_graph
        :return:
        """
        graph = nx.MultiDiGraph()

        # get all accounts of the graph
        accounts = self.account_set.all()
        for account in accounts:
            graph.add_node(account.label)

        # get all transactions of the graph
        transactions = self.transaction_set.all()
        for transaction in transactions:
            graph.add_edge(transaction.source.label, transaction.target.label, key=transaction.label,
                           weight=transaction.weight)

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
