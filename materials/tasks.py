# tasks.py
from celery import shared_task
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


@shared_task
def send_update(course_id):
    """Отправляет письма всем подписчикам курса об его обновлении"""

    from materials.models import Subscribe

    subscriptions = Subscribe.objects.filter(course_id=course_id, is_subscribe=True)

    for subscription in subscriptions:
        send_mail(
            'Обновление курса',
            f'Курс "{subscription.course.title}" был обновлен',
            EMAIL_HOST_USER,
            [subscription.user.email]
        )