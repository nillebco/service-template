import sys
import os

AUTHOR = "{{cookiecutter.full_name}} <{{cookiecutter.email}}>"
APP_NAME = "{{cookiecutter.project_name}}"

IS_TESTING = "pytest" in sys.modules
IS_DEV = os.getenv("IS_DEV")
DATA_FOLDER = "data"
API_PREFIX = "/api/v1"

MEDIA_DYNAMIC_API = "/media/dynamic"
