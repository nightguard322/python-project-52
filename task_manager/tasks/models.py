from django.db import models

# Create your models here.
class Status(models.Model):
    name = models.CharField('Название', max_lenght=200)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_add=True)