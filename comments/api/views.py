from django.db.models import Q

from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from comments.models import BaseComment, TopComment
from .serializers import CommentPolymorphicSerializer, TopCommentSerializers
from .pagination import DefaultCommentPagination


class TopCommentView(viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    queryset = TopComment.objects.all()
    serializer_class = TopCommentSerializers

    pagination_class = DefaultCommentPagination

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['user_name', 'email', 'time_create']


class CommentView(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = BaseComment.objects.all()
    serializer_class = CommentPolymorphicSerializer

    pagination_class = DefaultCommentPagination

    @action(detail=True, methods=('GET',))
    def nested(self, request, pk=None):
        queryset = (self.get_queryset().
                    filter(Q(NestedComment___parent_comment_id=pk))
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
