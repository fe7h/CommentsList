from django.db import models
from django.core.validators import FileExtensionValidator

from polymorphic.models import PolymorphicModel

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from .managers import CommentManagersMixin
from .validators import validate_file_size


# class UserData(models.Model):
#     pass
# модель с наборм данных с запроса пользователя(юзерагент апи и тд) и уникальным хешем на их основе

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
    # user_data = models.ForeignKey(
    #         UserData,
    #         on_delete=models.PROTECT,
    #         related_name='comments',
    #     )
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


class TopComment(BaseComment):
    pass


class NestedComment(BaseComment):
    parent_comment = models.ForeignKey(
        BaseComment,
        on_delete=models.CASCADE,
        related_name='nested_comments',
        blank=True
    )
