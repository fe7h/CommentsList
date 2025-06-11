import hashlib

from django.db import models
from django.core.validators import FileExtensionValidator

from polymorphic.models import PolymorphicModel

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from .managers import CommentManagersMixin
from .validators import validate_file_size


class UserData(models.Model):
    user_hash = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        primary_key=True
    )

    user_agent = models.TextField()
    screen_resolution = models.CharField(max_length=20)
    color_depth = models.PositiveSmallIntegerField()
    language = models.CharField(max_length=20)
    timezone_offset = models.CharField(max_length=255)
    cookie_enabled = models.BooleanField()

    plugins = models.TextField(blank=True)

    canvas_fp = models.TextField(blank=True)
    webgl_fp = models.TextField(blank=True)

    device_memory = models.FloatField(null=True, blank=True)
    platform = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        h = hashlib.sha256()

        fields = self._meta.fields
        for field in fields:
            val = str(getattr(self, field.name, None))
            h.update(val.encode('utf-8'))

        self.user_hash = h.hexdigest()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user_hash[:4]}...{self.user_hash[-4:]}'


class AttachedMedia(PolymorphicModel):
    pass


class AttachedFile(AttachedMedia):
    data = models.FileField(
        upload_to='comments/files/',
        validators=[
            FileExtensionValidator(allowed_extensions=['txt']),
            validate_file_size,
        ],
    )


class AttachedImage(AttachedMedia):
    data = ProcessedImageField(
        upload_to='comments/images/',
        processors=[ResizeToFill(320, 240)],
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'gif', 'png'])
        ],
    )


class BaseComment(CommentManagersMixin, PolymorphicModel):
    time_create = models.DateTimeField(auto_now_add=True)
    user_data = models.ForeignKey(
            UserData,
            on_delete=models.PROTECT,
            related_name='comments',
            blank=True,
            null=True,
        )
    user_name = models.CharField(max_length=30)
    email = models.EmailField()
    home_page = models.URLField(blank=True, null=True)
    text = models.TextField(max_length=5000)

    attached_media = models.OneToOneField(
        AttachedMedia,
        on_delete=models.SET_NULL,
        related_name='comment',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.pk}: Create in {self.time_create} by {self.user_name}'


class TopComment(BaseComment):
    pass


class NestedComment(BaseComment):
    parent_comment = models.ForeignKey(
        BaseComment,
        on_delete=models.CASCADE,
        related_name='nested_comments',
        blank=True
    )

    def __str__(self):
        return super().__str__() + f' answer to {self.parent_comment_id}'
