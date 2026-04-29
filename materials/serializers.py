from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()


    class Meta:
	    model = Course
	    fields = ('title', "review", 'description', 'lessons_count')

    @staticmethod
    def get_lessons_count(self):
        return Lesson.objects.all().count()





class LessonSerializer(ModelSerializer):
	class Meta:
	    model = Lesson
	    fields = '__all__'
