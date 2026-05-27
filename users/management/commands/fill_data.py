from django.core.management.base import BaseCommand
from materials.models import Course, Lesson
from django.contrib.auth import get_user_model

from users.models import Payment

User = get_user_model()


class Command(BaseCommand):
    help = 'Fill database with test data'

    def handle(self, *args, **options):
        # Очищаем существующие данные
        self.stdout.write('Clearing existing data...')

        Payment.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Existing data cleared successfully!'))

        # Создаем пользователей
        self.stdout.write('Creating users...')
        user1 = User.objects.create(
            email='user1@example.com',
            password='password123'
        )
        user2 = User.objects.create(
            email='user2@example.com',
            password='password123'
        )

        user1.set_password('password123')
        user2.set_password('password123')
        user1.save()
        user2.save()

        # Создаем курсы с owner
        self.stdout.write('Creating courses...')
        course1 = Course.objects.create(
            title="Python для начинающих",
            description="Базовый курс по Python",
            owner=user1
        )
        course2 = Course.objects.create(
            title="Django Framework",
            description="Продвинутый курс по Django",
            owner=user2
        )

        # Создаем уроки
        self.stdout.write('Creating lessons...')
        lesson1 = Lesson.objects.create(
            title="Введение в Python",
            course=course1,
            description="Первый урок по Python",
            url="https://www.youtube.com/watch?v=example1",
            owner = user1
        )
        lesson2 = Lesson.objects.create(
            title="Переменные и типы данных",
            course=course1,
            description="Второй урок по Python",
            url="https://www.youtube.com/watch?v=example2",
            owner = user2
        )

        # Создаем платежи
        self.stdout.write('Creating payments...')
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
        self.stdout.write(f'Courses: {Course.objects.count()}')
        self.stdout.write(f'Lessons: {Lesson.objects.count()}')
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Payments: {Payment.objects.count()}')