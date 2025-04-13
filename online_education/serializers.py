from rest_framework import serializers

from online_education.models import Course, Lesson, Subscription
from online_education.validators import LinkValidator
from online_education.services import create_price


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""
    class Meta:
        model = Subscription
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор урока."""
    validators = [
        LinkValidator(link='video_link'),
    ]
    price_id = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = "__all__"

    @staticmethod
    def get_price_id(obj):
        return create_price(obj)


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса."""
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField(source='subscription_course', read_only=True)

    def get_subscription(self, instance):
        """Получение данных о наличии подписки на конкретный курс."""
        user = self.context['request'].user
        return Subscription.objects.filter(user=user).filter(course=instance).exists()

    class Meta:
        model = Course
        fields = "__all__"

    @staticmethod
    def get_lessons_count(obj):
        """Получение количества уроков конкретного курса"""
        return obj.lessons.count()



