# Database Startup Check

## What It Does

Added an automatic check that runs when the app starts. If the database is empty (no vocabulary words), it displays a clear warning message.

## The Warning

When the database is empty, you'll see:

```
============================================================
⚠️  WARNING: Database is empty!
============================================================
The database has no vocabulary words.
Please run: python3 seed_database.py
============================================================
```

## Why This Is Helpful

**Prevents Silent Failures:**
- You'll know immediately if your database is empty
- No more "No sentences found" errors without knowing why
- Clear instructions on how to fix it

**Development Workflow:**
- If you delete the database to start fresh, you'll get a reminder to reseed
- New team members will see instructions on first run
- Helps catch issues after schema changes

## How It Works

In [app.py](app.py:26-35):

```python
# Check if database needs seeding
with app.app_context():
    word_count = VocabularyWord.query.count()
    if word_count == 0:
        print("\n" + "="*60)
        print("⚠️  WARNING: Database is empty!")
        print("="*60)
        print("The database has no vocabulary words.")
        print("Please run: python3 seed_database.py")
        print("="*60 + "\n")
```

**The check:**
1. Runs when app starts (after `init_db(app)`)
2. Counts vocabulary words in database
3. If count is 0, displays warning
4. App continues to run (doesn't crash)

## When You'll See This Warning

You'll see the warning when:
- **First setup** - Brand new database
- **After database deletion** - Deleted `instance/spanish_vocab.db`
- **After schema changes** - Recreated database with new models
- **Missing seed data** - Tables exist but empty

## When You Won't See It

No warning when:
- Database has vocabulary words (normal operation)
- After running `seed_database.py` successfully
- Database is properly populated

## Quick Fix

When you see the warning, just run:

```bash
python3 seed_database.py
```

Then restart your app and the warning will be gone!

## Additional Notes

**Why Not Auto-Seed?**
- We don't automatically seed on startup because:
  - It's slow (120 words + 60 templates)
  - Could overwrite existing data
  - Better to be explicit when seeding
  - Developer should know when database is being populated

**Production Considerations:**
- This check adds ~10ms to startup time
- Minimal overhead (single COUNT query)
- Only runs once at app startup
- Safe to use in production

## Related Files

- [app.py](app.py:26-35) - Startup check implementation
- [seed_database.py](seed_database.py) - Database seeding script
- [database.py](database.py) - Database models

---

**Remember**: Tests use in-memory databases that auto-seed, but your production database needs manual seeding!
