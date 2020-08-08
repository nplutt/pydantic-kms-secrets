from typing import Any, Callable, Dict, Generator, Optional

from pydantic_kms_secrets import decrypt


CallableGenerator = Generator[Callable[..., Any], None, None]


class KMSSecretStr:
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(type="string", writeOnly=True)

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> "KMSSecretStr":
        if isinstance(value, cls):
            return value
        return cls(value)

    def __init__(self, value: str):
        self._secret_value = value
        self.decrypted = False

    def __repr__(self) -> str:
        return f"KMSSecretStr('{self}')"

    def __str__(self) -> str:
        return "**********" if self._secret_value else ""

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, KMSSecretStr)
            and self.get_secret_value() == other.get_secret_value()
        )

    def decrypt_secret_value(self, key_id) -> str:
        if not self.decrypted:
            value = decrypt(key_id, self._secret_value)
            self._secret_value = value
            self.decrypted = True
        return self._secret_value

    def get_secret_value(self) -> str:
        return self._secret_value


def decrypt_kms_secrets(settings, key_id: Optional[str] = None):
    """
    Decrypts all of the KMSSecretStr values in the settings
    given a KMS key id
    """
    key_id = key_id or getattr(settings, "secrets_kms_key_id")
    if not key_id:
        raise ValueError(
            "Either key_id function param or the secrets_kms_key_id "
            "value must be set in the settings class"
        )

    for k, v in settings:
        if type(v) == KMSSecretStr:
            v.decrypt_secret_value(key_id)

    return settings
