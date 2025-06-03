from rest_framework import serializers
from rest_framework.fields import empty

from rest_polymorphic.serializers import PolymorphicSerializer

from comments.models import AttachedMedia, AttachedFile, AttachedImage


class AutoMappingPolymorphicSerializer(PolymorphicSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop(self.resource_type_field_name)
        return ret

    def to_resource_type(self, model_or_instance):
        return model_or_instance._meta.object_name.lower()

    def run_validation(self, data=empty):
        if self.allow_null and data is empty:
            return None
        return super().run_validation(data)


class AttachedMediaSerializers(serializers.ModelSerializer):
    pass


class AttachedFileSerializers(AttachedMediaSerializers):
    class Meta:
        model = AttachedFile
        fields = ('data',)


class AttachedImageSerializers(AttachedMediaSerializers):
    class Meta:
        model = AttachedImage
        fields = ('data',)


class AttachedMediaPolymorphicSerializer(AutoMappingPolymorphicSerializer):
    model_serializer_mapping = {
        AttachedFile: AttachedFileSerializers,
        AttachedImage: AttachedImageSerializers,
    }
