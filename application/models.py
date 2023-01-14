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


class Table(models.Model):
    title = models.CharField(max_length=150)
    graphic = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title