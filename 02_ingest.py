import sqlite3
import pandas as pd


df = pd.read_csv("raw_transactions.csv")

conn = sqlite3.connect("transactions.db")


df.to_sql("raw_transactions", conn, if_exists="replace", index=False)

conn.close()

print(f"Loaded {len(df)} rows into transactions.db -> table 'raw_transactions'")