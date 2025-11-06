UPDATE main.py:

- FIND: input_file = "PRPs/templates/prp_base.md"
- REPLACE: Use argparse.ArgumentParser() with --file/-f argument
- ADD: If no argument provided, throw an error "No input file provided"
- VALIDATE: uv run python main.py --help | grep "file"

TEST main.py:

- VALIDATE: uv run python main.py -f PRPs/templates/prp_base.md
- VALIDATE: uv run python main.py --file PRPs/templates/prp_base.md
