from rest_framework.pagination import PageNumberPagination


class CourseAndLessonPaginator(PageNumberPagination):
    """Пагинация страниц уроков и курсов."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100