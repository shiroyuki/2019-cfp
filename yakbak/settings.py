from typing import Any, Dict, Optional
import os.path

from attr import attrib, attrs, fields
from attr.validators import instance_of, optional
import toml


class InvalidSettings(Exception):
    pass


@attrs(frozen=True)
class DbSettings:
    uri: str = attrib(validator=instance_of(str))


@attrs(frozen=True)
class LoggingSettings:
    level: str = attrib(validator=instance_of(str))


@attrs(frozen=True)
class FlaskSettings:
    secret_key: str = attrib(validator=instance_of(str))


@attrs(frozen=True)
class SocialAuthSettings:
    github_key: Optional[str] = attrib(validator=optional(instance_of(str)))
    github_secret: Optional[str] = attrib(validator=optional(instance_of(str)))

    google_key: Optional[str] = attrib(validator=optional(instance_of(str)))
    google_secret: Optional[str] = attrib(validator=optional(instance_of(str)))

    # these are initialized in core.py
    github: bool = attrib()
    google: bool = attrib()
    none: bool = attrib()


@attrs(frozen=True)
class Settings:
    db: DbSettings = attrib()
    logging: LoggingSettings = attrib()
    flask: FlaskSettings = attrib()
    social_auth: SocialAuthSettings = attrib()


def find_settings_file() -> str:
    """
    Returns the canonical location of ``yakbak.toml`` in the project root.

    """
    here = os.path.dirname(__file__)
    toml = os.path.join(here, "..", "yakbak.toml")
    return os.path.abspath(toml)


def load_settings_file(settings_path: str) -> Settings:
    with open(settings_path) as fp:
        return load_settings(toml.load(fp))


def load_settings(settings_dict: Dict[str, Any]) -> Settings:
    top_level = {}
    for field in fields(Settings):
        section = field.name
        data = settings_dict.pop(section, None)
        if data is None:
            raise InvalidSettings(f"settings missing section: {section}")

        # For each social auth method, set a setting named eg "github"
        # if that method is configured; if none are configured, set
        # a field "none" to True
        if section == "social_auth":
            social_methods = set([
                f.name[:-4]
                for f in fields(SocialAuthSettings)
                if f.name.endswith("_key")
            ])

            data["none"] = True
            for social_method in social_methods:
                key_field = "{}_key".format(social_method)
                secret_field = "{}_secret".format(social_method)
                data.setdefault(key_field, None)
                data.setdefault(secret_field, None)
                data[social_method] = data.get(key_field) and data.get(secret_field)
                if data[social_method]:
                    data["none"] = False

        top_level[section] = field.type(**data)

    if settings_dict:
        raise InvalidSettings(
            f"settings has unexpected sections: {settings_dict.keys()}")

    return Settings(**top_level)  # type: ignore
