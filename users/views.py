from django.utils import timezone

from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from online_education.models import Course
from online_education.services import create_payment_link
from online_education.serializers import CourseSerializer
from users.models import Payment, User
from users.serializers import UserSerializer, PaymentSerializer


class PaymentListAPIView(ListAPIView):
    """Вывод платежей."""
    serializer_class = CourseSerializer
    queryset = Payment.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("date",)


class PaymentCreateAPIView(CreateAPIView):
    """Создание платежа."""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        course = Course.objects.get(pk=self.request.data['paid_course'])
        price_id = course.price_id
        serializer.save(payment_url=create_payment_link(price_id))


class RegistrationAPIView(CreateAPIView):
    """Регистрация пользователя."""
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()




