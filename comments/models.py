from django.db import models

from polymorphic.models import PolymorphicModel
from django_cte import CTEManager

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

from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager
#
# class MyModel(PolymorphicModel):
#     objects = PolymorphicManager()  # обязательно!
#     cte = CTEManager()

from django.db.models import IntegerField, TextField
from django.db.models.expressions import (
    Case,
    Exists,
    ExpressionWrapper,
    F,
    OuterRef,
    Q,
    Value,
    When,
)
from django.db.models.functions import Concat
from django.db.utils import DatabaseError
from django.test import TestCase

from django_cte import With
# >>> from comments.models import test


# def rec_q_test():
#     def make_cte(cte):
#         base = TopComment.objects.all().union(
#             cte.join(BaseComment, nested_comments=cte.col.id).all(),
#             all=True,
#         )
#         return base
#
#     cte = With.recursive(make_cte)
#
#     q = cte.join(TopComment.objects.all())
#
#     return q.with_cte(cte)

# def test():
#     def make_cte(cte):
#         return TopComment.objects.all(
#         ).values(
#             "nested_comments",
#         ).union(
#             # recursive union: get descendants
#             cte.join(NestedComment, parent_comment_id=cte.col.nested_comments).values(
#                 "nested_comments",
#             ),
#             all=True,
#         )
#
#     cte = With.recursive(make_cte)
#
#     q = cte.join(NestedComment, parent_comment_id=cte.col.nested_comments).with_cte(cte)
#
#     return q

def test():
    def make_cte(cte):
        return BaseComment.cte_objects.all(
        ).values(
            "nested_comments",
        ).union(
            # recursive union: get descendants
            cte.join(NestedComment, parent_comment_id=cte.col.nested_comments).values(
                "nested_comments",
            ),
            all=True,
        )

    cte = With.recursive(make_cte)

    q = cte.join(NestedComment.cte_objects.all(), parent_comment_id=cte.col.nested_comments).with_cte(cte)

    return q

# <CTEQuerySet [{'id': 33}, {'id': 9}, {'id': 10}, {'id': 15}, {'id': 16}, {'id': 23}, {'id': 35}, {'id': 14}, {'id': 27}, {'id': 21}, {'id': 22}, {'id': 40}, {'id': 30}, {'id': 32}]>

class Test(models.Manager):

    make_cte = None

    def __call__(self, pk):
        self.make_cte = self._make_cte(pk)
        return self

    def get_queryset(self):
        if not self.make_cte:
            raise Exception
        queryset = self.placeholder()
        del self.make_cte
        return queryset

    def placeholder(self):
        cte = With.recursive(self.make_cte)

        queryset = cte.join(
            NestedComment.cte_objects.all(), #<====================================
            parent_comment_id=cte.col.nested_comments
        ).with_cte(cte)

        return queryset

    def _make_cte(self, pk):
        def inner(cte):
            print(self.model)
            return self.model.cte_objects.filter(pk=pk).values('nested_comments').union(#<====================================
                cte.join(
                    NestedComment,
                    parent_comment_id=cte.col.nested_comments
                ).values('nested_comments'),
                all=True
            )
        return inner


class CommentPlaceholderMixin:

    objects = PolymorphicManager()
    cte_objects = CTEManager()
    cool = Test()


class BaseComment(CommentPlaceholderMixin, PolymorphicModel):
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
