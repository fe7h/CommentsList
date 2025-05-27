from ._common import *


class TopCommentSerializers(BaseCommentSerializer):
    class Meta:
        model = TopComment
        fields = COMMON_FIELDS


class NestedCommentSerializers(BaseCommentSerializer):
    class Meta:
        model = NestedComment
        fields = COMMON_FIELDS + ('parent_comment_id', )


class CommentPolymorphicSerializer(RawRepresentationPolymorphicSerializer):
    model_serializer_mapping = {
        TopComment: TopCommentSerializers,
        NestedComment: NestedCommentSerializers
    }

# from comments.api.serializers.comment import CommentPolymorphicSerializer as cps
