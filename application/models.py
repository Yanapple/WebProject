from django.db import models

# Create your models here.
class Profession(models.Model):
    name = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')


    def __str__(self):
        return  self.name

    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'
