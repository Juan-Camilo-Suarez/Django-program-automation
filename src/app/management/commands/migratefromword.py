from django.core.management.base import BaseCommand
from src.app.management.commands.utils import process_file


class Command(BaseCommand):
    help = "Migrate from word docx to database"

    def handle(self, *args, **kwargs):
        process_file(kwargs["file"])

    def add_arguments(self, parser):
        parser.add_argument(
            "file",
            type=str,
        )
