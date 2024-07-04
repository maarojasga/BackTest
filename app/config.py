import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'config', '../.env')
load_dotenv(dotenv_path)

class Settings:
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_HOST = os.getenv('DATABASE_HOST')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_PORT = os.getenv('DATABASE_PORT')
    HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY')
    CLICKUP_API_KEY = os.getenv('CLICKUP_API_KEY')
    CLICKUP_LIST_ID = os.getenv('CLICKUP_LIST_ID')

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{int(self.DATABASE_PORT)}/{self.DATABASE_NAME}"

settings = Settings()

