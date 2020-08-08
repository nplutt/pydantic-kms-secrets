import base64

import boto3


def encrypt(key_id: str, value: str) -> str:
    """
    Takes a KMS key id, encrypts the value using it and
    returns the encrypted value
    """
    client = boto3.client("kms")
    response = client.encrypt(KeyId=key_id, Plaintext=value.encode())
    return base64.b64encode(response["CiphertextBlob"]).decode("utf-8")


def decrypt(key_id: str, value: str) -> str:
    """
    Takes a KMS key id, decrypts the value using it and
    returns the decrypted value
    """
    client = boto3.client("kms")
    response = client.decrypt(
        KeyId=key_id, CiphertextBlob=bytes(base64.b64decode(value)),
    )
    return response["Plaintext"].decode("utf-8")
