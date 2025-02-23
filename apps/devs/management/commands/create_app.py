from django.core.management.base import CommandParser
from django.core.management import BaseCommand
import os


class Command(BaseCommand):
    """앱 생성"""

    app_name = ""
    directories = ["migrations", "models", "views", "validations", "services"]
    default_files_dict = {
        "admin.py": "from django.contrib import admin\n\n# Register your models here.\n",
        "urls.py": "from django.urls import path\n\nurlpatterns = []\n",
        "apps.py": "from django.apps import AppConfig\n\n\nclass {}Config(AppConfig):\n    default_auto_field = 'django.db.models.BigAutoField'\n    name = \"{}\"\n",
    }

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("app_name", type=str, help="생성할 앱 네임")

    def handle(self, *args, **kwargs):
        app_name = kwargs["app_name"]
        self.app_name = app_name

        self._create_directories(app_name)
        self._create_init_file(app_name)
        self._create_default_files(app_name)

    def _create_directories(self, app_name: str):
        os.mkdir(app_name)
        os.chdir(app_name)
        for directory in self.directories:
            os.mkdir(f"./{directory}")

    def _create_init_file(self, app_name: str):
        for directory in self.directories:
            os.chdir(directory)
            with open("__init__.py", "w") as file:
                file.write(f"# {app_name}")
            os.chdir("..")

    def _create_default_files(self, app_name: str):
        for file_name, file_content in self.default_files_dict.items():
            if file_name == "apps.py":
                file_content = file_content.format(
                    app_name.capitalize(), f"apps.{app_name}"
                )
            with open(file_name, "w") as file:
                file.write(file_content)
