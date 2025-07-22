from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://neondb_owner:npg_rRuahBA2GqQ9@ep-super-thunder-a6p0m6j8.us-west-2.aws.neon.tech/neondb?sslmode=require"
    
    class Config:
        env_file = ".env"

settings = Settings()