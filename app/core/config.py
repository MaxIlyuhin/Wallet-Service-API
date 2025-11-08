from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Wallet Service API'
    description: str = 'API для управления кошельками: депозиты, снятия, баланс. Поддержка параллельных операций.'

    class Config:
        env_file = '.env'


settings = Settings()
