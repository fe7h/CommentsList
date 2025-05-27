from rest_framework.pagination import PageNumberPagination


class DefaultCommentPagination(PageNumberPagination):
    page_size = 25
