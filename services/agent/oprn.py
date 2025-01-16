import re
from pathlib import Path
from typing import Any

from pydantic import GetCoreSchemaHandler, ValidatorFunctionWrapHandler
from pydantic_core import CoreSchema

from luhn import validate_string

COUNTRY_CODES_FILE = Path(__file__).parent / "iso3166-1.txt"
COUNTRY_CODES = {k: v for k, v in (line.split(maxsplit=1) for line in COUNTRY_CODES_FILE.read_text().splitlines())}


class OPRN:
    RE = re.compile(r"^(?P<a1>[A-Z]{3})(?P<a2>[0-9a-z]{12})(?P<a3>[0-9a-z])-(?P<b>[0-9a-z]{3})$", re.IGNORECASE)

    def __init__(self, oprn: str):
        if not isinstance(oprn, str):
            raise TypeError("OPRN must be a string")

        m = self.RE.match(oprn)
        if not m:
            raise ValueError("Format Error, check EN 4709-002:2023")

        a1 = m.group("a1").upper()
        if a1 not in COUNTRY_CODES:
            raise ValueError("Invalid Country Code, check ISO 3166-1")

        a2 = m.group("a2").lower()
        a3 = m.group("a3").lower()
        b = m.group("b").lower()

        luhn_str = a2 + b + a3
        if not validate_string(luhn_str):
            raise ValueError("Invalid OPRN: Checksum Error")

        self.oprn = f"{a1}{a2}{a3}-{b}"

    def __str__(self):
        return self.oprn

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.oprn})"

    @property
    def public_part(self) -> str:
        return self.oprn.split("-")[0]

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        from pydantic_core import core_schema

        return core_schema.no_info_wrap_validator_function(
            cls._pydantic_validate,
            core_schema.union_schema(
                [
                    core_schema.is_instance_schema(OPRN),
                    core_schema.no_info_plain_validator_function(OPRN),
                    core_schema.str_schema(pattern=r"[A-Z]{3}[0-9a-z]{13}-[0-9a-z]{3}", min_length=20, max_length=20),
                    core_schema.bytes_schema(min_length=20, max_length=20),
                ]
            ),
            serialization=core_schema.to_string_ser_schema(when_used="json-unless-none"),
        )

    @classmethod
    def _pydantic_validate(cls, value: Any, handler: ValidatorFunctionWrapHandler) -> Any:
        from pydantic_core import PydanticCustomError

        try:
            oprn = OPRN(value)
        except ValueError as err:
            raise PydanticCustomError("oprn_format", str(err)) from err
        return handler(oprn)


if __name__ == "__main__":
    print(OPRN("FIN87astrdge12k8-xyz"))
    print(OPRN("FIN92hello1world-909"))
    print(OPRN("FIN87ASTRDGE12K8-XYZ"))
    print(OPRN("fin87astrdge12k8-xyz"))
