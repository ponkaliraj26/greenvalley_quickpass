import sqlite3

# Connect to DB (creates file if it doesn't exist)
conn = sqlite3.connect("app.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS learners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    learner_id TEXT,
    name TEXT,
    grade TEXT,
    qr_code TEXT
)
""")

conn.commit()
conn.close()
print("✅ learners table created.")
