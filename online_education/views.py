from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny

from online_education.models import Course, Lesson
from online_education.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)

        elif self.action == "destroy":
            self.permission_classes = (IsOwner, ~IsModer)

        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsModer | IsOwner]

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = (~IsModer,)
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsModer | IsOwner]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsModer, IsOwner)
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (~IsModer, IsOwner)
    queryset = Lesson.objects.all()
