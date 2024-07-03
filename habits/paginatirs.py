from rest_framework.pagination import PageNumberPagination


class HabitPaginator(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"


class RewardPaginator(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
