from rest_framework import serializers

from online_education.models import Course, Lesson, Subscription
from online_education.validators import LinkValidator


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    validators = [
        LinkValidator(link='video_link'),
    ]

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField(source='subscription_course', read_only=True)

    def get_subscription(self, instance):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user).filter(course=instance).exists()

    class Meta:
        model = Course
        fields = "__all__"

    @staticmethod
    def get_lessons_count(obj):
        return obj.lessons.count()



