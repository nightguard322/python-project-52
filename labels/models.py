from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Label(models.Model):
    name = models.CharField(max_length=200, verbose_name='Метка')
    created_at = models.DateTimeField(verbose_name='Создана', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Изменена', auto_now=True)

    def __str__(self):
        return self.name
        
class TaggedItem(models.Model):
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id') 

    def __str__(self):
        return self.label.name