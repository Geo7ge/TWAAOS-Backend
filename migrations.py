"""
Migration manager for Supabase
Ajută la tracking și execuție de migrații
"""
import os
import glob
import json
from datetime import datetime
from config import settings


class MigrationManager:
    def __init__(self):
        self.migrations_dir = "migrations"
        self.migrations_log = "migrations/.migrations.log"  # Local JSON tracking
        self._ensure_log_exists()
    
    def _ensure_log_exists(self):
        """Ensure migrations log file exists"""
        if not os.path.exists(self.migrations_log):
            os.makedirs(os.path.dirname(self.migrations_log), exist_ok=True)
            with open(self.migrations_log, 'w') as f:
                json.dump({"applied": []}, f, indent=2)
        
    def get_applied_migrations(self):
        """Get list of applied migrations from local log"""
        self._ensure_log_exists()
        try:
            with open(self.migrations_log, 'r') as f:
                data = json.load(f)
                return data.get("applied", [])
        except Exception as e:
            print(f"⚠️  Warning: Could not fetch applied migrations: {e}")
            return []
    
    def get_all_migrations(self):
        """Get all migration files sorted by number"""
        pattern = os.path.join(self.migrations_dir, "*.sql")
        files = glob.glob(pattern)
        return sorted(files)
    
    def get_pending_migrations(self):
        """Get migrations that haven't been applied yet"""
        all_migrations = self.get_all_migrations()
        applied = self.get_applied_migrations()
        
        migration_names = [os.path.basename(f) for f in all_migrations]
        pending = [m for m in migration_names if m not in applied]
        return pending
    
    def apply_migration(self, migration_file):
        """Show migration content for manual execution in Supabase Dashboard"""
        migration_path = os.path.join(self.migrations_dir, migration_file)
        
        if not os.path.exists(migration_path):
            print(f"❌ File not found: {migration_path}")
            return
        
        with open(migration_path, 'r') as f:
            sql_content = f.read()
        
        print(f"\n⏳ Migration: {migration_file}")
        print(f"📋 SQL Content:")
        print("=" * 70)
        print(sql_content)
        print("=" * 70)
        print(f"\n📌 Instructions:")
        print(f"   1. Go to Supabase Dashboard -> SQL Editor")
        print(f"   2. Create a new query")
        print(f"   3. Paste the SQL content above")
        print(f"   4. Click 'Run' to execute")
        print(f"   5. After successful execution, run:")
        print(f"      python migrations.py mark {migration_file}")
    
    def mark_as_applied(self, migration_name):
        """Mark migration as applied in local log"""
        applied = self.get_applied_migrations()
        
        if migration_name in applied:
            print(f"⚠️  Migration {migration_name} is already marked as applied")
            return
        
        try:
            applied.append(migration_name)
            with open(self.migrations_log, 'w') as f:
                json.dump({
                    "applied": applied,
                    "last_updated": datetime.utcnow().isoformat()
                }, f, indent=2)
            print(f"✅ Migration {migration_name} marked as applied")
        except Exception as e:
            print(f"❌ Error marking migration as applied: {e}")
    
    def status(self):
        """Show migration status"""
        print("\n📊 Migration Status")
        print("=" * 70)
        
        applied = self.get_applied_migrations()
        all_migs = self.get_all_migrations()
        migration_names = [os.path.basename(f) for f in all_migs]
        pending = [m for m in migration_names if m not in applied]
        
        print(f"\n✅ Applied: {len(applied)}")
        if applied:
            for m in applied:
                print(f"   - {m}")
        else:
            print("   (none)")
        
        print(f"\n⏳ Pending: {len(pending)}")
        for m in pending:
            print(f"   - {m}")
        
        print(f"\n📁 Total migrations: {len(migration_names)}")


if __name__ == "__main__":
    import sys
    
    manager = MigrationManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "status":
            manager.status()
        elif command == "pending":
            pending = manager.get_pending_migrations()
            print("Pending migrations:")
            for m in pending:
                print(f"  - {m}")
        elif command == "apply" and len(sys.argv) > 2:
            migration_name = sys.argv[2]
            manager.apply_migration(migration_name)
        elif command == "mark" and len(sys.argv) > 2:
            migration_name = sys.argv[2]
            manager.mark_as_applied(migration_name)
        else:
            print("Usage:")
            print("  python migrations.py status              - Show migration status")
            print("  python migrations.py pending             - List pending migrations")
            print("  python migrations.py apply <name>        - Show SQL and instructions")
            print("  python migrations.py mark <name>         - Mark as applied after manual execution")
    else:
        manager.status()
