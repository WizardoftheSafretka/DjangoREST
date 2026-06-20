# tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User  # импортируйте вашу модель пользователя


@shared_task
def block_inactive_users():
    """Блокировка пользователей, которые не заходили более месяца"""

    month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        is_active=True,
        last_login__lt=month_ago
    )

    for user in inactive_users:
        user.is_active = False
        user.save()