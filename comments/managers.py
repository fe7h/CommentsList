from django.db import models

from polymorphic.managers import PolymorphicManager

from django_cte import With, CTEManager


def laze_load():
    from .models import NestedComment
    return NestedComment


class CommentRecursiveSelectionManager(models.Manager):

    make_cte = None

    def __call__(self, pk):
        self.make_cte = self._make_cte(pk)
        return self

    def get_queryset(self):
        if not self.make_cte:
            raise Exception
        queryset = self.name_placeholder()
        del self.make_cte
        return queryset

    def name_placeholder(self):
        cte = With.recursive(self.make_cte)

        queryset = cte.join(
            laze_load().cte_objects.all(),
            parent_comment_id=cte.col.nested_comments
        ).with_cte(cte)

        return queryset

    def _make_cte(self, pk):
        def inner(cte):
            return self.model.cte_objects.filter(pk=pk).values('nested_comments').union(
                cte.join(
                    laze_load(),
                    parent_comment_id=cte.col.nested_comments
                ).values('nested_comments'),
                all=True
            )
        return inner


class CommentManagersMixin:
    def __init_subclass__(cls, **kwargs):
        managers = {
            'objects': PolymorphicManager,
            'cte_objects': CTEManager,
            'tree': CommentRecursiveSelectionManager,
        }

        for name, manager_cls in managers.items():
            manager = manager_cls()
            setattr(cls, name, manager)
            manager.contribute_to_class(cls, name)
