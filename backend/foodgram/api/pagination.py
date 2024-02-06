from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class CustomPaginationForSubscribe(PageNumberPagination):
    page_size_query_param = 'recipes_limit'
