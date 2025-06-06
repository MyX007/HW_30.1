from django.urls import path
from rest_framework.routers import DefaultRouter

from online_education.apps import OnlineEducationConfig
from online_education.views import (CourseViewSet, LessonCreateAPIView,
                                    LessonDestroyAPIView, LessonListAPIView,
                                    LessonRetrieveAPIView, LessonUpdateAPIView,
                                    SubscriptionUpdateAPIView)

app_name = OnlineEducationConfig.name

router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="course")

urlpatterns = [
    path("", LessonListAPIView.as_view(), name="lesson-list"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-detail"),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lessons/", LessonListAPIView.as_view(), name="lesson-list"),
    path(
        "lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson-update"
    ),
    path(
        "lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson-destroy"
    ),
    path("subscription/", SubscriptionUpdateAPIView.as_view(), name="subscription-check"),
] + router.urls
