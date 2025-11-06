# Archon Migrations - Quick Start

## 30-Second Setup

```bash
cd db
./setup.sh                    # Install dependencies & create .env
# Edit .env with your Supabase credentials
python3 migrate.py status     # Check status
python3 migrate.py up         # Apply migrations
```

---

## Essential Commands

```bash
# Check what needs to be applied
python3 migrate.py status

# Preview migrations without applying (SAFE)
python3 migrate.py up --dry-run

# Apply all pending migrations
python3 migrate.py up

# Create a new migration
python3 migrate.py create add_new_feature

# Rollback a migration (requires rollback file)
python3 migrate.py down 011_add_page_metadata_table.sql
```

---

## Environment Setup

Create `db/.env`:
```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGc...  # Service role key (NOT anon!)
```

Get these from: **Supabase Dashboard → Settings → API**

---

## Creating Migrations

```bash
python3 migrate.py create my_migration_name
# Creates: migrations/NNN_my_migration_name.sql
```

Or manually create:
```sql
-- migrations/012_my_migration.sql
BEGIN;

ALTER TABLE my_table ADD COLUMN new_column TEXT;

INSERT INTO archon_migrations (version, migration_name)
VALUES ('0.1.0', '012_my_migration.sql')
ON CONFLICT (version, migration_name) DO NOTHING;

COMMIT;
```

---

## Safety Tips

✅ **Always dry-run first**: `python3 migrate.py up --dry-run`
✅ **Never modify applied migrations** - Create new ones instead
✅ **Keep .env secret** - Never commit it to git
❌ **Don't use anon key** - Must use service role key

---

## Troubleshooting

**"Missing environment variables"**
→ Create `.env` with `SUPABASE_URL` and `SUPABASE_SERVICE_KEY`

**"Migration has been modified"**
→ Don't edit applied migrations - Create a new one

**"Connection timeout"**
→ Check Supabase project is running and key is correct

---

## Full Documentation

See **[README.md](README.md)** for complete details.
