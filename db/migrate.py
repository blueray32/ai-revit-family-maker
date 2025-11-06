#!/usr/bin/env python3
"""
Archon Database Migration Runner
=================================

Safely applies database migrations to Supabase with:
- Automatic detection of pending migrations
- Checksum validation to prevent re-running modified migrations
- Dry-run mode for safety
- Rollback support
- Status checking

Usage:
    python migrate.py status              # Check migration status
    python migrate.py up                  # Apply all pending migrations
    python migrate.py up --dry-run        # Preview migrations without applying
    python migrate.py down <migration>    # Rollback specific migration (if rollback exists)
    python migrate.py create <name>       # Create new migration file

Environment Variables:
    SUPABASE_URL          # Your Supabase project URL
    SUPABASE_SERVICE_KEY  # Service role key (not anon key!)

Example:
    export SUPABASE_URL="https://xxxxx.supabase.co"
    export SUPABASE_SERVICE_KEY="eyJhbGc..."
    python migrate.py up
"""

import os
import sys
import hashlib
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

try:
    import psycopg2
    from psycopg2 import sql
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
except ImportError:
    print("ERROR: psycopg2 not installed. Run: pip install psycopg2-binary")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("WARNING: python-dotenv not installed. Run: pip install python-dotenv")
    load_dotenv = lambda: None


@dataclass
class Migration:
    """Represents a database migration file."""
    filename: str
    version: str
    number: int
    name: str
    sql_content: str
    checksum: str
    filepath: Path

    @property
    def migration_name(self) -> str:
        """Return the migration name as stored in archon_migrations."""
        return self.filename


class MigrationRunner:
    """Handles database migration operations."""

    MIGRATIONS_DIR = Path(__file__).parent / "migrations"
    ROLLBACKS_DIR = Path(__file__).parent / "migrations" / "rollbacks"

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.conn = None

    def connect(self):
        """Establish database connection."""
        if self.conn is None:
            self.conn = psycopg2.connect(self.connection_string)
            # Ensure migrations table exists
            self._ensure_migrations_table()

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _ensure_migrations_table(self):
        """Create archon_migrations table if it doesn't exist."""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS archon_migrations (
                    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                    version VARCHAR(20) NOT NULL,
                    migration_name VARCHAR(255) NOT NULL,
                    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    checksum VARCHAR(32),
                    UNIQUE(version, migration_name)
                );

                CREATE INDEX IF NOT EXISTS idx_archon_migrations_version
                ON archon_migrations(version);

                CREATE INDEX IF NOT EXISTS idx_archon_migrations_applied_at
                ON archon_migrations(applied_at DESC);
            """)
            self.conn.commit()

    @staticmethod
    def calculate_checksum(content: str) -> str:
        """Calculate MD5 checksum of migration content."""
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    @staticmethod
    def parse_migration_filename(filename: str) -> Optional[Tuple[int, str]]:
        """
        Parse migration filename to extract number and name.

        Expected format: NNN_migration_name.sql
        Example: 001_add_source_url_display_name.sql

        Returns: (number, name) or None if invalid
        """
        match = re.match(r'^(\d{3})_(.+)\.sql$', filename)
        if match:
            return (int(match.group(1)), match.group(2))
        return None

    def discover_migrations(self) -> List[Migration]:
        """
        Discover all migration files in migrations directory.

        Returns: List of Migration objects sorted by number
        """
        migrations = []

        if not self.MIGRATIONS_DIR.exists():
            print(f"WARNING: Migrations directory not found: {self.MIGRATIONS_DIR}")
            return migrations

        for filepath in sorted(self.MIGRATIONS_DIR.glob("*.sql")):
            parsed = self.parse_migration_filename(filepath.name)
            if not parsed:
                print(f"WARNING: Skipping invalid migration filename: {filepath.name}")
                continue

            number, name = parsed
            sql_content = filepath.read_text()
            checksum = self.calculate_checksum(sql_content)

            migrations.append(Migration(
                filename=filepath.name,
                version="0.1.0",  # Extract from migration if needed
                number=number,
                name=name,
                sql_content=sql_content,
                checksum=checksum,
                filepath=filepath
            ))

        return sorted(migrations, key=lambda m: m.number)

    def get_applied_migrations(self) -> Dict[str, Dict]:
        """
        Get list of already applied migrations from database.

        Returns: Dict mapping migration_name to metadata
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT migration_name, version, applied_at, checksum
                FROM archon_migrations
                ORDER BY applied_at
            """)

            applied = {}
            for row in cur.fetchall():
                applied[row[0]] = {
                    'version': row[1],
                    'applied_at': row[2],
                    'checksum': row[3]
                }

            return applied

    def get_pending_migrations(self) -> List[Migration]:
        """Get list of migrations that haven't been applied yet."""
        all_migrations = self.discover_migrations()
        applied = self.get_applied_migrations()

        pending = []
        for migration in all_migrations:
            if migration.migration_name not in applied:
                pending.append(migration)
            else:
                # Check checksum to detect modifications
                applied_checksum = applied[migration.migration_name].get('checksum')
                if applied_checksum and applied_checksum != migration.checksum:
                    print(f"WARNING: Migration {migration.migration_name} has been modified!")
                    print(f"  Applied checksum:  {applied_checksum}")
                    print(f"  Current checksum:  {migration.checksum}")
                    print(f"  This migration will be SKIPPED to prevent re-running modified SQL")

        return pending

    def apply_migration(self, migration: Migration, dry_run: bool = False):
        """
        Apply a single migration to the database.

        Args:
            migration: Migration to apply
            dry_run: If True, print SQL but don't execute
        """
        print(f"\n{'[DRY RUN] ' if dry_run else ''}Applying: {migration.filename}")
        print(f"  Name: {migration.name}")
        print(f"  Checksum: {migration.checksum}")

        if dry_run:
            print(f"\n--- SQL Preview (first 500 chars) ---")
            print(migration.sql_content[:500])
            if len(migration.sql_content) > 500:
                print(f"... ({len(migration.sql_content) - 500} more characters)")
            print(f"--- End Preview ---\n")
            return

        try:
            # Execute migration SQL
            with self.conn.cursor() as cur:
                cur.execute(migration.sql_content)

            # Record migration in tracking table
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO archon_migrations (version, migration_name, checksum)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (version, migration_name) DO NOTHING
                """, (migration.version, migration.migration_name, migration.checksum))

            self.conn.commit()
            print(f"  ✓ Applied successfully")

        except Exception as e:
            self.conn.rollback()
            print(f"  ✗ ERROR: {e}")
            raise

    def status(self):
        """Print current migration status."""
        all_migrations = self.discover_migrations()
        applied = self.get_applied_migrations()
        pending = self.get_pending_migrations()

        print("\n" + "="*70)
        print("MIGRATION STATUS")
        print("="*70)

        print(f"\nTotal migrations: {len(all_migrations)}")
        print(f"Applied: {len(applied)}")
        print(f"Pending: {len(pending)}")

        if applied:
            print(f"\n--- Applied Migrations ---")
            for migration in all_migrations:
                if migration.migration_name in applied:
                    meta = applied[migration.migration_name]
                    applied_at = meta['applied_at'].strftime('%Y-%m-%d %H:%M:%S')
                    print(f"  ✓ {migration.filename} (applied {applied_at})")

        if pending:
            print(f"\n--- Pending Migrations ---")
            for migration in pending:
                print(f"  ○ {migration.filename}")

        print("\n" + "="*70 + "\n")

    def migrate_up(self, dry_run: bool = False):
        """Apply all pending migrations."""
        pending = self.get_pending_migrations()

        if not pending:
            print("\n✓ Database is up to date. No pending migrations.")
            return

        print(f"\n{'[DRY RUN MODE] ' if dry_run else ''}Found {len(pending)} pending migration(s)")

        for migration in pending:
            self.apply_migration(migration, dry_run=dry_run)

        if dry_run:
            print(f"\n[DRY RUN] Would apply {len(pending)} migration(s)")
            print("Run without --dry-run to apply for real")
        else:
            print(f"\n✓ Successfully applied {len(pending)} migration(s)")

    def rollback(self, migration_name: str):
        """
        Rollback a specific migration (if rollback file exists).

        Args:
            migration_name: Name of migration to rollback (e.g., "001_add_source_url_display_name.sql")
        """
        rollback_path = self.ROLLBACKS_DIR / migration_name

        if not rollback_path.exists():
            print(f"ERROR: Rollback file not found: {rollback_path}")
            print(f"Rollbacks must be created manually in: {self.ROLLBACKS_DIR}")
            return

        applied = self.get_applied_migrations()
        if migration_name not in applied:
            print(f"ERROR: Migration {migration_name} has not been applied")
            return

        print(f"\nRolling back: {migration_name}")

        try:
            sql_content = rollback_path.read_text()

            with self.conn.cursor() as cur:
                cur.execute(sql_content)

            # Remove from tracking table
            with self.conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM archon_migrations
                    WHERE migration_name = %s
                """, (migration_name,))

            self.conn.commit()
            print(f"  ✓ Rolled back successfully")

        except Exception as e:
            self.conn.rollback()
            print(f"  ✗ ERROR: {e}")
            raise

    def create_migration(self, name: str):
        """
        Create a new migration file with the next available number.

        Args:
            name: Migration name (e.g., "add_new_column")
        """
        existing = self.discover_migrations()
        next_number = max([m.number for m in existing], default=0) + 1

        filename = f"{next_number:03d}_{name}.sql"
        filepath = self.MIGRATIONS_DIR / filename

        template = f"""-- {filename}
-- =====================================================
-- Description: {name.replace('_', ' ').title()}
-- =====================================================

-- Your migration SQL here

BEGIN;

-- Example: Add a new column
-- ALTER TABLE your_table
-- ADD COLUMN your_column TEXT;

-- Record migration application for tracking
INSERT INTO archon_migrations (version, migration_name)
VALUES ('0.1.0', '{filename}')
ON CONFLICT (version, migration_name) DO NOTHING;

COMMIT;

-- =====================================================
-- MIGRATION COMPLETE
-- =====================================================
"""

        filepath.write_text(template)
        print(f"\n✓ Created migration: {filepath}")
        print(f"\nEdit the file and run: python migrate.py up")


def get_connection_string() -> str:
    """
    Get Supabase database connection string from environment.

    Returns: PostgreSQL connection string
    """
    load_dotenv()

    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_KEY')

    if not supabase_url or not supabase_key:
        print("\nERROR: Missing required environment variables:")
        print("  SUPABASE_URL - Your Supabase project URL")
        print("  SUPABASE_SERVICE_KEY - Your service role key (not anon key!)")
        print("\nSet these in .env file or export them:")
        print('  export SUPABASE_URL="https://xxxxx.supabase.co"')
        print('  export SUPABASE_SERVICE_KEY="eyJhbGc..."')
        sys.exit(1)

    # Extract project ref from URL
    # Format: https://xxxxx.supabase.co -> xxxxx
    project_ref = supabase_url.replace('https://', '').replace('.supabase.co', '')

    # Construct direct PostgreSQL connection string
    # Supabase uses pooler on port 6543 for direct connections
    connection_string = (
        f"postgresql://postgres.{project_ref}:{supabase_key}"
        f"@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
    )

    return connection_string


def main():
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Archon Database Migration Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    subparsers = parser.add_subparsers(dest='command', help='Migration commands')

    # Status command
    subparsers.add_parser('status', help='Check migration status')

    # Up command
    up_parser = subparsers.add_parser('up', help='Apply pending migrations')
    up_parser.add_argument('--dry-run', action='store_true', help='Preview without applying')

    # Down command
    down_parser = subparsers.add_parser('down', help='Rollback a migration')
    down_parser.add_argument('migration', help='Migration filename to rollback')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new migration file')
    create_parser.add_argument('name', help='Migration name (e.g., add_new_column)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Get database connection
    try:
        connection_string = get_connection_string()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Execute command
    try:
        with MigrationRunner(connection_string) as runner:
            if args.command == 'status':
                runner.status()

            elif args.command == 'up':
                runner.migrate_up(dry_run=args.dry_run)

            elif args.command == 'down':
                runner.rollback(args.migration)

            elif args.command == 'create':
                runner.create_migration(args.name)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
