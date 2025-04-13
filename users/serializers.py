from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from online_education.serializers import CourseSerializer
from online_education.services import create_payment_link

from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""
    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор платежей."""

    class Meta:
        model = Payment
        fields = "__all__"




