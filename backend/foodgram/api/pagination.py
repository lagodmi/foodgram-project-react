from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """"
    Пагинация по параметру 'limit'.
    """
    page_size_query_param = 'limit'


# Может понадобиться.
class CustomPaginationForSubscribe(PageNumberPagination):
    """
    Пагинация рецептов в подписке.
    """
    page_size_query_param = 'recipes_limit'
