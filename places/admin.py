from adminsortable2.admin import SortableAdminBase, SortableTabularInline
from django.contrib import admin
from django.utils.html import format_html

from .models import Place, PlaceImage


class PlaceImageInline(SortableTabularInline):
    model = PlaceImage
    extra = 0
    fields = ("image", "get_preview", "position")
    readonly_fields = ("get_preview",)

    def get_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; '
                'max-width: 100%; object-fit: contain;" />',
                obj.image.url,
            )
        return "Здесь появится превью"

    get_preview.short_description = "Превью"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    inlines = [PlaceImageInline]
