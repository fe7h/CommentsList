from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from comments.models import TopComment, NestedComment, BaseComment


COMMON_FIELDS = ('id', 'user_name', 'home_page', 'email', 'time_create', 'text')
READ_ONLY_FIELDS = ('time_create',)
WRITE_ONLY_FIELDS = {
    'email': {'write_only': True},
}


class BaseCommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        required=True, max_length=5000, allow_blank=True
    )
    user_name = serializers.CharField(
        required=True, max_length=30
    )


class RawRepresentationPolymorphicSerializer(PolymorphicSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop(self.resource_type_field_name)
        return ret

    def to_resource_type(self, model_or_instance):
        return model_or_instance._meta.object_name.lower()
