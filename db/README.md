# Archon Database Migrations

Professional-grade database migration system for the Archon RAG/document crawling platform.

## Features

✅ **Automatic Migration Detection** - Scans `migrations/` directory for SQL files
✅ **Checksum Validation** - Prevents re-running modified migrations
✅ **Dry-Run Mode** - Preview changes before applying
✅ **Status Checking** - See applied vs pending migrations
✅ **Rollback Support** - Reverse migrations with rollback files
✅ **Transaction Safety** - Each migration runs in a transaction
✅ **Migration Tracking** - Uses `archon_migrations` table

---

## Quick Start

### 1. Install Dependencies

```bash
pip install psycopg2-binary python-dotenv
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file in the `db/` directory:

```bash
# Your Supabase project URL
SUPABASE_URL=https://xxxxx.supabase.co

# Service role key (NOT the anon key!)
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Security Note**: The service role key has admin access. Never commit it to git!

### 3. Check Status

```bash
python migrate.py status
```

Output:
```
======================================================================
MIGRATION STATUS
======================================================================

Total migrations: 11
Applied: 8
Pending: 3

--- Applied Migrations ---
  ✓ 001_add_source_url_display_name.sql (applied 2025-01-15 10:30:00)
  ✓ 002_add_hybrid_search_tsvector.sql (applied 2025-01-15 10:30:15)
  ...

--- Pending Migrations ---
  ○ 009_add_cascade_delete_constraints.sql
  ○ 010_add_provider_placeholders.sql
  ○ 011_add_page_metadata_table.sql

======================================================================
```

### 4. Preview Migrations (Dry Run)

```bash
python migrate.py up --dry-run
```

This shows what **would** be applied without actually running it.

### 5. Apply Migrations

```bash
python migrate.py up
```

Output:
```
Found 3 pending migration(s)

Applying: 009_add_cascade_delete_constraints.sql
  Name: add_cascade_delete_constraints
  Checksum: a1b2c3d4e5f6...
  ✓ Applied successfully

Applying: 010_add_provider_placeholders.sql
  Name: add_provider_placeholders
  Checksum: f6e5d4c3b2a1...
  ✓ Applied successfully

Applying: 011_add_page_metadata_table.sql
  Name: add_page_metadata_table
  Checksum: 1a2b3c4d5e6f...
  ✓ Applied successfully

✓ Successfully applied 3 migration(s)
```

---

## Commands

### `python migrate.py status`
Check which migrations are applied and which are pending.

### `python migrate.py up`
Apply all pending migrations in order.

### `python migrate.py up --dry-run`
Preview migrations without applying them (safe to run anytime).

### `python migrate.py down <migration_file>`
Rollback a specific migration (requires rollback file).

Example:
```bash
python migrate.py down 011_add_page_metadata_table.sql
```

### `python migrate.py create <name>`
Create a new migration file with the next available number.

Example:
```bash
python migrate.py create add_user_preferences
# Creates: 012_add_user_preferences.sql
```

---

## Migration File Format

Migrations must follow this naming convention:

```
NNN_descriptive_name.sql
```

Where:
- `NNN` = 3-digit number (001, 002, 003, etc.)
- `descriptive_name` = snake_case description
- `.sql` = SQL file extension

**Examples**:
- ✅ `001_add_source_url_display_name.sql`
- ✅ `010_add_provider_placeholders.sql`
- ✅ `011_add_page_metadata_table.sql`
- ❌ `add_column.sql` (missing number)
- ❌ `1_add_column.sql` (number too short)

---

## Directory Structure

```
db/
├── migrate.py                    # Migration runner script
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (gitignored)
├── .env.example                  # Example environment file
├── README.md                     # This file
├── migrations/                   # Migration SQL files
│   ├── 001_add_source_url_display_name.sql
│   ├── 002_add_hybrid_search_tsvector.sql
│   ├── 003_ollama_add_columns.sql
│   ├── 004_ollama_migrate_data.sql
│   ├── 005_ollama_create_functions.sql
│   ├── 006_ollama_create_indexes_optional.sql
│   ├── 007_add_priority_column_to_tasks.sql
│   ├── 008_add_migration_tracking.sql
│   ├── 009_add_cascade_delete_constraints.sql
│   ├── 010_add_provider_placeholders.sql
│   └── 011_add_page_metadata_table.sql
└── migrations/rollbacks/         # Rollback SQL files (optional)
    └── 011_add_page_metadata_table.sql
```

---

## Creating Migrations

### Automatic Creation

```bash
python migrate.py create add_new_feature
```

This creates a template file: `NNN_add_new_feature.sql`

### Manual Creation

1. Create file: `migrations/012_your_migration_name.sql`
2. Add SQL content
3. Include tracking insert at the end:

```sql
-- 012_your_migration_name.sql
BEGIN;

-- Your migration SQL here
ALTER TABLE your_table ADD COLUMN new_column TEXT;

-- Record migration
INSERT INTO archon_migrations (version, migration_name)
VALUES ('0.1.0', '012_your_migration_name.sql')
ON CONFLICT (version, migration_name) DO NOTHING;

COMMIT;
```

---

## Rollback Support

To enable rollback for a migration:

1. Create inverse SQL in `migrations/rollbacks/`
2. Match the filename exactly

Example:

**Forward** (`migrations/011_add_page_metadata_table.sql`):
```sql
CREATE TABLE archon_page_metadata (...);
```

**Rollback** (`migrations/rollbacks/011_add_page_metadata_table.sql`):
```sql
DROP TABLE IF EXISTS archon_page_metadata CASCADE;

DELETE FROM archon_migrations
WHERE migration_name = '011_add_page_metadata_table.sql';
```

Then rollback with:
```bash
python migrate.py down 011_add_page_metadata_table.sql
```

---

## Safety Features

### 1. Checksum Validation
Each migration's content is checksummed. If you modify an already-applied migration, the runner will detect it and refuse to re-run it.

```
WARNING: Migration 005_ollama_create_functions.sql has been modified!
  Applied checksum:  a1b2c3d4e5f6...
  Current checksum:  f6e5d4c3b2a1...
  This migration will be SKIPPED to prevent re-running modified SQL
```

### 2. Transaction Safety
Each migration runs in a transaction. If it fails, changes are rolled back automatically.

### 3. Dry-Run Mode
Always preview with `--dry-run` first when applying migrations to production.

### 4. Migration Tracking
The `archon_migrations` table tracks:
- Which migrations have been applied
- When they were applied
- Checksum for validation

---

## Troubleshooting

### "ERROR: Missing required environment variables"
**Solution**: Create a `.env` file with `SUPABASE_URL` and `SUPABASE_SERVICE_KEY`.

### "ERROR: psycopg2 not installed"
**Solution**: `pip install psycopg2-binary`

### "WARNING: Skipping invalid migration filename"
**Solution**: Ensure filename follows `NNN_name.sql` format (e.g., `001_add_column.sql`)

### "ERROR: Migration has been modified"
**Solution**: Don't modify migrations after they've been applied. Create a new migration instead.

### Connection Timeout
**Solution**: Check your Supabase project is running and the service key is correct.

### Migration Fails Mid-Way
**Solution**: The transaction is rolled back automatically. Fix the SQL and run `python migrate.py up` again.

---

## Best Practices

1. **Never modify applied migrations** - Create new migrations instead
2. **Use descriptive names** - `add_user_preferences` not `update_db`
3. **Test with dry-run first** - Always run `--dry-run` before applying
4. **Keep migrations small** - One logical change per migration
5. **Include comments** - Explain WHY, not just WHAT
6. **Create rollbacks** - For critical migrations, create rollback files
7. **Run migrations in order** - The system enforces this automatically

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Apply Migrations

on:
  push:
    branches: [main]
    paths:
      - 'db/migrations/**'

jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          cd db
          pip install -r requirements.txt

      - name: Check migration status
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_SERVICE_KEY: ${{ secrets.SUPABASE_SERVICE_KEY }}
        run: |
          cd db
          python migrate.py status

      - name: Apply migrations
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_SERVICE_KEY: ${{ secrets.SUPABASE_SERVICE_KEY }}
        run: |
          cd db
          python migrate.py up
```

---

## Advanced Usage

### Custom Connection String

If you're not using Supabase, you can modify the `get_connection_string()` function in `migrate.py` to return your PostgreSQL connection string directly.

### Parallel Execution

Migrations run sequentially by design for safety. Do not attempt to run migrations in parallel.

### Large Migrations

For migrations that modify millions of rows:
1. Test on a staging database first
2. Run during low-traffic periods
3. Consider breaking into smaller migrations
4. Monitor database performance during application

---

## Support

For issues or questions:
1. Check this README first
2. Review migration file comments
3. Check Supabase dashboard SQL Editor for errors
4. Open an issue in the repository

---

## License

Part of the Archon project. See main project LICENSE.
