from unittest.mock import MagicMock, patch

from pytest import mark

from src.cli import main, parse_args


@mark.parametrize(
    ("args", "decrypt_called", "encrypt_called", "expected"),
    (
        # Decrypt flag set to True
        (
            MagicMock(decrypt=True, encrypt=False, key_id="key", value="val"),
            True,
            False,
            "decrypted_value",
        ),
        # Encrypt flag set to True
        (
            MagicMock(decrypt=False, encrypt=True, key_id="key", value="val"),
            False,
            True,
            "encrypted_value",
        ),
        # Both flags set to False
        (
            MagicMock(decrypt=False, encrypt=False, key_id="key", value="val"),
            False,
            False,
            "ERROR: Either --decrypt or --encrypt flag must be set",
        ),
        # Both flags set to True
        (
            MagicMock(decrypt=True, encrypt=True, key_id="key", value="val"),
            False,
            False,
            "ERROR: Only one of --decrypt or --encrypt flags can be set",
        ),
    ),
)
@patch("src.cli.encrypt", return_value="encrypted_value")
@patch("src.cli.decrypt", return_value="decrypted_value")
def test_parse_args(
    decrypt_mock, encrypt_mock, args, decrypt_called, encrypt_called, expected,
):
    assert parse_args(args) == expected

    if decrypt_called:
        decrypt_mock.assert_called_once_with(args.key_id, args.value)
    else:
        decrypt_mock.assert_not_called()

    if encrypt_called:
        encrypt_mock.assert_called_once_with(args.key_id, args.value)
    else:
        encrypt_mock.assert_not_called()


@patch("src.cli.print")
@patch("src.cli.parse_args")
@patch("src.cli.initialize_parser")
def test_main(
    initialize_parser_mock, parse_args_mock, print_mock,
):
    parser = MagicMock()
    parser.parse_args.return_value = "args"
    initialize_parser_mock.return_value = parser
    parse_args_mock.return_value = "result"

    main()

    initialize_parser_mock.assert_called_once_with()
    parser.parse_args.assert_called_once_with()
    parse_args_mock.assert_called_once_with("args")
    print_mock.assert_called_once_with("result")
