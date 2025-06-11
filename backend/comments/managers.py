from polymorphic.managers import PolymorphicManager, PolymorphicQuerySet

from django_cte import CTEManager

from utils.managers import RecursiveSelectionManager


class CommentRecursiveSelectionManager(RecursiveSelectionManager):
    parent_model_path = 'comments.BaseComment'
    related_model_path = 'comments.NestedComment'

    parent_field_name = 'parent_comment'

    def queryset_wrapper(self, queryset):
        return PolymorphicQuerySet(
            model=self.parent_model,
            query=queryset.query,
            using=queryset._db
        )


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
