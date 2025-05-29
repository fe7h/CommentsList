from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from .models import *


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
    list_display = ('id', 'time_create', 'user_name', 'email', 'file', 'parent_comment')

    @staticmethod
    def parent_comment(obj):
        return getattr(obj.get_real_instance(), 'parent_comment_id', 'Top')

    @staticmethod
    def file(obj):
        return bool(obj.attached_media)
