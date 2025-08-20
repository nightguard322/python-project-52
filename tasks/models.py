from django.db import models
from django.conf import settings

# Create your models here.
class Status(models.Model):
    # NEW = 'new'
    # AT_WORK = 'at_work'
    # TESTING = 'testing'
    # DONE = 'done'

    # STATUSES = [
    #     (NEW, 'новый'),
    #     (AT_WORK, 'в работе'),
    #     (TESTING, 'на тестировании'),
    #     (DONE, 'завершен')
    # ]
    name = models.CharField(verbose_name='Имя', max_length=200) #, choices=STATUSES, default=NEW)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлен', auto_now=True)


class Task(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=200)
    description = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        related_name='Author',
        on_delete=models.PROTECT
    )
    reference_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Испольнитель',
        related_name='reference_to',
        on_delete=models.PROTECT
    )
    status = models.ForeignKey('Status', verbose_name='Статус', on_delete=models.PROTECT)