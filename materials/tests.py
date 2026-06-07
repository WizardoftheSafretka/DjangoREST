from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscribe
from users.models import User


class BaseAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin@example.com",
            password="testpass123"
        )
        self.moderator = User.objects.create(
            email="moder@example.com",
            password="testpass456",
            is_staff=True
        )
        self.other_user = User.objects.create(
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
        User.objects.all().delete()
        Course.objects.all().delete()
        Lesson.objects.all().delete()


class CourseTestCase(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            course=self.course,
            owner=self.user
        )

    def test_course_retrieve(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)
        self.assertEqual(data.get("description"), self.course.description)

    def test_course_create(self):
        url = reverse("materials:course-list")
        data = {
            "title": "New Course",
            "description": "Test description for new course"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_create_moderator(self):
        self.client.force_authenticate(user=self.moderator)

        url = reverse("materials:course-list")
        data = {
            "title": "Moder Course",
            "description": "Test description"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_create_invalid_data(self):
        url = reverse("materials:course-list")
        data = {"title": ""}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_update(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {"title": "Updated Course Title"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data.get("title"), "Updated Course Title")

        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Updated Course Title")

    def test_course_update_other_user(self):
        self.client.force_authenticate(user=self.other_user)

        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {"title": "Hacked Title"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_update_moderator(self):
        self.client.force_authenticate(user=self.moderator)

        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {"title": "Moder Updated Title"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Moder Updated Title")

    def test_course_delete(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_delete_moderator(self):
        course2 = Course.objects.create(
            title='Test Course 2',
            description='Test description',
            owner=self.other_user
        )
        self.client.force_authenticate(user=self.moderator)

        url = reverse("materials:course-detail", args=(course2.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_course_list(self):
        url = reverse("materials:course-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data.get("count"), 1)
        self.assertEqual(len(data.get("results")), 1)

        result = data.get("results")[0]
        self.assertEqual(result.get("id"), self.course.pk)
        self.assertEqual(result.get("title"), self.course.title)

        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(data.get("count"), 1)


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
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_retrieve_not_found(self):
        url = reverse("materials:lessons_retrieve", args=(999,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_lesson_create(self):
        url = reverse("materials:lessons_create")
        data = {
            "title": "New Lesson",
            "course": self.course.pk,
            "description": "Test description for new lesson"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_create_moderator(self):
        self.client.force_authenticate(user=self.moderator)

        url = reverse("materials:lessons_create")
        data = {
            "title": "Moder Lesson",
            "course": self.course.pk,
            "description": "Test description"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_create_without_course(self):
        url = reverse("materials:lessons_create")
        data = {
            "title": "New Lesson",
            "description": "Test description"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_create_invalid_course(self):
        url = reverse("materials:lessons_create")
        data = {
            "title": "New Lesson",
            "course": 999,
            "description": "Test description"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update(self):
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {
            "title": "Updated Lesson Title",
            "description": "Updated description"
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data.get("title"), "Updated Lesson Title")

        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson Title")

    def test_lesson_update_other_user(self):
        self.client.force_authenticate(user=self.other_user)

        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"title": "Hacked Lesson"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_update_moderator(self):
        self.client.force_authenticate(user=self.moderator)

        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"title": "Moder Updated Lesson"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Moder Updated Lesson")

    def test_lesson_delete(self):
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_delete_moderator(self):
        lesson2 = Lesson.objects.create(
            title='Test Lesson 2',
            description='Lesson description',
            course=self.course,
            owner=self.other_user
        )
        self.client.force_authenticate(user=self.moderator)

        url = reverse("materials:lessons_delete", args=(lesson2.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_lesson_list(self):
        url = reverse("materials:lessons_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        if isinstance(data, dict) and "results" in data:
            self.assertEqual(data.get("count"), 1)
            self.assertEqual(len(data.get("results")), 1)
            result = data.get("results")[0]
        else:
            self.assertEqual(len(data), 1)
            result = data[0]

        self.assertEqual(result.get("title"), self.lesson.title)


class SubscribeTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="user@example.com",
            password="testpass123"
        )
        self.other_user = User.objects.create(
            email="other@example.com",
            password="testpass456"
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
        Subscribe.objects.all().delete()

    def test_subscribe_create(self):
        url = reverse("materials:subscribe-list")
        data = {"course": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("message"), "подписка добавлена")
        self.assertEqual(Subscribe.objects.count(), 1)

        subscribe = Subscribe.objects.first()
        self.assertEqual(subscribe.user, self.user)
        self.assertEqual(subscribe.course, self.course)
        self.assertTrue(subscribe.is_subscribe)

    def test_subscribe_delete(self):
        Subscribe.objects.create(
            course=self.course,
            user=self.user,
            is_subscribe=True
        )

        url = reverse("materials:subscribe-list")
        data = {"course": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data.get("message"), "подписка удалена")
        self.assertEqual(Subscribe.objects.count(), 0)

    def test_subscribe_toggle(self):
        url = reverse("materials:subscribe-list")
        data = {"course": self.course.pk}

        response1 = self.client.post(url, data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscribe.objects.count(), 1)

        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscribe.objects.count(), 0)

    def test_subscribe_without_course(self):
        url = reverse("materials:subscribe-list")
        data = {}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscribe_with_invalid_course(self):
        url = reverse("materials:subscribe-list")
        data = {"course": 999}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscribe_unauthenticated(self):
        self.client.force_authenticate(user=None)

        url = reverse("materials:subscribe-list")
        data = {"course": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscribe_list(self):
        Subscribe.objects.create(
            course=self.course,
            user=self.user,
            is_subscribe=True
        )

        url = reverse("materials:subscribe-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        if isinstance(data, dict) and "results" in data:
            self.assertEqual(data.get("count"), 1)
            result = data.get("results")[0]
        else:
            self.assertEqual(len(data), 1)
            result = data[0]

        self.assertEqual(result.get("is_subscribe"), True)
        self.assertEqual(result.get("user"), str(self.user.email))

    def test_subscribe_list_other_user(self):
        Subscribe.objects.create(
            course=self.course,
            user=self.other_user,
            is_subscribe=True
        )

        url = reverse("materials:subscribe-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        if isinstance(data, dict) and "results" in data:
            self.assertEqual(data.get("count"), 1)
        else:
            self.assertEqual(len(data), 1)

    def test_subscribe_retrieve(self):
        subscribe = Subscribe.objects.create(
            course=self.course,
            user=self.user,
            is_subscribe=True
        )

        url = reverse("materials:subscribe-detail", args=(subscribe.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("is_subscribe"), True)
        self.assertEqual(response.data.get("course").get("title"), self.course.title)

    def test_subscribe_retrieve_other_user(self):
        subscribe = Subscribe.objects.create(
            course=self.course,
            user=self.other_user,
            is_subscribe=True
        )

        url = reverse("materials:subscribe-detail", args=(subscribe.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscribe_delete_method(self):
        subscribe = Subscribe.objects.create(
            course=self.course,
            user=self.user,
            is_subscribe=True
        )

        url = reverse("materials:subscribe-detail", args=(subscribe.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscribe.objects.count(), 0)