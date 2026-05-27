from django.core.management.base import BaseCommand
from materials.models import Course, Lesson
from users.models import User, Payment


class Command(BaseCommand):
    help = 'Fill database with test data'

    def handle(self, *args, **options):
        # Создаем курсы
        course1 = Course.objects.create(
            title="Python для начинающих",
            description="Базовый курс по Python"
        )
        course2 = Course.objects.create(
            title="Django Framework",
            description="Продвинутый курс по Django"
        )

        # Создаем уроки
        lesson1 = Lesson.objects.create(
            title="Введение в Python",
            course=course1,
            description="Первый урок по Python",
            url="https://www.youtube.com/watch?v=example1"
        )
        lesson2 = Lesson.objects.create(
            title="Переменные и типы данных",
            course=course1,
            description="Второй урок по Python",
            url="https://www.youtube.com/watch?v=example2"
        )

        # Создаем пользователей
        user1 = User.objects.create_user(
            email='user1@example.com',
            password='password123'
        )
        user2 = User.objects.create_user(
            email='user2@example.com',
            password='password123'
        )

        # Создаем платежи
        Payment.objects.create(
            user=user1,
            paid_course=course1,
            amount=4999.00,
            payment_method='transfer'
        )
        Payment.objects.create(
            user=user1,
            paid_lesson=lesson1,
            amount=999.00,
            payment_method='cash'
        )
        Payment.objects.create(
            user=user2,
            paid_course=course2,
            amount=2999.00,
            payment_method='transfer'
        )

        self.stdout.write(self.style.SUCCESS('Database filled successfully!'))