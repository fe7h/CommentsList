from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from .models import *
from utils.admin import InputFilter


class NestedCommentsFilter(InputFilter):
    parameter_name = 'parent_id'
    title = 'nested comments of:'

    def queryset(self, request, queryset):
        if self.value() is not None:
            try:
                pk = int(self.value())
                return BaseComment.tree(root_pk=pk).all()
            except ValueError:
                return queryset


class BaseCommentChildAdmin(PolymorphicChildModelAdmin):
    pass


@admin.register(TopComment)
class TopCommentAdmin(BaseCommentChildAdmin):
    base_model = TopComment


@admin.register(NestedComment)
class ModelCAdmin(BaseCommentChildAdmin):
    base_model = NestedComment


@admin.register(BaseComment)
class BaseCommentParentAdmin(PolymorphicParentModelAdmin):
    base_model = BaseComment
    child_models = (TopComment, NestedComment)
    list_display = (
        'id',
        'time_create',
        'user_name',
        'email',
        'attached_media',
        'parent_comment',
    )
    list_filter = [NestedCommentsFilter]

    @staticmethod
    def parent_comment(obj):
        return getattr(obj.get_real_instance(), 'parent_comment_id', 'Top')
