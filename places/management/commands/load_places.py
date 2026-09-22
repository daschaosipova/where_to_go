from django.core.management.base import BaseCommand, CommandError
from environs import Env

from places.management.commands.load_place import Command as LoadPlaceCommand

URL_ENV_VAR = "PLACES_INDEX_URL"

env = Env()
env.read_env()


class Command(BaseCommand):
    help = "Загружает в базу все локации из репозитория where-to-go-places"

    def add_arguments(self, parser):
        parser.add_argument(
            "--index",
            help=(
                "URL со списком JSON-файлов локаций. "
                "По умолчанию берётся из переменной окружения PLACES_INDEX_URL"
            ),
        )

    def handle(self, *args, **options):
        loader = LoadPlaceCommand(
            stdout=self.stdout, stderr=self.stderr, no_color=options.get("no_color", False)
        )

        index_url = options["index"] or env(URL_ENV_VAR, default=None)
        if not index_url:
            raise CommandError(
                "Укажите URL списка локаций: флагом --index "
                "или переменной окружения PLACES_INDEX_URL"
            )

        try:
            entries = loader.download_json(index_url)
        except CommandError as exc:
            self.stderr.write(self.style.ERROR(str(exc)))
            return

        json_files = [
            entry
            for entry in entries
            if isinstance(entry, dict) and entry.get("name", "").endswith(".json")
        ]
        if not json_files:
            raise CommandError("В списке нет JSON-файлов локаций")

        loaded = 0
        for entry in json_files:
            name = entry["name"]
            download_url = entry.get("download_url")
            if not download_url:
                self.stderr.write(self.style.WARNING(f"Пропускаю {name}: нет ссылки на файл"))
                continue
            try:
                payload = loader.download_json(download_url)
                loader.create_place(payload)
                loaded += 1
            except (CommandError, KeyError, ValueError) as exc:
                self.stderr.write(self.style.WARNING(f"{name}: {exc}"))

        self.stdout.write(self.style.SUCCESS(f"Загружено локаций: {loaded}"))
