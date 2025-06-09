from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from drf_recaptcha.fields import ReCaptchaV2Field

from comments.models import TopComment, NestedComment, BaseComment

from .attached_media import AttachedFileSerializers, AttachedMediaPolymorphicSerializer


COMMON_FIELDS = ('id', 'user_name', 'home_page', 'email', 'time_create', 'text', 'attached_media',)
READ_ONLY_FIELDS = ('time_create',)
WRITE_ONLY_FIELDS = {
    # 'email': {'write_only': True},
}


class BaseCommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        required=True, max_length=5000, allow_blank=True
    )
    user_name = serializers.CharField(
        required=True, max_length=30
    )
    attached_media = AttachedMediaPolymorphicSerializer(required=False, allow_null=True, default=None)

    def create(self, validated_data):
        if attached_media_data := validated_data.pop('attached_media'):
            attached_media_serializer = AttachedMediaPolymorphicSerializer(data=attached_media_data)
            attached_media_serializer.is_valid(raise_exception=True)
            attached_media_obj = attached_media_serializer.save()
            validated_data['attached_media'] = attached_media_obj

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
