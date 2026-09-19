import json
import os
from urllib.parse import quote, unquote, urlparse, urlunparse
from urllib.request import Request, urlopen

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from places.models import Place, PlaceImage


class Command(BaseCommand):
    help = "Загружает локацию из JSON-файла по ссылке"

    def add_arguments(self, parser):
        parser.add_argument(
            "url",
            help="URL JSON-файла с данными локации",
        )

    def handle(self, *args, **options):
        url = options["url"]
        payload = self.download_json(url)
        self.create_place(payload)

    def download_json(self, url):
        url = self.normalize_url(url)
        try:
            with urlopen(
                Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30
            ) as response:
                return json.loads(response.read().decode("utf-8"))
        except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise CommandError(f"Не удалось загрузить данные из {url}: {exc}")

    def normalize_url(self, url):
        parts = urlparse(url)
        path = quote(unquote(parts.path))
        query = quote(unquote(parts.query), safe="&=")
        return urlunparse(parts._replace(path=path, query=query))

    def create_place(self, payload):
        title = payload.get("title")
        if not title:
            raise CommandError("В JSON-файле нет заголовка локации (ключ «title»)")

        coordinates = payload.get("coordinates", {})
        lat = coordinates.get("lat")
        lng = coordinates.get("lng")
        if lat is None or lng is None:
            raise CommandError("В JSON-файле нет координат локации (ключ «coordinates»)")

        place, _ = Place.objects.update_or_create(
            title=title,
            defaults={
                "description_short": payload.get("description_short", ""),
                "description_long": payload.get("description_long", ""),
                "lat": float(lat),
                "lng": float(lng),
            },
        )
        self.upload_images(place, payload.get("imgs", []))
        self.stdout.write(self.style.SUCCESS(f"Локация «{title}» загружена"))

    def upload_images(self, place, image_urls):
        existing_names = set(place.images.values_list("image", flat=True))
        last_position = (
            place.images.order_by("-position").values_list("position", flat=True).first()
        )
        position = (last_position + 1) if last_position is not None else 0

        for image_url in image_urls:
            filename = self.image_filename(image_url)
            if filename in existing_names:
                continue
            try:
                image_data = self.download(image_url)
            except OSError as exc:
                self.stderr.write(
                    self.style.WARNING(f"Не удалось скачать изображение {image_url}: {exc}")
                )
                continue
            PlaceImage.objects.create(
                place=place,
                image=ContentFile(image_data, name=filename),
                position=position,
            )
            existing_names.add(filename)
            position += 1

    def download(self, url):
        with urlopen(
            Request(self.normalize_url(url), headers={"User-Agent": "Mozilla/5.0"}),
            timeout=30,
        ) as response:
            return response.read()

    def image_filename(self, url):
        filename = os.path.basename(unquote(urlparse(url).path))
        return filename or "image.jpg"