UPDATE utils/text_analyzer.py:

- ADD: get_word_frequency(text) -> dict function
- IMPLEMENT: Return {word: count} dict, normalize to lowercase, strip punctuation
- VALIDATE: python -c "from utils.text_analyzer import get_word_frequency; print(get_word_frequency('Hello world. Hello!'))"

UPDATE utils/file_stats.py:

- ADD: include_frequency parameter to get_file_stats(file_path, include_frequency=False)
- IMPORT: get_word_frequency from text_analyzer
- IMPLEMENT: Add word_frequency to return dict when include_frequency=True show all words
- VALIDATE: python -c "from utils.file_stats import get_file_stats; print('word_frequency' in get_file_stats('PRPs/templates/prp_base.md', True))"

UPDATE main.py:

- ADD: parser.add_argument("--words", "-w", action="store_true", help="Show word frequency")
- FIND: stats = get_file_stats(args.file)
- REPLACE: stats = get_file_stats(args.file, args.words)
- ADD: if args.words conditional to print formatted word frequency table
- VALIDATE: uv run python main.py -f PRPs/templates/prp_base.md -w | head -5

UPDATE tests/test_text_analyzer.py:

- ADD: test_get_word_frequency function
- IMPLEMENT: test_basic_frequency, test_case_insensitive, test_punctuation_stripped
- VALIDATE: uv run pytest tests/test_text_analyzer.py::test_get_word_frequency -v

UPDATE tests/test_file_stats.py:

- ADD: test_get_file_stats_with_frequency function
- IMPLEMENT: Test include_frequency=True returns word_frequency key
- VALIDATE: uv run pytest tests/test_file_stats.py::test_get_file_stats_with_frequency -v

VALIDATE ALL:

- VALIDATE: uv run pytest tests/ -v
