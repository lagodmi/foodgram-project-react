from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """ "
    Пагинация по параметру 'limit'.
    """

    page_size_query_param = "limit"
