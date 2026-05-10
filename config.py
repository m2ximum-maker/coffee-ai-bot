import os

from dotenv import load_dotenv

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if value is None or value.strip() == "":
        raise ValueError(f"{name} не найден в .env")

    return value


def get_optional_env(name: str, default: str) -> str:
    value = os.getenv(name)

    if value is None or value.strip() == "":
        return default

    return value


def get_bot_token() -> str:
    return get_required_env("BOT_TOKEN")


def get_db_path() -> str:
    return get_required_env("DB_PATH")


def get_openai_api_key() -> str:
    return get_required_env("OPENAI_API_KEY")


def get_openai_model() -> str:
    return get_optional_env("OPENAI_MODEL", "gpt-4.1-mini")
