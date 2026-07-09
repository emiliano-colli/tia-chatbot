import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.4))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 800))

    @classmethod
    def validate(cls):
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "Falta OPENAI_API_KEY en el archivo .env. "
                "Copiá .env.example a .env y completá tu clave."
            )

config = Config()
config.validate()
