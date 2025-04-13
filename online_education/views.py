from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status, request
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from online_education.models import Course, Lesson, Subscription
from online_education.paginators import CourseAndLessonPaginator
from online_education.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from online_education.services import create_price
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Вьюсет курсов."""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CourseAndLessonPaginator

    def get_permissions(self):
        """Получение разрешений."""
        if self.action == "create":
            self.permission_classes = (~IsModer,)

        elif self.action == "destroy":
            self.permission_classes = (IsOwner, ~IsModer)

        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsModer | IsOwner]

        return super().get_permissions()

    def perform_create(self, serializer):
        """Назначение владелца."""
        serializer.save(owner=self.request.user, price_id=create_price(
            title=self.request.data["title"],
            description=self.request.data["description"],
            amount=self.request.data["amount"],
        )
                        )



class LessonCreateAPIView(generics.CreateAPIView):
    """Создание урока."""
    permission_classes = (~IsModer,)
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        """Назначение владельца."""
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """Просмотр всех уроков."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CourseAndLessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр одного урока."""
    permission_classes = [IsModer | IsOwner]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Обновление урока."""
    permission_classes = [IsModer | IsOwner]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаление урока."""
    permission_classes = [~IsModer | IsOwner]
    queryset = Lesson.objects.all()


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    """Обновление статуса подписки на курс"""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            status_code = status.HTTP_204_NO_CONTENT
            message = 'Подписка отключена'

        else:
            subs_item.create(
                user=user,
                course=course_item,
            )
            status_code = status.HTTP_201_CREATED
            message = 'Подписка подключена'

        return Response({'message': message}, status=status_code)
