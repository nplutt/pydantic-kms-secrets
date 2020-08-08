from unittest.mock import patch, MagicMock
from pydantic_kms_secrets.kms import encrypt, decrypt


ENCRYPTED_BYTES = \
    b'\x01\x02\x02\x00x@\xcau^\xa5\x9c\xdd\x1e\xed\xe0\x00w]A\xba-\x83\x89\xb2' \
    b'N\x98<?\x10vkL\xd3\x87\x03:\xa6\x01X\x12\xc7Y\x1d\x17\xe2a\xef\xa0Pz\xef\x81' \
    b'\xc2\x04\x00\x00\x00c0a\x06\t*\x86H\x86\xf7\r\x01\x07\x06\xa0T0R\x02' \
    b'\x01\x000M\x06\t*\x86H\x86\xf7\r\x01\x07\x010\x1e\x06\t`\x86H\x01e' \
    b'\x03\x04\x01.0\x11\x04\x0c\x13\x07d$Du\x10\xf1\xdb\x91\x932\x02\x01\x10\x80' \
    b' \x0c\x81:G3b(\x01\xeb\xe1\xa6\x1c\x03a\xa7R\x84\xbcVT\xe4AG\x9fn\x1b|' \
    b'\x143\x96\x11\xd0'

ENCRYPTED_STRING = \
    'AQICAHhAynVepZzdHu3gAHddQbotg4myTpg8PxB2a0zThwM6pgFYEsdZHRfiYe+gUHrvgc' \
    'IEAAAAYzBhBgkqhkiG9w0BBwagVDBSAgEAME0GCSqGSIb3DQEHATAeBglghkgBZQMEAS4w' \
    'EQQMEwdkJER1EPHbkZMyAgEQgCAMgTpHM2IoAevhphwDYadShLxWVORBR59uG3wUM5YR0A=='


@patch('pydantic_kms_secrets.kms.boto3')
def test_encrypt(boto3_mock):
    client_mock = MagicMock()
    client_mock.encrypt.return_value = {
        'CiphertextBlob': ENCRYPTED_BYTES,
    }
    boto3_mock.client.return_value = client_mock

    assert encrypt('key', 'value') == ENCRYPTED_STRING

    client_mock.encrypt.assert_called_once_with(
        KeyId='key',
        Plaintext=b'value',
    )


@patch('pydantic_kms_secrets.kms.boto3')
def test_decrypt(boto3_mock):
    client_mock = MagicMock()
    client_mock.decrypt.return_value = {
        'Plaintext': b'stuff',
    }
    boto3_mock.client.return_value = client_mock

    assert decrypt('key', ENCRYPTED_STRING) == 'stuff'

    client_mock.decrypt.assert_called_once_with(
        KeyId='key',
        CiphertextBlob=ENCRYPTED_BYTES,
    )
