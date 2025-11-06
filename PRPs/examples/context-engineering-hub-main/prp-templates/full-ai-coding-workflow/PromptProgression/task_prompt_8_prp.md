name: "File Statistics and Sentiment Analysis Tool - Complete Implementation"
description: |

## Purpose

Implement a complete file analysis tool that provides word statistics, frequency analysis, and sentiment analysis using Anthropic's Claude API. This PRP consolidates all functionality from tasks 1-7 into a single, comprehensive implementation.

## Core Principles

1. **KISS + LLM Trust**: Minimal parsing, trust Claude responses, let errors bubble up
2. **Modular Architecture**: Clean separation of concerns across utility modules
3. **Complete Data Flow**: Full text analysis without truncation or over-parsing
4. **Progressive Validation**: Each component validates independently and together
5. **Environment Security**: API keys loaded securely via environment variables

---

## Goal

Create a complete file analysis CLI tool that:

- Reads any text file and provides comprehensive statistics
- Shows word frequency analysis for all words (not truncated)
- Performs sentiment analysis using Anthropic Claude API
- Maintains clean modular architecture with comprehensive test coverage

## Why

- Demonstrates complete text analysis pipeline from file I/O to AI analysis
- Shows proper LLM integration with trust-based parsing patterns
- Establishes reusable modular architecture for text processing tools
- Provides foundation for more complex document analysis workflows

## What

CLI tool with three analysis modes:

- Basic stats: word count, line count, character count
- Frequency analysis: complete word frequency distribution
- Sentiment analysis: AI-powered sentiment with confidence and reasoning

### Success Criteria

- [ ] All files under 200 lines following single responsibility principle
- [ ] Complete test coverage with pytest
- [ ] CLI accepts -f/--file, -w/--words, -s/--sentiment flags
- [ ] No truncation of data - show all words, send full text to LLM
- [ ] Minimal parsing - trust Claude JSON responses, strip markdown only
- [ ] Environment-based API key management with python-dotenv
- [ ] All validation gates pass

## All Needed Context

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- file: PRPs/ai_docs/anthropic_api/quickstart.md
  why: Basic API setup and authentication patterns

- file: PRPs/ai_docs/anthropic_api/messages_api.md
  why: Messages API patterns for sentiment analysis implementation

- file: PRPs/ai_docs/anthropic_api/authentication.md
  why: Environment variable setup and security best practices

- file: PRPs/ai_docs/task_best_practices/task_structure.md
  why: Task structure format and validation patterns

- file: PRPs/templates/prp_base.md
  why: PRP template structure and validation loop patterns
```

### Desired Codebase Structure

```bash
sean/
├── main.py                    # CLI entry point with argparse
├── pyproject.toml            # UV project with anthropic, python-dotenv, pytest
├── utils/
│   ├── __init__.py
│   ├── file_reader.py        # File I/O with error handling
│   ├── text_analyzer.py      # Text processing and word frequency
│   ├── sentiment_analyzer.py # Anthropic API integration
│   └── file_stats.py        # Orchestration layer
└── tests/
    ├── __init__.py
    ├── test_file_reader.py
    ├── test_text_analyzer.py
    ├── test_sentiment_analyzer.py
    └── test_file_stats.py
```

### Known Gotchas & LLM Trust Patterns

````python
# CRITICAL: Trust Claude responses - minimal parsing only
# GOOD: Strip markdown blocks, parse JSON directly
response_text = message.content[0].text.strip()
if response_text.startswith("```json"):
    response_text = response_text.replace("```json", "").replace("```", "").strip()
return json.loads(response_text)  # Let JSON errors bubble up

# CRITICAL: Send full text to LLM - no truncation
# GOOD: Send complete content for accurate analysis
messages=[{"role": "user", "content": f"Analyze: {text}"}]  # Full text

# CRITICAL: Show all data - no artificial limits
# GOOD: Display complete word frequency
for word, count in sorted_words:  # All words, not [:20]
    print(f"{word}: {count}")

# CRITICAL: Environment security
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
````

## Implementation Blueprint

### Data Models and Structure

Clean modular architecture with single responsibility:

```python
# utils/file_reader.py - File I/O only
def read_file(file_path: str) -> str:
    """Read file with proper error handling"""

# utils/text_analyzer.py - Text processing only
def count_words(text: str) -> int:
def count_lines(text: str) -> int:
def count_chars(text: str) -> int:
def get_word_frequency(text: str) -> dict:

# utils/sentiment_analyzer.py - AI integration only
def analyze_sentiment(text: str) -> dict:
    """Claude API call with minimal parsing"""

# utils/file_stats.py - Orchestration layer
def get_file_stats(file_path: str, include_frequency=False, include_sentiment=False) -> dict:
    """Combines all analysis capabilities"""
```

### List of Tasks to Complete the PRP

```yaml
Task 1 - Setup Dependencies:
UPDATE pyproject.toml:
  - ENSURE: uv add anthropic python-dotenv pytest
  - VALIDATE: grep -E "(anthropic|python-dotenv|pytest)" pyproject.toml

Task 2 - Create File Reader Module:
CREATE utils/file_reader.py:
  - IMPLEMENT: read_file(file_path) with UTF-8 encoding
  - IMPLEMENT: Proper error handling for FileNotFoundError
  - VALIDATE: python -c "from utils.file_reader import read_file; print(len(read_file('PRPs/templates/prp_base.md')))"

Task 3 - Create Text Analyzer Module:
CREATE utils/text_analyzer.py:
  - IMPLEMENT: count_words, count_lines, count_chars functions
  - IMPLEMENT: get_word_frequency with lowercase normalization and punctuation stripping
  - VALIDATE: python -c "from utils.text_analyzer import get_word_frequency; print(get_word_frequency('Hello world. Hello!'))"

Task 4 - Create Sentiment Analyzer Module:
CREATE utils/sentiment_analyzer.py:
  - IMPLEMENT: Load environment with python-dotenv
  - IMPLEMENT: analyze_sentiment using Claude API with full text (no truncation)
  - IMPLEMENT: Minimal parsing - strip markdown blocks only, let JSON errors bubble up
  - CONTEXT: Follow patterns from PRPs/ai_docs/anthropic_api/messages_api.md
  - VALIDATE: python -c "from utils.sentiment_analyzer import analyze_sentiment; print(analyze_sentiment('I love this!'))"

Task 5 - Create File Stats Orchestrator:
CREATE utils/file_stats.py:
  - IMPLEMENT: get_file_stats with optional frequency and sentiment parameters
  - IMPORT: All utility functions from other modules
  - IMPLEMENT: Proper error handling for empty files
  - VALIDATE: python -c "from utils.file_stats import get_file_stats; print(get_file_stats('PRPs/templates/prp_base.md', True, True))"

Task 6 - Create CLI Interface:
CREATE main.py:
  - IMPLEMENT: argparse with -f/--file, -w/--words, -s/--sentiment flags
  - IMPLEMENT: Display all stats with proper formatting
  - IMPLEMENT: Show ALL words in frequency analysis (no truncation)
  - VALIDATE: uv run python main.py -f PRPs/templates/prp_base.md -w -s

Task 7 - Create Complete Test Suite:
CREATE tests/test_file_reader.py:
  - IMPLEMENT: test_read_file_success, test_file_not_found, test_encoding_error
  - VALIDATE: uv run pytest tests/test_file_reader.py -v

CREATE tests/test_text_analyzer.py:
  - IMPLEMENT: test_count_functions, test_word_frequency, test_empty_text
  - VALIDATE: uv run pytest tests/test_text_analyzer.py -v

CREATE tests/test_sentiment_analyzer.py:
  - IMPLEMENT: Mock Claude API responses with realistic JSON
  - IMPLEMENT: Test markdown stripping and error bubbling
  - VALIDATE: uv run pytest tests/test_sentiment_analyzer.py -v

CREATE tests/test_file_stats.py:
  - IMPLEMENT: Integration tests with mocked dependencies
  - VALIDATE: uv run pytest tests/test_file_stats.py -v
```

### Implementation Patterns

````python
# Pattern 1: LLM Trust with Minimal Parsing
def analyze_sentiment(text: str) -> dict:
    # Send full text - no truncation
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""Analyze sentiment and respond with JSON:
{{"sentiment": "positive|negative|neutral", "confidence": 0.0-1.0, "reasoning": "brief explanation"}}

Text: {text}"""  # Full text, no [:1000] truncation
        }]
    )

    # Minimal parsing - trust Claude
    response_text = message.content[0].text.strip()
    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "").replace("```", "").strip()

    return json.loads(response_text)  # Let errors bubble up

# Pattern 2: Complete Data Display
def display_word_frequency(word_freq: dict):
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_words:  # ALL words, no [:20] limit
        print(f"{word}: {count}")

# Pattern 3: Environment Security
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    return {"sentiment": "error", "reasoning": "ANTHROPIC_API_KEY not set"}
````

## Validation Loop

### Level 1: Module Validation

```bash
# After each module creation:
uv run python -c "from utils.module_name import function_name; print('✓ Import successful')"
uv run pytest tests/test_module_name.py -v
```

### Level 2: Integration Validation

```bash
# Test CLI with all flags:
uv run python main.py -f PRPs/templates/prp_base.md
uv run python main.py -f PRPs/templates/prp_base.md -w
uv run python main.py -f PRPs/templates/prp_base.md -s
uv run python main.py -f PRPs/templates/prp_base.md -w -s
```

### Level 3: Complete Test Suite

```bash
# All tests must pass:
uv run pytest tests/ -v
# Expected: All tests pass, no truncation, full LLM trust working
```

## Final Validation Checklist

- [ ] Dependencies installed: `grep -E "(anthropic|python-dotenv)" pyproject.toml`
- [ ] All modules import successfully
- [ ] Complete test coverage: `uv run pytest tests/ -v`
- [ ] CLI shows all word frequencies (no truncation)
- [ ] Sentiment analysis works with full text and minimal parsing
- [ ] Environment variables loaded securely
- [ ] JSON parsing errors bubble up naturally (no defensive fallbacks)
- [ ] All files follow single responsibility principle

---

## Anti-Patterns to Avoid

- ❌ Don't truncate text sent to LLM (no `text[:1000]`)
- ❌ Don't limit word frequency display (no `[:20]`)
- ❌ Don't add defensive JSON parsing fallbacks - trust Claude
- ❌ Don't hardcode API keys - use environment variables
- ❌ Don't mix concerns - keep modules focused on single responsibility
- ❌ Don't skip tests - comprehensive coverage required
