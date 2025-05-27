from django.db.models import Q

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from comments.models import BaseComment
from .serializers import CommentPolymorphicSerializer


class CommentView(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = CommentPolymorphicSerializer
    queryset = BaseComment.objects.all()

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
