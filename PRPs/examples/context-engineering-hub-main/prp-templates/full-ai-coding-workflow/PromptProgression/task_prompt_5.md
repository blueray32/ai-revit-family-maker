CREATE utils/file_reader.py:

- CREATE: Single responsibility file reading module
- IMPLEMENT: read_file(file_path) -> str with error handling
- VALIDATE: python -c "from utils.file_reader import read_file; print(len(read_file('PRPs/templates/prp_base.md')))"

CREATE utils/text_analyzer.py:

- CREATE: Text analysis functions module
- IMPLEMENT: count_words(text), count_lines(text), count_chars(text)
- VALIDATE: python -c "from utils.text_analyzer import count_words; print(count_words('hello world test'))"

UPDATE utils/file_stats.py:

- FIND: def get_file_stats(file_path):
- REPLACE: Use file_reader.read_file() and text_analyzer functions
- VALIDATE: python -c "from utils.file_stats import get_file_stats; print(get_file_stats('PRPs/templates/prp_base.md'))"

REMOVE main.py:

- FIND: def get_word_count(file_path):
- DELETE: Remove duplicate function (use utils/file_stats instead)
- VALIDATE: uv run python main.py -f PRPs/templates/prp_base.md

CREATE tests/test_file_reader.py:

- IMPLEMENT: test_read_file_success, test_file_not_found, test_encoding_error
- VALIDATE: uv run pytest tests/test_file_reader.py -v

CREATE tests/test_text_analyzer.py:

- IMPLEMENT: test_count_words, test_count_lines, test_count_chars, test_empty_text
- VALIDATE: uv run pytest tests/test_text_analyzer.py -v

VALIDATE ALL:

- VALIDATE: uv run pytest tests/ -v

Validation:

- Each module validated individually
- Integration validated through file_stats.py
- Full CLI validated end-to-end
- All tests must pass before completion
