from rest_framework.pagination import CursorPagination


class CreatedAtBasedCursorPagination(CursorPagination):
    ordering = "-created_at"
    page_size_query_param = "page_size"
