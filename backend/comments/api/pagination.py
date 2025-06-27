from rest_framework.pagination import PageNumberPagination, CursorPagination


class DefaultCommentPagination(CursorPagination):
    page_size = 25
    ordering = 'time_create'


class TopCommentPagination(CursorPagination):
    page_size = 25
    ordering = '-time_create'
