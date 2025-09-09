# !/bin/bash
set -eo pipefail

COLOR_BLUE=$(tput setaf 2)
COLOR_NC=$(tput sgr0)

cd "$(dirname "$0")/.."

echo "Starting ruff"
uv run ruff check --select I --fix
uv run ruff check --fix
echo "OK"

echo "Starting mypy"
uv run mypy .
echo "OK"

echo "Start pytest with coverage"
uv run coverage run -m pytest .
uv run coverage report -m
uv run coverage html
echo "OK"

echo "${COLOR_BLUE}ALL tests passed successfully!${COLOR_NC}"