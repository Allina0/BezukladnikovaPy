from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название вида')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид'
        verbose_name_plural = 'Виды'


class Stats(models.Model):
    key = models.CharField(max_length=255, verbose_name='Ключ')
    value = models.CharField(max_length=255, verbose_name='Значение')
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return self.key + ' - ' + self.value

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'


class Image(models.Model):
    url = models.FileField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return self.url.url

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
