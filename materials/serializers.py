from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson, Subscribe
from materials.validators import validate_forbidden_word


class CourseBaseSerializer(ModelSerializer):
    title = serializers.CharField(validators=[validate_forbidden_word])

    class Meta:
        model = Course
        fields = ['id', 'title', 'review', 'description']


class LessonSerializer(ModelSerializer):
    title = serializers.CharField(validators=[validate_forbidden_word])
    course = CourseBaseSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('owner',)


class CourseSerializer(ModelSerializer):
    title = serializers.CharField(validators=[validate_forbidden_word])
    lessons_count = SerializerMethodField()
    lessons = SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'review', 'description', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_lessons(self, obj):
        lessons = obj.lessons.all()
        return LessonSerializer(lessons, many=True).data  # ✅ Теперь это безопасно


class SubscribeSerializer(ModelSerializer):
    course = CourseBaseSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Subscribe
        fields = ['id', 'course', 'user', 'is_subscribe']