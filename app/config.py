from pydantic import BaseSettings, validator
import os

class Settings(BaseSettings):
    client_origin_url: str
    http_port: int
    reload: bool
    auth_base_url: str
    realm: str
    client_id: str

    # @classmethod
    # @validator("auth_base_url", "realm", "client_id")
    # def check_not_empty(cls, v):
    #     assert v != "", f"{v} is not defined"
    #     return v

    class Config:
        case_sensitive = False
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"

# print(os.environ.items())
settings = Settings()
print(Settings().dict())
