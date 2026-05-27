from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'review', 'description', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_lessons(self, obj):
        lessons = obj.lessons.all()
        return LessonSerializer(lessons, many=True).data


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'