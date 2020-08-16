from unittest.mock import patch

from pytest import fixture

from pydantic import BaseSettings
from pydantic_kms_secrets.pydantic import KMSSecretStr, decrypt_kms_secrets


@fixture
def kms_secret_str():
    yield KMSSecretStr("secret-value")


def test_kms_secret_str_initialize(kms_secret_str):
    assert kms_secret_str._secret_value == "secret-value"
    assert kms_secret_str.decrypted is False


def test_kms_secret_str_to_string(kms_secret_str):
    assert str(kms_secret_str) == "**********"


def test_kms_secret_str_equal(kms_secret_str):
    assert kms_secret_str == kms_secret_str
    assert kms_secret_str != str(kms_secret_str)


@patch("pydantic_kms_secrets.pydantic.decrypt", return_value="decrypted")
def test_kms_secret_decrypt_secret_value(decrypt_mock, kms_secret_str):
    assert kms_secret_str.decrypt_secret_value("key") == "decrypted"
    assert kms_secret_str._secret_value == "decrypted"
    assert kms_secret_str.decrypted is True

    # Call decrypt key again to check that decrypt is only called once
    kms_secret_str.decrypt_secret_value("key")

    decrypt_mock.assert_called_once_with("key", "secret-value")


def test_kms_secret_str_get_secret_value(kms_secret_str):
    assert kms_secret_str.get_secret_value() == "secret-value"


@patch("pydantic_kms_secrets.pydantic.decrypt", return_value="decrypted")
def test_decrypt_kms_secrets(decrypt_mock):
    class Settings(BaseSettings):
        env: str
        secrets_kms_key_id: str
        kms_secret_1: KMSSecretStr
        kms_secret_2: KMSSecretStr

    mock_settings = Settings(
        env="env",
        secrets_kms_key_id="fake-key-id",
        kms_secret_1=KMSSecretStr("secret-1"),
        kms_secret_2=KMSSecretStr("secret-2"),
    )

    settings = decrypt_kms_secrets(mock_settings)

    assert settings.kms_secret_1.get_secret_value() == "decrypted"
    assert settings.kms_secret_2.get_secret_value() == "decrypted"
    assert settings.env == "env"

    assert decrypt_mock.call_count == 2
    decrypt_mock.assert_any_call("fake-key-id", "secret-1")
