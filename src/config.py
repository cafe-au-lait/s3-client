# coding:utf-8
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    # oss配置
    oss_endpoint: Optional[str] = "http://127.0.0.1:9000"
    oss_access_key: Optional[str] = "OSS_ACCESS_KEY"
    oss_secret_key: Optional[str] = "OSS_SECRET_KEY"
    oss_region: Optional[str] = None
    oss_bucket: Optional[str] = 'default'

    class Config:
        env_prefix = ''
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
