from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Метка')
    created_at = models.DateTimeField(verbose_name='Создана', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Изменена', auto_now=True)

class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')