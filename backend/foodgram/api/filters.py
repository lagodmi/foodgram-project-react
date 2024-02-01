from rest_framework.filters import SearchFilter


class NameFilter(SearchFilter):
    """
    Фильтрация поля name  для ингридиентов.
    """
    search_param = 'name'
