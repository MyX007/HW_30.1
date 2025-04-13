from django.db import models

from config import settings


# Create your models here.


class Lesson(models.Model):
    """Модель урока."""
    title = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(upload_to="lessons/", null=True, blank=True)
    video_link = models.URLField(null=True, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    amount = models.IntegerField(default=0, verbose_name="Цена урока")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Course(models.Model):
    """Модель курса."""
    title = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(upload_to="courses/", null=True, blank=True)
    lessons = models.ManyToManyField(Lesson, blank=True, null=True, related_name="courses")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    amount = models.IntegerField(default=0, verbose_name="Цена курса")
    price_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Subscription(models.Model):
    """Модель полписки на курс."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", null=True,
                             blank=True, related_name="subscription_user")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", null=True, blank=True,
                               related_name="subscription_course")
