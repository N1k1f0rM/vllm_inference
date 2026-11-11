#!/bin/bash

set -e

uv run alembic -c app/alembic.ini upgrade head

exec "$@"