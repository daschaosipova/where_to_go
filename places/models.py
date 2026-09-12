from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="Название")
    description_short = models.TextField(verbose_name="Короткое описание", blank=True)
    description_long = models.TextField(verbose_name="Длинное описание", blank=True)
    
    lat = models.FloatField(verbose_name="Широта")
    lng = models.FloatField(verbose_name="Долгота")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Интересное место"
        verbose_name_plural = "Интересные места"