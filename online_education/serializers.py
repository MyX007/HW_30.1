from rest_framework import serializers

from online_education.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    @staticmethod
    def get_lessons_count(obj):
        return obj.lessons.count()

    @staticmethod
    def get_lessons(obj):
        return obj.lessons.all()