@echo off

poetry env activate
poetry install
poetry run pytest -rx