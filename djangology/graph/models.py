from django.db import models

from django.db import models

class Node(models.Model):
    """
    Graph node (vertex).
    """
    label = models.CharField(max_length=255, blank=True, db_index=True)

    def __str__(self):
        return self.label or f"Node {self.pk}"

    class Meta:
        indexes = [
            models.Index(fields=["label"]),
        ]


class Edge(models.Model):
    """
    Directed multiedge
    """
    label = models.CharField(
        max_length=100,
        blank=True,
        help_text="label to distinguish parallel edges",
        db_index=True,
    )
    source = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name="out_edges",
        db_index=True,
    )
    target = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name="in_edges",
        db_index=True,
    )
    weight = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        k = f" ({self.label})" if self.label else ""
        return f"{self.source} -> {self.target}{k}"

    class Meta:
        indexes = [
            models.Index(fields=["source", "target"]),
            models.Index(fields=["target", "source"]),
            models.Index(fields=["label"]),
        ]

