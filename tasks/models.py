from django.db import models

# Create your models here.
class Status(models.Model):
    STATUSES = {
        new: 'новый',
        at_work: 'в работе',
        testing: 'на тестировании',
        done: 'завершен'
    }
    name = models.CharField(verbose_name='Название', max_lenght=200, choises=STATUSES, default=new)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлен', auto_add=True)


class Task(models.Model):
    name = models.CharField(verbose_name='Имя', max_lenght=200)
    description = models.TextField(verbose_name='Описание')
    author = models.ForeignKey('User', verbose_name='Автор', on_delete=models.PROTECT)
    reference_to = models.ForeignKey('User', verbose_name='Испольнитель', on_delete=models.PROTECT)
    status = models.ForeignKey('Status', verbose_name='Статус', on_delete=models.PROTECT)