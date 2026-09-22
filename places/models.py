from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название",
    )
    short_description = models.TextField(
        verbose_name="Короткое описание",
        blank=True,
    )
    long_description = HTMLField(
        verbose_name="Длинное описание",
        blank=True,
    )

    lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Широта",
    )
    lng = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Долгота",
    )

    class Meta:
        verbose_name = "Интересное место"
        verbose_name_plural = "Интересные места"

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(
        "Place",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Место",
    )
    image = models.ImageField(
        verbose_name="Изображение",
    )

    position = models.PositiveIntegerField(
        default=0,
        verbose_name="Позиция",
    )

    class Meta:
        ordering = ["position"]
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

    def __str__(self):
        return f"{self.position} {self.place.title}"
