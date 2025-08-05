#!/bin/bash

API_KEY="TEST_KEY" DATABASE_NAME="test.db" PYTHONPATH=. uv run pytest tests/
