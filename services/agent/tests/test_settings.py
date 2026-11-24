import logging
from pathlib import Path

import pytest
from pydantic import ValidationError

from settings import Settings

VALID_SERIAL = "1715B12345678901"
OTHER_SERIAL = "17151Z"


@pytest.fixture
def suite(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    directory = tmp_path / "suite"
    directory.mkdir()
    secrets = tmp_path / "secrets"
    secrets.mkdir()
    monkeypatch.setenv("DRONETAG_AGENT_SUITE_DIR", str(directory))
    monkeypatch.delenv("UAS_ID", raising=False)
    monkeypatch.setitem(Settings.model_config, "secrets_dir", str(secrets))
    return directory


def test_reads_vehicle_sn_with_trailing_newline(suite: Path) -> None:
    (suite / "vehicle_sn").write_text(VALID_SERIAL + "\n")

    assert Settings().uas_id == VALID_SERIAL


def test_missing_vehicle_sn(suite: Path) -> None:
    assert Settings().uas_id is None


def test_blank_vehicle_sn(suite: Path) -> None:
    (suite / "vehicle_sn").write_text(" \n")

    assert Settings().uas_id is None


def test_vehicle_sn_directory(suite: Path, caplog: pytest.LogCaptureFixture) -> None:
    (suite / "vehicle_sn").mkdir()

    with caplog.at_level(logging.WARNING):
        settings = Settings()

    assert settings.uas_id is None
    assert "not a regular file" in caplog.text
    assert (suite / "vehicle_sn").is_dir()


def test_invalid_vehicle_sn(suite: Path) -> None:
    (suite / "vehicle_sn").write_text("not-a-serial\n")

    with pytest.raises(ValidationError):
        Settings()


def test_env_overrides_vehicle_sn(suite: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (suite / "vehicle_sn").write_text(VALID_SERIAL + "\n")
    monkeypatch.setenv("UAS_ID", OTHER_SERIAL)

    assert Settings().uas_id == OTHER_SERIAL
