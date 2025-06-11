from ._common import *

COMMON_FIELDS += ('nested_comments', )

# возращает все связаные обекты одним запросом к бд
class _FullNestetSerializer(BaseCommentSerializer):

    nested_comments = serializers.SerializerMethodField()

    def get_nested_comments(self, obj):

        # >> > qs = NestedComment.tree(20)
        # >> > qs_list = list(qs)
        # >> > ser = ncs(qs_list[0], context={'req_qs': qs_list})
        # >> > ser.data

        req_qs: list = self.context.get('req_qs')

        return _NestedCommentSerializers(
            [instance for instance in req_qs if getattr(instance, 'parent_comment_id', None) == obj.pk],
            many=True,
            read_only=True,
            context=self.context
        ).data if obj.nested_comments else None


class _TopCommentSerializers(BaseCommentSerializer):
    class Meta:
        model = TopComment
        fields = COMMON_FIELDS


class _NestedCommentSerializers(BaseCommentSerializer):
    class Meta:
        model = NestedComment
        fields = COMMON_FIELDS + ('parent_comment_id', )


class CommentFullNestedSerializer(RawRepresentationPolymorphicSerializer):
    # на вход принимает объект вершины дерева и кверисет после .tree преабразованый в лист
    model_serializer_mapping = {
        TopComment: _TopCommentSerializers,
        NestedComment: _NestedCommentSerializers
    }

# qs = NestedComment.tree(8)
# obj = qs.get(pk=8)
# qs.filter(nestedcomment__parent_comment_id=8)
