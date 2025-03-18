from django.urls import path

from online_education.apps import OnlineEducationConfig
from rest_framework.routers import DefaultRouter

from online_education.views import (CourseViewSet, LessonListAPIView, LessonCreateAPIView, LessonUpdateAPIView,
                                    LessonRetrieveAPIView, LessonDestroyAPIView)


app_name = OnlineEducationConfig.name

router = DefaultRouter()
router.register('course',
                CourseViewSet,
                basename='course'
                )

urlpatterns = [
    path('', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-destroy'),
] + router.urls

