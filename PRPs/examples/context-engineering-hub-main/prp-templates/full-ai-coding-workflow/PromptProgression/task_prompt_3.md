CREATE utils/file_stats.py:
- CREATE: New module with get_file_stats(file_path) function  
- IMPLEMENT: Return dict with {word_count, line_count, char_count}
- VALIDATE: python -c "from utils.file_stats import get_file_stats; print(get_file_stats('PRPs/templates/prp_base.md'))"

UPDATE main.py:
- FIND: from utils.file_stats import get_file_stats
- ADD: Import statement after argparse import
- FIND: word_count = get_word_count(args.file)
- REPLACE: stats = get_file_stats(args.file)
- FIND: print(f"Total word count: {word_count}")
- REPLACE: Print all stats (words, lines, chars)
- VALIDATE: uv run python main.py -f PRPs/templates/prp_base.md | grep -E "(words|lines|chars)"