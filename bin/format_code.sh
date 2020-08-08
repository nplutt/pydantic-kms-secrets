#!/usr/bin/env bash
pipenv run black pydantic_kms_secrets/ tests/
pipenv run isort .