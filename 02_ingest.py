"""
STEP 2: INGESTION
==================
This takes our raw CSV file and loads it into a proper database
(SQLite). A CSV is just a loose file. A database lets us run
SQL queries on it later, and is how real companies store data
instead of passing spreadsheets around.

OUTPUT: transactions.db  (a database file, containing table: raw_transactions)
"""

import sqlite3
import pandas as pd

# 1. read the CSV file into a pandas "DataFrame" (basically a spreadsheet
#    object Python can work with)
df = pd.read_csv("raw_transactions.csv")

# 2. connect to (or create) a SQLite database file called transactions.db
conn = sqlite3.connect("transactions.db")

# 3. write the DataFrame into the database as a table called raw_transactions
#    if_exists="replace" means: if this table already exists, wipe it and
#    redo it (useful while we're still testing things)
df.to_sql("raw_transactions", conn, if_exists="replace", index=False)

conn.close()

print(f"Loaded {len(df)} rows into transactions.db -> table 'raw_transactions'")