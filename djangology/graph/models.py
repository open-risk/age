from django.db import models
from taggit.managers import TaggableManager
import networkx as nx


# We use the networkx multidigraph
# https://networkx.org/documentation/latest/reference/classes/multidigraph.html#networkx.MultiDiGraph

class Entity(models.Model):
    identity = models.CharField(max_length=255, unique=True, db_index=True, help_text='Entity Identity')

    def store_networkx_graph(self, nx_graph):

        # get and store all nodes (accounts) of the graph
        for account, data in nx_graph.nodes(data=True):
            dj_account = Account.objects.create(identity=account, graph=self)
            dj_account.save()
            if data['tag']:
                dj_account.tags.add(data['tag'])

        # get and store all edges of the graph
        for u, v, key, data in nx_graph.edges(keys=True, data=True):
            dj_u = Account.objects.get(identity=u, graph=self)
            dj_v = Account.objects.get(identity=v, graph=self)
            dj_edge = Transaction.objects.create(identity=key, graph=self, weight=data['weight'].tolist(), source=dj_u, target=dj_v)
            dj_edge.save()
            if data['tag']:
                dj_edge.tags.add(data['tag'])

    def get_networkx_graph(self):
        """
        Compile accounts and transactions into a networkx_graph
        :return:
        """
        graph = nx.MultiDiGraph()

        # get all accounts of the graph
        accounts = self.account_set.all()
        for account in accounts:
            tags = [tag.name for tag in account.tags.all()]
            graph.add_node(account.identity, tags=tags)

        # get all transactions of the graph
        transactions = self.transaction_set.all()
        for transaction in transactions:
            tags = [tag.name for tag in transaction.tags.all()]
            graph.add_edge(transaction.source.identity, transaction.target.identity, key=transaction.identity, weight=transaction.weight, tags=tags)

        return graph

    def __str__(self):
        return f"{self.identity}"

    class Meta:
        verbose_name = "Entity"
        verbose_name_plural = "Entities"


class Account(models.Model):
    """
    Graph node (vertex).
    """
    identity = models.CharField(max_length=255, unique=True, db_index=True, help_text='Account Identity')

    tags = TaggableManager()

    # TODO provisionally blanks allowed but don't make sense
    graph = models.ForeignKey(Entity, null=True, blank=True, on_delete=models.CASCADE,
                              help_text='Entity to which the Account belongs')

    def __str__(self):
        return f"{self.graph.identity} : {self.identity} ({self.pk})"

    class Meta:
        indexes = [
            models.Index(fields=["identity"]),
        ]

        verbose_name = "Account"
        verbose_name_plural = "Accounts"


class Transaction(models.Model):
    """
    Directed edge with vector weights
    """
    identity = models.CharField(
        max_length=100,
        unique=True,
        help_text="Transaction Identity",
        db_index=True,
    )

    tags = TaggableManager()

    # TODO provisionally blanks allowed but don't make sense
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
        return f"{self.graph.identity} : {self.source} -> {self.target}{self.identity}"

    class Meta:
        indexes = [
            models.Index(fields=["source", "target"]),
            models.Index(fields=["target", "source"]),
            models.Index(fields=["identity"]),
        ]

        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
