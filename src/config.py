import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.4))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 800))

    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    MAIL_FROM = os.getenv("MAIL_FROM", "") or os.getenv("SMTP_USER", "")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")
    SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))

    @classmethod
    def validate(cls):
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "Falta OPENAI_API_KEY en el archivo .env. "
                "Copiá .env.example a .env y completá tu clave."
            )

    @classmethod
    def smtp_ready(cls) -> bool:
        return bool(
            cls.SMTP_HOST
            and cls.SMTP_PORT
            and cls.SMTP_USER
            and cls.SMTP_PASSWORD
            and cls.MAIL_FROM
            and cls.ADMIN_EMAIL
        )


config = Config()
config.validate()
