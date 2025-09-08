from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.
class Status(models.Model):

    name = models.CharField(verbose_name='Имя', max_length=200)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлен', auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=200)
    description = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        related_name='author',
        on_delete=models.PROTECT
    )
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        verbose_name='Исполнитель',
        related_name='executor',
        on_delete=models.PROTECT
    )
    status = models.ForeignKey(
        'Status',
        verbose_name='Статус',
        on_delete=models.PROTECT
    )
    created_at = models.DateTimeField(
        verbose_name='Создан',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлен',
        auto_now=True
    )
    labels = GenericRelation('labels.TaggedItem')

    def __str__(self):
        return self.name
    