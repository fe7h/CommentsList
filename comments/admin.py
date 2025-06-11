from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db.models import Q

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from .models import *
from utils.admin import InputFilter, link_to_obj


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
        return None


COMMON_READONLY_FIELDS = (
    'user_data',
    'nested_comments',
)


class BaseCommentChildAdmin(PolymorphicChildModelAdmin):
    readonly_fields = COMMON_READONLY_FIELDS

    def nested_comments(self, obj):
        queryset = (BaseComment.objects.
                    filter(Q(NestedComment___parent_comment_id=obj.pk))
        )
        return mark_safe('<br>'.join(
            map(
                lambda x: link_to_obj(x, 'basecomment'),
                queryset
            )
        ))

    nested_comments.short_description = mark_safe('First level<br>nested comments')

    def has_module_permission(self, request):
        return False


@admin.register(TopComment)
class TopCommentAdmin(BaseCommentChildAdmin):
    base_model = TopComment


@admin.register(NestedComment)
class ModelCAdmin(BaseCommentChildAdmin):
    base_model = NestedComment

    readonly_fields = (
        'parent_comment',
        *COMMON_READONLY_FIELDS,
    )


@admin.register(BaseComment)
class BaseCommentParentAdmin(PolymorphicParentModelAdmin):
    base_model = BaseComment
    child_models = (TopComment, NestedComment)

    list_per_page = 20
    list_display = (
        'id',
        'time_create',
        'user_name',
        'email',
        'attached_media',
        'parent_comment',
        'linked_user_data',
    )
    search_fields = (
        'user_name',
        'email',
    )
    list_filter = [NestedCommentsFilter]

    def parent_comment(self, obj):
        return link_to_obj(
            obj.get_real_instance(),
            representation=lambda obj: getattr(obj, 'parent_comment_id', 'Top')
        )

    def linked_user_data(self, obj):
        return mark_safe(link_to_obj(user_data)) if (user_data := obj.user_data) else None

    linked_user_data.short_description = 'USER DATA'


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'short_user_hash',
        'user_agent',
        'platform',
        'language',
        'timezone_offset',
    )

    readonly_fields = (
        'user_hash',
        'user_agent',
        'screen_resolution',
        'color_depth',
        'language',
        'timezone_offset',
        'cookie_enabled',
        'plugins',
        'canvas_fp',
        'webgl_fp',
        'device_memory',
        'platform',
        'created_at',
        'comments',
    )

    def short_user_hash(self, obj):
        return str(obj)

    short_user_hash.short_description = 'USER HASH'

    def comments(self, obj):
        return mark_safe('<br>'.join(
            map(
                lambda x: link_to_obj(x, 'basecomment'),
                obj.comments.all()
            )
        ))
