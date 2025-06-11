from ._common import *


class TopCommentSerializers(BaseCommentSerializer):
    class Meta:
        model = TopComment
        fields = COMMON_FIELDS

        read_only_fields = READ_ONLY_FIELDS
        extra_kwargs = {
            **WRITE_ONLY_FIELDS
        }


class NestedCommentSerializers(BaseCommentSerializer):
    parent_comment_id = serializers.IntegerField()

    def validate_parent_comment_id(self, value):
        if not BaseComment.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Object does not exist")
        return value

    class Meta:
        model = NestedComment
        fields = COMMON_FIELDS + ('parent_comment_id', )

        read_only_fields = READ_ONLY_FIELDS
        extra_kwargs = {
            **WRITE_ONLY_FIELDS
        }


class CommentPolymorphicSerializer(RawRepresentationPolymorphicSerializer):
    model_serializer_mapping = {
        TopComment: TopCommentSerializers,
        NestedComment: NestedCommentSerializers
    }
