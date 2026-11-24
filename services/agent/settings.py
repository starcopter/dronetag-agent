import logging
import os
import re
from ipaddress import IPv4Address
from pathlib import Path
from typing import Annotated, Any, Tuple, Type

from pydantic import AfterValidator
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, JsonConfigSettingsSource, PydanticBaseSettingsSource, SettingsConfigDict

from mavlink_messages.enums import CategoryEU, ClassEU, UAType
from oprn import OPRN

logger = logging.getLogger(__name__)

CONFIG_FILE = os.environ.get("DRONETAG_AGENT_CONFIG_FILE", "config.json")
DEFAULT_SUITE_DIR = Path("/mnt/suite")
VEHICLE_SN_FILENAME = "vehicle_sn"


def validate_uas_id(uas_id: str) -> str:
    """Validate UAS ID according to ANSI/CTA-2063-A, September 2019 edition."""
    m = re.match(r"^(?P<mfr>[0-9A-HJ-NP-Z]{4})(?P<len>[0-9A-F])(?P<serial>[0-9A-HJ-NP-Z]{1,15})$", uas_id)
    if not m:
        raise ValueError("Invalid UAS ID format")
    if len(m.group("serial")) != int(m.group("len"), 16):
        raise ValueError("Invalid UAS ID length")
    return uas_id


def suite_dir() -> Path:
    """Directory bind-mounted from the Skynode's /persistent/suite."""
    return Path(os.environ.get("DRONETAG_AGENT_SUITE_DIR", DEFAULT_SUITE_DIR))


def read_vehicle_sn() -> str | None:
    """Return the vehicle serial when vehicle_sn is a regular file.

    A missing path is normal before the serial is programmed. A directory at that
    path is left over from mounting the file itself and must not be treated as a serial.
    """
    path = suite_dir() / VEHICLE_SN_FILENAME
    if not path.exists():
        return None
    if not path.is_file():
        logger.warning("UAS ID path %s is not a regular file, so no serial was loaded", path)
        return None
    value = path.read_text().strip()
    return value or None


class VehicleSnSettingsSource(PydanticBaseSettingsSource):
    """Load uas_id from the Suite directory. Lower priority than env and config.json."""

    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        return None, "", False

    def __call__(self) -> dict[str, Any]:
        uas_id = read_vehicle_sn()
        if uas_id is None:
            return {}
        return {"uas_id": uas_id}


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

    course_speed_threshold_fraction: float = 0.5

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
        return (
            init_settings,
            env_settings,
            JsonConfigSettingsSource(settings_cls),
            file_secret_settings,
            VehicleSnSettingsSource(settings_cls),
        )

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
