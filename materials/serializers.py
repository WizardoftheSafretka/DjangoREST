from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from materials.models import Course, Lesson, Subscribe
from materials.validators import validate_forbidden_word


class CourseBaseSerializer(ModelSerializer):
    url = serializers.CharField(validators=[validate_forbidden_word])

    class Meta:
        model = Course
        fields = ['id', 'title', 'review', 'description']


class SubscribeSerializer(ModelSerializer):
    course = CourseBaseSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Subscribe
        fields = ['id', 'course', 'user', 'is_subscribe']


class LessonSerializer(ModelSerializer):
    url = serializers.CharField(validators=[validate_forbidden_word])
    course = CourseBaseSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('owner',)


class CourseSerializer(ModelSerializer):
    url = serializers.CharField(validators=[validate_forbidden_word])
    lessons_count = SerializerMethodField()
    lessons = SerializerMethodField()
    is_subscribed = SerializerMethodField()
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'review', 'description', 'lessons_count',
                  'lessons', 'is_subscribed', 'owner']
        read_only_fields = ('owner',)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_lessons(self, obj):
        lessons = obj.lessons.all()
        return LessonSerializer(lessons, many=True).data

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscribe.objects.filter(
                course=obj,
                user=request.user,
                is_subscribe=True
            ).exists()
        return False