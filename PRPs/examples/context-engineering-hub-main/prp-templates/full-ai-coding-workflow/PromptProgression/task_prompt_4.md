UPDATE pyproject.toml:
- FIND: [build-system]
- ADD: pytest to dev dependencies using uv add pytest --dev
- VALIDATE: uv add pytest --dev && grep "pytest" pyproject.toml

CREATE tests/test_file_stats.py:
- CREATE: Basic test file with test_get_file_stats function
- IMPLEMENT: Test word_count, line_count, char_count for known file
- VALIDATE: uv run pytest tests/test_file_stats.py -v