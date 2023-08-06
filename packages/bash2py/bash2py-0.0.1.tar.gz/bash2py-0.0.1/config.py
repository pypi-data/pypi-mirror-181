import os
import uuid


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or str(uuid.uuid4())
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
