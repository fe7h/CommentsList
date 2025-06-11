from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
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


class BaseCommentChildAdmin(PolymorphicChildModelAdmin):
    readonly_fields = (
        'media_data',
        'user_data',
        'nested_comments',
    )

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

    def media_data(self, obj):
        attached_media = obj.attached_media
        field = link_to_obj(attached_media)
        if isinstance(attached_media, AttachedImage):
            field += '<br>' + AttachedImageAdmin.img(self, attached_media)
        return format_html(field)

    def has_module_permission(self, request):
        return False


@admin.register(TopComment)
class TopCommentAdmin(BaseCommentChildAdmin):
    base_model = TopComment


@admin.register(NestedComment)
class NestedCommentAdmin(BaseCommentChildAdmin):
    base_model = NestedComment

    readonly_fields = (
        'parent_comment',
        *BaseCommentChildAdmin.readonly_fields,
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


class AttachedMediaChildAdmin(PolymorphicChildModelAdmin):
    list_display = (
        'id',
        'data',
    )
    readonly_fields = (
        'data',
        'comment',
    )


@admin.register(AttachedFile)
class AttachedFileAdmin(AttachedMediaChildAdmin):
    base_model = AttachedFile


@admin.register(AttachedImage)
class AttachedImageAdmin(AttachedMediaChildAdmin):
    base_model = AttachedImage

    list_display = (
        'id',
        'img',
    )

    readonly_fields = (
        *AttachedMediaChildAdmin.readonly_fields,
        'img',
    )

    def img(self, obj):
        return format_html('<img src="{}"/>', obj.data.url)
