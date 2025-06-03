from rest_framework.pagination import PageNumberPagination, CursorPagination


class DefaultCommentPagination(PageNumberPagination):
    page_size = 25


class CommentCursorPagination(CursorPagination):
    page_size = 3
    ordering = '-time_create'
