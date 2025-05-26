from rest_framework import serializers
# from rest_framework.mixins import
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from comments.models import TopComment, NestedComment


general_fields = ('id', 'user_name', 'home_page', 'time_create', 'text', 'nested_comments')


class _BaseCommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        required=True, max_length=5000, allow_blank=True
    )
    user_name = serializers.CharField(
        required=True, max_length=30
    )
    nested_comments = serializers.SerializerMethodField()

    def get_nested_comments(self, obj):

        # >> > qs = NestedComment.tree(20)
        # >> > qs_list = list(qs)
        # >> > ser = ncs(qs_list[0], context={'req_qs': qs_list})
        # >> > ser.data

        req_qs: list = self.context.get('req_qs')

        # print(obj, self.context, obj.nested_comments)
        return NestedCommentSerializers(
            # obj.nested_comments.all(),
            [instance for instance in req_qs if getattr(instance, 'parent_comment_id', None) == obj.pk],
            many=True,
            read_only=True,
            context=self.context
        ).data if obj.nested_comments else None


class TopCommentSerializers(_BaseCommentSerializer):
    class Meta:
        model = TopComment
        fields = general_fields


class NestedCommentSerializers(_BaseCommentSerializer):
    class Meta:
        model = NestedComment
        fields = general_fields + ('parent_comment_id', )



# from comments.api.serializers import TopCommentSerializers as tcs, NestedCommentSerializers as ncs


# qs = NestedComment.tree(8)
# obj = qs.get(pk=8)
# qs.filter(nestedcomment__parent_comment_id=8)
