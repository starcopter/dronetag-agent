import os
import re
from ipaddress import IPv4Address
from typing import Annotated, Tuple, Type

from pydantic import AfterValidator
from pydantic_settings import BaseSettings, JsonConfigSettingsSource, PydanticBaseSettingsSource, SettingsConfigDict

from mavlink_messages.enums import CategoryEU, ClassEU, UAType
from oprn import OPRN

CONFIG_FILE = os.environ.get("DRONETAG_AGENT_CONFIG_FILE", "config.json")


def validate_uas_id(uas_id: str) -> str:
    """Validate UAS ID according to ANSI/CTA-2063-A, September 2019 edition."""
    m = re.match(r"^(?P<mfr>[0-9A-HJ-NP-Z]{4})(?P<len>[0-9A-F])(?P<serial>[0-9A-HJ-NP-Z]{1,15})$", uas_id)
    if not m:
        raise ValueError("Invalid UAS ID format")
    if len(m.group("serial")) != int(m.group("len"), 16):
        raise ValueError("Invalid UAS ID length")
    return uas_id


class Settings(BaseSettings):
    uas_id: Annotated[str, AfterValidator(validate_uas_id)] | None = None
    uas_type: UAType = UAType.MAV_ODID_UA_TYPE_HELICOPTER_OR_MULTIROTOR
    skynode_id: str | None = None
    oprn: OPRN | None = None
    category_eu: CategoryEU = CategoryEU.MAV_ODID_CATEGORY_EU_OPEN
    class_eu: ClassEU = ClassEU.MAV_ODID_CLASS_EU_CLASS_3

    mavlink_endpoint_ip: IPv4Address = IPv4Address("172.17.0.1")
    mavlink_endpoint_port: int = 5790
    fmu_system_id: int = 1
    fmu_component_id: int = 236  # MAV_COMP_ID_ODID_TXRX_1
    dri_system_id: int = 2
    dri_component_id: int = 1  # MAV_COMP_ID_AUTOPILOT1

    odid_course_speed_threshold: int = 25  # cm/s

    model_config = SettingsConfigDict(
        validate_assignment=True,
        secrets_dir="/etc",
        json_file=CONFIG_FILE,
        env_ignore_empty=True,
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return init_settings, env_settings, JsonConfigSettingsSource(settings_cls), file_secret_settings

    def save(self):
        with open(self.model_config["json_file"], "w") as f:
            f.write(self.model_dump_json(indent=2, exclude_defaults=True))
            f.write("\n")

    def load(self):
        # https://docs.pydantic.dev/latest/concepts/pydantic_settings/#in-place-reloading
        self.__init__()


if __name__ == "__main__":
    from rich import print

    settings = Settings()
    print(settings)
    settings.save()
