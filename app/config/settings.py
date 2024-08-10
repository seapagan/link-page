"""Set up the settings for the project."""

from simple_toml_settings import TOMLSettings


class Settings(TOMLSettings):
    """Settings for the project."""

    name: str
    role: str
    homepage: dict[str, str]
    github: str


settings = Settings.get_instance("linkpage", local_file=True)
