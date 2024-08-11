from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

# Create your models here.


class BgRemover(models.Model):
    img = models.ImageField(upload_to='remove')
    created_at = models.DateField(auto_now=True)
    result = models.ImageField(upload_to='result', blank=True, null=True)


@receiver(post_delete, sender=BgRemover)
def delete_result_file(sender, instance, **kwargs):
    if instance.result:
        if os.path.isfile(instance.result.path):
            os.remove(instance.result.path)
    if instance.created_at:
        if os.path.isfile(instance.img.path):
            os.remove(instance.img.path)
