from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from online_education.models import Subscription
from users.models import User


@shared_task
def subscribe_update(course):
    """Проверяет подписку пользователей на обновления курса и отправляет уведомление на E-mail."""
    users = User.objects.all()

    for user in users:
        subs_item = Subscription.objects.filter(user=user, course=course)

        if subs_item.exists():
            send_mail(
                subject="Обновление курса",
                message=f"По курсу {course.title} вышло обновление. Перейдите на сайт для просмотра",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )


@shared_task
def last_login_check():
    """Деактивирует пользователей, которые не авторизовывались на сайте более 30 дней."""
    today = timezone.now().today().date()
    users = User.objects.filter(last_login__isnull=False, last_login__lt=today - timedelta(days=30))
    for user in users:
        user.is_active = False
        user.save()
