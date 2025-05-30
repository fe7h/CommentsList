from django.db import models

from polymorphic.managers import PolymorphicManager, PolymorphicQuerySet

from django_cte import With, CTEManager


def laze_load():
    from .models import NestedComment
    return NestedComment


def laze_load2():
    from .models import BaseComment
    return BaseComment

# qs = TopComment.tree(root_pk=5).all()
# PolymorphicQuerySet(model=BaseComment, query=qs.query, using=qs._db)


# RecursiveChildManager
class CommentRecursiveSelectionManager(models.Manager):
    """
        nested_comments
        'parent_comment'_id
        laze_load() -> NestedComment дочерняя модель что может ссылаться сам на себя
        self.model -> TopComment родительская модель (высшая в звене)

    """

    # make_cte = None

    def __call__(self, root_pk):
        # self.make_cte = self._make_cte(pk)
        return self.get_queryset(self._make_cte(root_pk))

    def get_queryset(self, make_cte=None):
        if not make_cte:
            raise Exception

        cte = With.recursive(make_cte)

        queryset = cte.join(
            laze_load2().cte_objects.all(),
            id=cte.col.id
        ).with_cte(cte)

        queryset = PolymorphicQuerySet(
            model=laze_load2(),
            query=queryset.query,
            using=queryset._db
        )
        # queryset = cte.join(laze_load().cte_objects.all()).with_cte(cte)
        return queryset

    # @staticmethod
    # def name_placeholder(make_cte):
    #     cte = With.recursive(make_cte)
    #
    #     queryset = cte.join(
    #         laze_load().cte_objects.all(),
    #         parent_comment_id=cte.col.nested_comments
    #     ).with_cte(cte)
    #
    #     return queryset

    def _make_cte(self, root_pk):
        def inner(cte):
            return (self.model.cte_objects.filter(pk=root_pk).values('id')
            .union(
                cte.join(
                    laze_load(),
                    parent_comment=cte.col.id
                ).values('id'),
                all=True
            ))
        return inner


class CommentWithMediaManager(PolymorphicManager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('attached_media')


class CommentManagersMixin:
    def __init_subclass__(cls, **kwargs):
        managers = {
            'objects': PolymorphicManager,
            'cte_objects': CTEManager,
            'tree': CommentRecursiveSelectionManager,
            'with_media': CommentWithMediaManager,
        }

        for name, manager_cls in managers.items():
            manager = manager_cls()
            setattr(cls, name, manager)
            manager.contribute_to_class(cls, name)
