# Archon Migration System - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Archon Migration System                      │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Developer  │──────│  migrate.py  │──────│   Supabase   │
│   Terminal   │      │   (Runner)   │      │  PostgreSQL  │
└──────────────┘      └──────────────┘      └──────────────┘
                             │
                             │ Reads
                             ▼
                      ┌──────────────┐
                      │ migrations/  │
                      │  001_*.sql   │
                      │  002_*.sql   │
                      │  ...         │
                      └──────────────┘
```

---

## Data Flow

### 1. Status Check Flow
```
User runs: python migrate.py status

migrate.py
  ├─> Connect to Supabase PostgreSQL
  ├─> Query archon_migrations table (applied)
  ├─> Scan migrations/ directory (available)
  ├─> Calculate diff (pending)
  └─> Display results to user
```

### 2. Migration Application Flow
```
User runs: python migrate.py up

migrate.py
  ├─> Get pending migrations
  │
  ├─> For each migration:
  │   ├─> Calculate checksum
  │   ├─> Start transaction
  │   ├─> Execute SQL
  │   ├─> Insert into archon_migrations
  │   ├─> Commit transaction
  │   └─> Report success/failure
  │
  └─> Summary report
```

### 3. Dry-Run Flow
```
User runs: python migrate.py up --dry-run

migrate.py
  ├─> Get pending migrations
  ├─> For each migration:
  │   ├─> Print filename
  │   ├─> Print SQL preview
  │   └─> Skip execution
  └─> Summary (no changes made)
```

---

## Database Schema

### archon_migrations Table
```sql
CREATE TABLE archon_migrations (
    id UUID PRIMARY KEY,
    version VARCHAR(20),            -- e.g., "0.1.0"
    migration_name VARCHAR(255),    -- e.g., "001_add_column.sql"
    applied_at TIMESTAMPTZ,         -- When applied
    checksum VARCHAR(32),           -- MD5 hash of SQL content
    UNIQUE(version, migration_name)
);

-- Indexes
CREATE INDEX idx_archon_migrations_version ON archon_migrations(version);
CREATE INDEX idx_archon_migrations_applied_at ON archon_migrations(applied_at DESC);
```

**Purpose**: Track which migrations have been applied

**Key Fields**:
- `migration_name` - Filename of SQL file
- `applied_at` - Timestamp for audit trail
- `checksum` - Prevents re-running modified migrations
- `version` - Groups migrations by release

---

## Class Structure

### MigrationRunner Class
```python
class MigrationRunner:
    """Main migration orchestrator"""

    MIGRATIONS_DIR = Path("migrations/")
    ROLLBACKS_DIR = Path("migrations/rollbacks/")

    def __init__(self, connection_string: str)
    def connect()                                    # DB connection
    def close()                                      # Cleanup

    # Core Operations
    def discover_migrations() -> List[Migration]     # Scan directory
    def get_applied_migrations() -> Dict             # Query DB
    def get_pending_migrations() -> List[Migration]  # Calculate diff

    # Actions
    def status()                                     # Show status
    def migrate_up(dry_run: bool)                    # Apply pending
    def apply_migration(migration, dry_run)          # Apply one
    def rollback(migration_name: str)                # Reverse
    def create_migration(name: str)                  # Generate template

    # Utilities
    def calculate_checksum(content: str) -> str      # MD5 hash
    def parse_migration_filename(filename) -> Tuple  # Parse NNN_name.sql
```

### Migration Dataclass
```python
@dataclass
class Migration:
    """Represents a single migration file"""

    filename: str           # e.g., "001_add_column.sql"
    version: str            # e.g., "0.1.0"
    number: int             # e.g., 1
    name: str               # e.g., "add_column"
    sql_content: str        # Full SQL text
    checksum: str           # MD5 hash
    filepath: Path          # Absolute path to file
```

---

## File Format

### Migration File Structure
```sql
-- 001_migration_name.sql
-- =====================================================
-- Description: What this migration does
-- =====================================================

BEGIN;  -- Start transaction

-- Your SQL here
ALTER TABLE my_table ADD COLUMN new_column TEXT;
CREATE INDEX idx_my_table_new_column ON my_table(new_column);

-- Record application
INSERT INTO archon_migrations (version, migration_name)
VALUES ('0.1.0', '001_migration_name.sql')
ON CONFLICT (version, migration_name) DO NOTHING;

COMMIT;  -- End transaction

-- =====================================================
-- MIGRATION COMPLETE
-- =====================================================
```

**Key Elements**:
1. **Header comment** - Description
2. **BEGIN/COMMIT** - Transaction wrapper
3. **Migration SQL** - Actual changes
4. **Tracking insert** - Records application
5. **Footer comment** - Visual delimiter

---

## Naming Convention

### Migration Files
```
NNN_descriptive_name.sql

Where:
  NNN = 3-digit number (001, 002, 003, ...)
  descriptive_name = snake_case description
  .sql = SQL file extension
```

**Examples**:
- ✅ `001_add_source_url_display_name.sql`
- ✅ `010_add_provider_placeholders.sql`
- ✅ `011_add_page_metadata_table.sql`
- ❌ `add_column.sql` (missing number)
- ❌ `1_add_column.sql` (too short)
- ❌ `01_add_column.sql` (only 2 digits)

---

## Safety Mechanisms

### 1. Checksum Validation
```python
def calculate_checksum(content: str) -> str:
    return hashlib.md5(content.encode('utf-8')).hexdigest()

# Before applying:
if applied_checksum != current_checksum:
    raise Warning("Migration has been modified!")
```

**Prevents**: Re-running modified migrations

### 2. Transaction Safety
```sql
BEGIN;
  -- Migration SQL here
  -- If error occurs, automatic ROLLBACK
COMMIT;
```

**Prevents**: Partial migrations

### 3. Uniqueness Constraint
```sql
UNIQUE(version, migration_name)
```

**Prevents**: Duplicate applications

### 4. Dry-Run Mode
```python
def apply_migration(migration, dry_run=False):
    if dry_run:
        print("Would apply:", migration.sql_content[:500])
        return  # Don't execute
    # ... actual execution
```

**Prevents**: Accidental changes

### 5. Sequential Ordering
```python
migrations = sorted(migrations, key=lambda m: m.number)
```

**Prevents**: Out-of-order application

---

## Connection Architecture

### Supabase Connection
```python
# Environment
SUPABASE_URL = "https://xxxxx.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGc..."

# Extract project ref
project_ref = "xxxxx"  # from URL

# Build connection string
connection_string = (
    f"postgresql://postgres.{project_ref}:{service_key}"
    f"@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
)

# Connect
conn = psycopg2.connect(connection_string)
```

**Components**:
- **User**: `postgres.{project_ref}`
- **Password**: Service role key
- **Host**: Supabase pooler
- **Port**: 6543 (pooler port)
- **Database**: `postgres`

---

## Error Handling

### Connection Errors
```python
try:
    conn = psycopg2.connect(connection_string)
except psycopg2.OperationalError as e:
    print("ERROR: Cannot connect to database")
    print("Check SUPABASE_URL and SUPABASE_SERVICE_KEY")
    sys.exit(1)
```

### Migration Errors
```python
try:
    cursor.execute(migration.sql_content)
    conn.commit()
except Exception as e:
    conn.rollback()  # Automatic rollback
    print(f"ERROR: {e}")
    raise
```

### Checksum Errors
```python
if applied_checksum != current_checksum:
    print("WARNING: Migration has been modified!")
    print("This migration will be SKIPPED")
    # Don't apply
```

---

## Workflow Diagrams

### Developer Workflow
```
┌─────────────────────────────────────────────────────┐
│ Developer creates new feature                        │
└─────────────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────────────┐
│ python migrate.py create add_feature                 │
│   → Creates: 012_add_feature.sql                     │
└─────────────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────────────┐
│ Developer edits SQL file                             │
│   → Adds tables, columns, indexes, etc.             │
└─────────────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────────────┐
│ python migrate.py up --dry-run                       │
│   → Preview changes                                  │
└─────────────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────────────┐
│ python migrate.py up                                 │
│   → Apply to local database                          │
└─────────────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────────────┐
│ git add db/migrations/012_add_feature.sql            │
│ git commit -m "Add feature migration"                │
│ git push                                             │
└─────────────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────────────┐
│ CI/CD runs: python migrate.py up                     │
│   → Applies to production                            │
└─────────────────────────────────────────────────────┘
```

### Rollback Workflow
```
┌─────────────────────────────────────────────────────┐
│ Migration causes issues in production                │
└─────────────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────────────┐
│ Create rollback file:                                │
│ migrations/rollbacks/012_add_feature.sql             │
│   → Inverse SQL (DROP TABLE, etc.)                  │
└─────────────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────────────┐
│ python migrate.py down 012_add_feature.sql           │
│   → Executes rollback SQL                            │
│   → Removes from archon_migrations                   │
└─────────────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────────────┐
│ Fix original migration                               │
│ Re-apply corrected version                           │
└─────────────────────────────────────────────────────┘
```

---

## Performance Considerations

### Sequential Execution
- Migrations run one at a time (by design)
- Prevents race conditions
- Ensures correct ordering

### Transaction Boundaries
- Each migration in own transaction
- Fast commit on success
- Fast rollback on failure

### Index Creation
- Can be slow for large tables
- Consider `CONCURRENTLY` option
- Schedule during low-traffic periods

### Checksum Calculation
- MD5 is fast (< 1ms for typical migrations)
- Cached in `archon_migrations` table
- Only calculated once per migration

---

## Security Model

### Authentication
- Requires Supabase service role key
- Admin-level access
- Never use anon key

### Authorization
- Migration system bypasses RLS (service role)
- Necessary for schema changes
- Keep service key secret

### Secrets Management
- `.env` file (gitignored)
- Environment variables
- Never hardcoded

---

## Extension Points

### Custom Connection String
```python
def get_connection_string() -> str:
    # Override for non-Supabase PostgreSQL
    return "postgresql://user:pass@host:5432/db"
```

### Custom Migration Validation
```python
def validate_migration(migration: Migration):
    # Add custom checks
    if "DROP TABLE" in migration.sql_content:
        print("WARNING: Destructive operation!")
```

### Pre/Post Migration Hooks
```python
def pre_migration_hook(migration):
    # Backup before applying
    pass

def post_migration_hook(migration):
    # Send notification
    pass
```

---

## Testing Strategy

### Unit Tests
- Test `parse_migration_filename()`
- Test `calculate_checksum()`
- Test `discover_migrations()`

### Integration Tests
- Test against test database
- Apply migrations
- Verify schema changes
- Rollback and verify

### End-to-End Tests
- Full workflow simulation
- Create → Apply → Status → Rollback

---

## Monitoring

### What to Monitor
1. **Migration status** - `python migrate.py status`
2. **archon_migrations table** - Row count, timestamps
3. **Application errors** - Failed migrations
4. **Performance** - Migration duration

### Alerts
- CI/CD failure on migration error
- Long-running migrations (> 5 min)
- Checksum mismatches

---

## Disaster Recovery

### Backup Strategy
1. **Before migration**: Snapshot database
2. **After migration**: Verify schema
3. **If failure**: Restore from snapshot

### Manual Recovery
```sql
-- If migration tracking table corrupted:
SELECT * FROM archon_migrations ORDER BY applied_at;

-- Manually fix or re-create table
CREATE TABLE archon_migrations (...);
```

---

## Future Architecture

Potential enhancements:
- **Web UI**: React dashboard for status
- **Notifications**: Slack/Discord integration
- **Scheduling**: Time-based migrations
- **Multi-tenancy**: Per-tenant migrations
- **Dependency graph**: Migration dependencies
- **Parallel execution**: Safe parallel migrations

---

## References

- PostgreSQL Docs: https://www.postgresql.org/docs/
- psycopg2 Docs: https://www.psycopg.org/docs/
- Supabase Docs: https://supabase.com/docs
- Python Docs: https://docs.python.org/3/

---

**Last Updated**: 2025-01-15
**Version**: 1.0
