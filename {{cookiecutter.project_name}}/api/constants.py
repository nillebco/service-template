import sys
import os

AUTHOR = "{{cookiecutter.full_name}} <{{cookiecutter.email}}>"
APP_NAME = "{{cookiecutter.project_name}}"

IS_TESTING : bool = "pytest" in sys.modules
IS_DEV : bool = os.getenv("IS_DEV") == "true"
DATA_FOLDER : str = "data"
API_PREFIX : str = "/api/v1"

MEDIA_DYNAMIC_API : str = "/media/dynamic"
