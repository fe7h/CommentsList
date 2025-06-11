from typing import Callable

from django.db import models
from django.db.models.query import QuerySet
from django.apps import apps

from django_cte import With


class RecursiveSelectionManager(models.Manager):
    """Returns QuerySets with parent and all of its children.

    Model must have CTEManager as cte_objects class attribute.

    Also works with PolymorphicModel where child -> base:
        parent_model_path (str): Path to base model
        related_model_path (str): Model which have related field with base model
        parent_field_name (str): Name of related field in related_model

    Usage:
        Model.this_manager(root_pk).all()
    """

    parent_model_path: str = None
    related_model_path: str = None

    parent_field_name: str = None

    def __call__(self, root_pk):
        return self.get_queryset(self._make_cte(root_pk))

    @property
    def parent_model(self) -> models.Model:
        return apps.get_model(self.parent_model_path or self.model)

    @property
    def nested_model(self) -> models.Model:
        return apps.get_model(self.related_model_path or self.model)

    def get_queryset(self, make_cte: Callable = None) -> QuerySet:
        """
        Args:
            make_cte (Callable): Function which return cte

        Returns:
            queryset (QuerySet): Consists of a parent and all of its children
        """
        if not make_cte:
            raise Exception('You must call this manager with root object pk')

        cte = With.recursive(make_cte)

        queryset = cte.join(
            self.parent_model.cte_objects.all(),
            id=cte.col.id
        ).with_cte(cte)

        return self.queryset_wrapper(queryset)

    def queryset_wrapper(self, queryset: QuerySet) -> QuerySet:
        return queryset

    def _make_cte(self, root_pk: int) -> Callable[[With], With]:
        """Generated make_cte func with a given pk"""
        def inner(cte):
            return (
                self.model.cte_objects.filter(pk=root_pk).values('id')
                .union(
                    cte.join(
                        self.nested_model,
                        **{self.parent_field_name: cte.col.id}
                    ).values('id'),
                    all=True
                )
            )
        return inner
