"""
Emergency Rollback Script

Usage: python scripts/rollback.py [--phase 2|3|4|5|all]
Reverts the DB and code to the last stable state.

Examples:
    python scripts/rollback.py --phase 3    # Undo Plan 3 changes
    python scripts/rollback.py --phase all  # Full emergency rollback
"""

import subprocess
import sys
import shutil
import os
from pathlib import Path

# Project root directory
ROOT = Path(__file__).parent.parent

# Phase to git tag mapping
PHASE_TAGS = {
    "2": "pre_plan2",
    "3": "pre_plan3",
    "4": "pre_plan4",
    "5": "pre_plan5",
    "6": "pre_plan6",
    "7": "pre_plan7",
    "8": "pre_plan8",
    "9": "pre_plan9",
    "all": "pre_migration",
}


def rollback(phase: str):
    """Perform rollback to the specified phase."""
    tag = PHASE_TAGS.get(phase)
    if not tag:
        print(f"❌ Unknown phase: {phase}")
        print(f"   Available phases: {', '.join(PHASE_TAGS.keys())}")
        sys.exit(1)

    print(f"⏪ Rolling back to: {tag}")
    print()

    # Step 1: Check if Alembic is available
    try:
        result = subprocess.run(
            ["alembic", "--version"], 
            capture_output=True, 
            text=True,
            cwd=ROOT
        )
        if result.returncode != 0:
            print("⚠️  Alembic not found. Skipping database rollback.")
            alembic_available = False
        else:
            print(f"✅ Alembic found: {result.stdout.strip()}")
            alembic_available = True
    except FileNotFoundError:
        print("⚠️  Alembic not found. Skipping database rollback.")
        alembic_available = False

    # Step 2: Revert DB to migration below this phase
    if alembic_available:
        print()
        print("  1. Reverting Alembic DB migration...")
        try:
            result = subprocess.run(
                ["alembic", "downgrade", tag], 
                capture_output=True, 
                text=True,
                cwd=ROOT
            )
            if result.returncode != 0:
                print(f"  ❌ Alembic rollback failed: {result.stderr}")
            else:
                print(f"  ✅ DB reverted to {tag}")
                if result.stdout:
                    print(f"     {result.stdout}")
        except Exception as e:
            print(f"  ❌ Error running alembic: {e}")

    # Step 3: Check for git tag (optional code rollback)
    print()
    print("  2. Checking for git tag...")
    try:
        result = subprocess.run(
            ["git", "tag", "-l", tag], 
            capture_output=True, 
            text=True,
            cwd=ROOT
        )
        if tag in result.stdout:
            print(f"  ✅ Git tag '{tag}' exists")
            
            # Ask user if they want to rollback code
            response = input("  Do you want to rollback code to this tag? (y/N): ")
            if response.lower() == 'y':
                print(f"  Rolling back code to {tag}...")
                # First check if there are uncommitted changes
                result = subprocess.run(
                    ["git", "status", "--porcelain"], 
                    capture_output=True, 
                    text=True,
                    cwd=ROOT
                )
                if result.stdout:
                    print("  ⚠️  You have uncommitted changes.")
                    print("     Commit or stash them before rolling back.")
                    print(f"     Uncommitted files: {result.stdout[:200]}")
                
                # Stash uncommitted changes
                if result.stdout:
                    subprocess.run(["git", "stash"], cwd=ROOT)
                    print("  ✅ Uncommitted changes stashed")
                
                # Checkout the tag
                result = subprocess.run(
                    ["git", "checkout", tag], 
                    capture_output=True, 
                    text=True,
                    cwd=ROOT
                )
                if result.returncode == 0:
                    print(f"  ✅ Code rolled back to {tag}")
                else:
                    print(f"  ❌ Git checkout failed: {result.stderr}")
        else:
            print(f"  ⚠️  Git tag '{tag}' not found")
            print(f"     Run: git tag {tag}  (before starting next plan)")
    except Exception as e:
        print(f"  ⚠️  Git operation failed: {e}")

    # Step 4: Restore main.py from backup if exists
    print()
    print("  3. Checking for main.py backup...")
    backup = ROOT / f"app/main.py.{tag}_backup"
    if backup.exists():
        shutil.copy2(backup, ROOT / "app/main.py")
        print(f"  ✅ app/main.py restored from {backup.name}")
    else:
        print(f"  ⚠️  No main.py backup found for {tag}")
        print(f"     Expected: {backup}")

    print()
    print("=" * 50)
    print(f"✅ Rollback to {tag} complete!")
    print("=" * 50)
    print()
    print("Next steps:")
    print("  1. Restart your application")
    print("  2. Verify functionality")
    print("  3. Check logs for any errors")


if __name__ == "__main__":
    # Parse command line arguments
    phase = "all"
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.startswith("--phase"):
            phase = arg.replace("--phase", "").strip()
        elif arg.startswith("-"):
            phase = arg.replace("-", "").strip()
    
    rollback(phase)
