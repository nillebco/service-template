import sys
import os

APP_NAME = "podcasts-app"
IS_TESTING = "pytest" in sys.modules
IS_DEV = os.getenv("IS_DEV")
DATA_FOLDER = "data"
API_PREFIX = "/api/v1"
MEDIA_API = "/media/static"
MEDIA_DYNAMIC_API = "/media/dynamic"
