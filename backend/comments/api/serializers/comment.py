from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from drf_recaptcha.fields import ReCaptchaV2Field

from comments.models import TopComment, NestedComment, BaseComment, UserData

from .attached_media import AttachedFileSerializers, AttachedMediaPolymorphicSerializer

COMMON_FIELDS = (
    'id',
    'user_name',
    'home_page',
    'email',
    'time_create',
    'text',
    'attached_media',
    'user_data',
)
READ_ONLY_FIELDS = ('time_create',)
WRITE_ONLY_FIELDS = {
    'user_data': {'write_only': True},
}


class BaseCommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        required=True, max_length=5000, allow_blank=True
    )
    user_name = serializers.CharField(
        required=True, max_length=30
    )
    attached_media = AttachedMediaPolymorphicSerializer(required=False, allow_null=True, default=None)
    user_data = serializers.JSONField(required=False, allow_null=True, default=None, write_only=True)

    def create(self, validated_data):
        if attached_media_data := validated_data.pop('attached_media'):
            attached_media_serializer = AttachedMediaPolymorphicSerializer(data=attached_media_data)
            attached_media_serializer.is_valid(raise_exception=True)
            attached_media_obj = attached_media_serializer.save()
            validated_data['attached_media'] = attached_media_obj
        if user_data := validated_data.pop('user_data'):
            user_data_obj, _ = UserData.objects.get_or_create(**user_data)
            validated_data['user_data'] = user_data_obj

        comment_model = self.Meta.model
        comment = comment_model.objects.create(**validated_data)

        return comment


class RawRepresentationPolymorphicSerializer(PolymorphicSerializer):
    recaptcha = ReCaptchaV2Field()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop(self.resource_type_field_name)
        return ret

    def to_resource_type(self, model_or_instance):
        return model_or_instance._meta.object_name.lower()

    def is_valid(self, *args, **kwargs):
        result = super().is_valid(*args, **kwargs)

        recaptcha_field = self.fields.get('recaptcha')
        recaptcha_value = self.initial_data.get('recaptcha')
        recaptcha_field.run_validation(recaptcha_value)

        return result


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
