import argparse
from os import environ

from pydantic_kms_secrets import decrypt, encrypt


parser = argparse.ArgumentParser(
    add_help='--help',
    description='Tool to encrypt and decrypt secrets via a KMS key',
)

parser.add_argument(
    '-k', '--key-id',
    dest='key_id',
    help='ID of the KMS key to use',
)

parser.add_argument(
    '-v', '--value',
    dest='value',
    required=True,
    help='The value to be encrypted',
)

parser.add_argument(
    '-e', '--encrypt',
    dest='encrypt',
    action='store_const',
    const=True,
    help='Set to encrypt value',
)

parser.add_argument(
    '-d', '--decrypt',
    dest='decrypt',
    action='store_const',
    const=True,
    help='Set to decrypt value',
)


def main():
    args = parser.parse_args()

    key_id = args.key_id or environ.get('SECRETS_KMS_KEY_ID')
    if not key_id:
        raise argparse.ArgumentError(
            'Either the --key-id flag or the SECRETS_KMS_KEY_ID '
            'environment variable must be set'
        )

    if args.decrypt:
        decrypted_value = decrypt(args.key_id, args.value)
        print(decrypted_value)

    elif args.encrypt:
        encrypted_value = encrypt(args.key_id, args.value)
        print(encrypted_value)

    else:
        raise argparse.ArgumentError(
            'Either --decrypt or --encrypt flag must be set'
        )
