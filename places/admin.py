from django.contrib import admin
from django.utils.html import format_html
from .models import Place, PlaceImage


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)

admin.site.register(PlaceImage)
