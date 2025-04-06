from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from online_education.serializers import CourseSerializer
from users.models import Payment, User
from users.serializers import UserSerializer


class PaymentListAPIView(ListAPIView):
    serializer_class = CourseSerializer
    queryset = Payment.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("date",)


class RegistrationAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
