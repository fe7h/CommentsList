from django.db import models

from polymorphic.models import PolymorphicModel

from .managers import CommentManagersMixin


# class UserData(models.Model):
#     pass
# модель с наборм данных с запроса пользователя(юзерагент апи и тд) и уникальным хешем на их основе

# attached_media
# class AttachedFile(models.Model):
#     pass
#
#
# class AttachedImage(models.Model):
#     pass


class BaseComment(CommentManagersMixin, PolymorphicModel):
    time_create = models.DateTimeField(auto_now_add=True)
    # user_data = models.ForeignKey(
    #         UserData,
    #         on_delete=models.PROTECT,
    #         related_name='comments',
    #     )

    user_name = models.CharField(max_length=30)
    email = models.EmailField()
    home_page = models.URLField(blank=True)
    text = models.TextField(max_length=5000)


class TopComment(BaseComment):
    pass


class NestedComment(BaseComment):
    parent_comment = models.ForeignKey(
        BaseComment,
        on_delete=models.CASCADE,
        related_name='nested_comments',
        blank=True
    )
