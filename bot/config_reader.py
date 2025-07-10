from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, RedisDsn

class Settings(BaseSettings):
    GITHUB_TOKEN: SecretStr
    DEEPSEEK_MODEL: str = "deepseek/DeepSeek-V3-0324"

    BOT_TOKEN: SecretStr

    REDIS_URL: RedisDsn = RedisDsn("redis://localhost:6379/0")

    CLERY_BROKER_URL: RedisDsn = RedisDsn("redis://localhost:6379/1")
    CLERY_RESULT_BACKEND: RedisDsn = RedisDsn("redis://localhost:6379/2")

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

config = Settings()