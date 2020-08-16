import argparse

from pydantic_kms_secrets.kms import decrypt, encrypt


def initialize_parser() -> argparse.ArgumentParser:
    """
    Initializes the arg parser and adds arguments
    """
    parser = argparse.ArgumentParser(
        add_help="--help",
        description="Tool to encrypt and decrypt secrets via a KMS key",
    )

    parser.add_argument(
        "-k", "--key-id", dest="key_id", required=True, help="ID of the KMS key to use",
    )

    parser.add_argument(
        "-v", "--value", dest="value", required=True, help="The value to be encrypted",
    )

    parser.add_argument(
        "-e",
        "--encrypt",
        dest="encrypt",
        action="store_const",
        const=True,
        help="Set to encrypt value",
    )

    parser.add_argument(
        "-d",
        "--decrypt",
        dest="decrypt",
        action="store_const",
        const=True,
        help="Set to decrypt value",
    )

    return parser


def parse_args(args) -> str:
    """
    Parses incoming args and returns the appropriate value
    depending on the passed args.
    """
    if args.decrypt and args.encrypt:
        return "ERROR: Only one of --decrypt or --encrypt flags can be set"

    if args.decrypt:
        decrypted_value = decrypt(args.key_id, args.value)
        return decrypted_value

    elif args.encrypt:
        encrypted_value = encrypt(args.key_id, args.value)
        return encrypted_value

    else:
        return "ERROR: Either --decrypt or --encrypt flag must be set"


def main() -> None:
    """
    Initializes the parser, parses the incomin args, and prints
    the result for the end user
    """
    parser = initialize_parser()
    args = parser.parse_args()

    result = parse_args(args)
    print(result)
