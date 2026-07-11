from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class BaseAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="admin@example.com",
            password="testpass123"
        )

        self.moderator = User.objects.create_user(
            email="moder@example.com",
            password="testpass456"
        )
        self.moderator.is_staff = True
        self.moderator.save()

        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="testpass789"
        )

        self.course = Course.objects.create(
            title='Test Course',
            description='Test description',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        User.objects.all().delete()


class CourseTestCase(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            course=self.course,
            owner=self.user
        )

    def test_course_retrieve(self):
        """Тест получения курса"""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), self.course.title)

    def test_course_list(self):
        """Тест списка курсов"""
        url = reverse("materials:course-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data.get("count"), 1)

    def test_course_create(self):
        """Тест создания курса (обычный пользователь МОЖЕТ)"""
        url = reverse("materials:course-list")
        data = {
            "title": "New Course",
            "description": "Test description"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_course_create_moderator(self):
        """Тест создания курса модератором (тоже может)"""
        self.client.force_authenticate(user=self.moderator)

        url = reverse("materials:course-list")
        data = {
            "title": "Moder Course",
            "description": "Test description"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_course_update(self):
        """Тест обновления курса (владелец может)"""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {"title": "Updated Course Title"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Updated Course Title")

    def test_course_update_other_user(self):
        """Тест обновления чужого курса (другой пользователь НЕ может)"""
        self.client.force_authenticate(user=self.other_user)

        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {"title": "Hacked Title"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_update_moderator(self):
        """Тест обновления курса модератором (может)"""
        self.client.force_authenticate(user=self.moderator)

        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {"title": "Moder Updated Title"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Moder Updated Title")

    def test_course_delete(self):
        """Тест удаления курса (обычный пользователь НЕ может)"""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Course.objects.count(), 1)

    def test_course_delete_moderator(self):
        """Тест удаления курса модератором (может)"""
        self.client.force_authenticate(user=self.moderator)

        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


class LessonTestCase(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Lesson description',
            course=self.course,
            owner=self.user
        )

    def test_lesson_retrieve(self):
        """Тест получения урока"""
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), self.lesson.title)

    def test_lesson_list(self):
        """Тест списка уроков"""
        url = reverse("materials:lessons_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        if isinstance(data, dict) and "results" in data:
            self.assertGreaterEqual(data.get("count"), 1)
        else:
            self.assertGreaterEqual(len(data), 1)

    def test_lesson_update(self):
        """Тест обновления урока (владелец может)"""
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"title": "Updated Lesson Title"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson Title")

    def test_lesson_update_other_user(self):
        """Тест обновления чужого урока (другой пользователь НЕ может)"""
        self.client.force_authenticate(user=self.other_user)

        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"title": "Hacked Lesson"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_moderator(self):
        """Тест обновления урока модератором (может)"""
        self.client.force_authenticate(user=self.moderator)

        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"title": "Moder Updated Lesson"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Moder Updated Lesson")

    def test_lesson_delete(self):
        """Тест удаления урока (обычный пользователь НЕ может)"""
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_lesson_delete_moderator(self):
        """Тест удаления урока модератором (может)"""
        self.client.force_authenticate(user=self.moderator)

        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscribeTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpass123"
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test description',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        User.objects.all().delete()
        Course.objects.all().delete()

    def test_subscribe_create(self):
        """Тест создания подписки"""
        url = reverse("materials:subscribe-list")
        data = {"course": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("message"), "подписка добавлена")

    def test_subscribe_delete(self):
        """Тест удаления подписки"""
        url = reverse("materials:subscribe-list")
        data = {"course": self.course.pk}

        self.client.post(url, data)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data.get("message"), "подписка удалена")