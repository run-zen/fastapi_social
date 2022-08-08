from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_password: str
    database_port: str
    database_name: str
    database_username: str
    Messaging_Service_SID: str
    Account_SID: str
    Auth_token: str

    secret_key: str
    algorithm: str
    access_token_expire_days: int

    class Config:
        env_file = "local.env"


settings = Settings()
