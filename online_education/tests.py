from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from online_education.models import Lesson, Course, Subscription
from users.models import User


# Create your tests here.


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(title='test', description='test',
                                            video_link='https://www.youtube.com/watch?v=0xXIPqRCx',
                                            owner=self.user)

    def test_create_lesson(self):
        data = {
            'title': self.lesson.title,
            'description': self.lesson.description,
            'video_link': self.lesson.video_link,
        }

        response = self.client.post('/lesson/create/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('title'), self.lesson.title)
        self.assertEqual(response.json().get('description'), self.lesson.description)
        self.assertEqual(response.json().get('video_link'), self.lesson.video_link)
        self.assertEqual(response.json().get('owner'), self.user.id)
        self.assertTrue(Lesson.objects.filter(title=self.lesson.title).exists())

    def test_update_lesson(self):
        data = {
            'title': 'Test 2',
            'description': 'Test 2',
            'video_link': 'https://www.youtube.com/watch?v=0xXIP',
        }

        response = self.client.patch(f'/lesson/update/{self.lesson.id}/', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), data['title'])
        self.assertEqual(response.json().get('description'), data['description'])
        self.assertEqual(response.json().get('video_link'), data['video_link'])
        self.assertEqual(response.json().get('owner'), self.user.id)
        self.assertTrue(Lesson.objects.filter(title=data['title']).exists())

    def test_delete_lesson(self):

        response = self.client.delete(f'/lesson/delete/{self.lesson.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(title=self.lesson.title).exists())

    def test_get_lesson(self):
        response = self.client.get(f'/lesson/{self.lesson.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), 'test')
        self.assertEqual(response.json().get('description'), 'test')
        self.assertEqual(response.json().get('video_link'), 'https://www.youtube.com/watch?v=0xXIPqRCx')
        self.assertEqual(response.json().get('owner'), self.user.id)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='test', description='test')

    def test_create_subscription(self):
        url = reverse("online_education:subscription-check")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Подписка подключена")

    def test_delete_subscription(self):
        Subscription.objects.create(course=self.course, user=self.user)

        url = reverse("online_education:subscription-check")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data["message"], "Подписка отключена")
