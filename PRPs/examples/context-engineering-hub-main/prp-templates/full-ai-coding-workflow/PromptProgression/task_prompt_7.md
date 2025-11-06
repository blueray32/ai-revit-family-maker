CONTEXT REFERENCES:

- PRPs/ai_docs/anthropic_api/quickstart.md - Basic API setup and authentication
- PRPs/ai_docs/anthropic_api/messages_api.md - Messages API patterns for sentiment analysis
- PRPs/ai_docs/anthropic_api/authentication.md - Environment variable setup

UPDATE pyproject.toml:

- ADD: uv add anthropic python-dotenv
- VALIDATE: uv add anthropic python-dotenv && grep -E "(anthropic|python-dotenv)" pyproject.toml

CREATE utils/sentiment_analyzer.py:

- CREATE: Anthropic API sentiment analysis module with dotenv support
- IMPLEMENT: analyze_sentiment(text) -> dict function using Claude API
- IMPLEMENT: Load ANTHROPIC_API_KEY from environment using python-dotenv
- IMPLEMENT: Send FULL text to LLM (no truncation), trust JSON response with minimal parsing
- IMPLEMENT: Strip markdown ```json blocks only, let JSON errors bubble up as exceptions
- CONTEXT: Follow patterns from PRPs/ai_docs/anthropic_api/messages_api.md
- VALIDATE: python -c "from utils.sentiment_analyzer import analyze_sentiment; print(analyze_sentiment('I love this product!'))"

UPDATE utils/file_stats.py:

- ADD: include_sentiment parameter to get_file_stats(file_path, include_frequency=False, include_sentiment=False)
- IMPORT: analyze_sentiment from sentiment_analyzer
- IMPLEMENT: Add sentiment_analysis to return dict when include_sentiment=True
- VALIDATE: python -c "from utils.file_stats import get_file_stats; print('sentiment_analysis' in get_file_stats('PRPs/templates/prp_base.md', False, True))"

UPDATE main.py:

- ADD: parser.add_argument("--sentiment", "-s", action="store_true", help="Show sentiment analysis")
- FIND: stats = get_file_stats(args.file, args.words)
- REPLACE: stats = get_file_stats(args.file, args.words, args.sentiment)
- ADD: if args.sentiment conditional to print sentiment analysis results
- ENSURE: Show ALL words when --words flag used (no truncation limit)
- VALIDATE: uv run python main.py -f PRPs/templates/prp_base.md -s

CREATE tests/test_sentiment_analyzer.py:

- IMPLEMENT: test_analyze_sentiment with mock API responses
- IMPLEMENT: Mock should return realistic Claude JSON responses (with/without markdown)
- IMPLEMENT: Test error cases - let JSON parsing errors bubble up naturally
- CONTEXT: Use mock patterns to avoid API calls in tests
- VALIDATE: uv run pytest tests/test_sentiment_analyzer.py -v

UPDATE tests/test_file_stats.py:

- ADD: test_get_file_stats_with_sentiment function with mocked API
- VALIDATE: uv run pytest tests/test_file_stats.py::test_get_file_stats_with_sentiment -v

VALIDATE ALL:

- VALIDATE: uv run pytest tests/ -v
