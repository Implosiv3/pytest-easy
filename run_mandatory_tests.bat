@echo off

set library=pytest_easy

poetry env activate
poetry install --with dev,test
poetry run pytest-easy-init-log-file "%library%"
poetry run pytest-easy-run-tests-isolated --mandatory-only --stop-if-failed