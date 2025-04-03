from django.contrib.auth.models import AbstractUser
from django.db import models
from online_education.models import Lesson, Course


# Create your models here.


class User(AbstractUser):
    phone = models.CharField(
        max_length=35,
        verbose_name='Телефон',
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        upload_to='users/',
        null=True,
        blank=True,
        verbose_name='Аватар'
    )
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='E-mail'
    )
    city = models.CharField(
        max_length=100,
        verbose_name='Страна',
        blank=True,
        null=True
    )

    token = models.CharField(
        max_length=100,
        verbose_name="Токен",
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        null=True,
        blank=True,
        related_name='payments'
    )
    date = models.DateTimeField(
        verbose_name='Дата оплаты'
    )
    paid_course = models.ForeignKey(
        Course,
        verbose_name='Оплаченный курс',
        on_delete=models.CASCADE,
        related_name='paid_courses',
        null=True,
        blank=True
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        verbose_name='Оплаченный урок',
        on_delete=models.CASCADE,
        related_name='paid_lessons',
        null=True,
        blank=True,
    )

    amount = models.PositiveIntegerField(
        verbose_name='Сумма оплаты'
    )
    payment_method = models.CharField(
        max_length=50,
        verbose_name='Способ оплаты'
    )
