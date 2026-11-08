# BaseSettings reads values from environment variables / a .env file and validates them
# SettingsConfigDict lets us tell it WHERE to find the .env file
from pydantic_settings import BaseSettings, SettingsConfigDict


# A class that holds all of our app's settings in one place
class Settings(BaseSettings):
    # The database address. No default value, so the app refuses to start if it's missing
    DATABASE_URL: str

    # Tell pydantic-settings to read from a file called ".env" (utf-8 text)
    # extra="ignore" means unknown variables in .env won't cause an error
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


# Create ONE settings object that the rest of the app imports and reuses
settings = Settings()
