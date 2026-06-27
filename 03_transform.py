"""
STEP 3: TRANSFORMATION (CLEANING)
===================================
The raw data has real problems: missing ages, negative amounts,
inconsistent status text (e.g. "COMPLETED  " vs "Completed").

This script uses SQL to fix those problems and saves the result
as a NEW table called clean_transactions. We never overwrite the
raw table -- you always keep raw data untouched, and build clean
versions on top of it. This is standard practice: if your cleaning
logic has a bug, you can always start over from raw data.
"""

import sqlite3

conn = sqlite3.connect("transactions.db")
cur = conn.cursor()

# Drop the clean table if it already exists, so we can rebuild it
# fresh every time we run this script during testing.
cur.execute("DROP TABLE IF EXISTS clean_transactions")

# This single SQL statement does ALL the cleaning at once:
#
# - TRIM(UPPER(status)) -> "COMPLETED  " becomes "COMPLETED" (no spaces, all caps)
#   then we use CASE to turn it into a clean, consistent label
# - sender_age: if it's missing (NULL), we fill it with 0 and flag it
#   as "age_unknown" = 1, rather than guessing a fake age
# - amount: if negative, we flip it positive using ABS() -- this assumes
#   the negative was a data entry glitch, not a real refund
# - distance_km, needed_assistance, etc. pass through unchanged, they
#   were already clean
# - is_elderly: a NEW calculated column. age 60+ = elderly. This is the
#   single most important column for your whole analysis.
query = """
CREATE TABLE clean_transactions AS
SELECT
    sender_name,
    COALESCE(sender_age, 0) AS sender_age,
    CASE WHEN sender_age IS NULL THEN 1 ELSE 0 END AS age_unknown,
    receiver_name,
    ABS(amount) AS amount,
    method,
    location,
    distance_km,
    timestamp,
    CASE
        WHEN TRIM(UPPER(status)) LIKE 'COMPLETED%' THEN 'Completed'
        WHEN TRIM(UPPER(status)) LIKE 'FAILED%' THEN 'Failed'
        WHEN TRIM(UPPER(status)) LIKE 'PENDING%' THEN 'Pending'
        ELSE 'Unknown'
    END AS status,
    needed_assistance,
    CASE WHEN sender_age >= 60 THEN 1 ELSE 0 END AS is_elderly
FROM raw_transactions
"""

cur.execute(query)
conn.commit()

# quick check: how many rows made it through, and how many are flagged elderly
cur.execute("SELECT COUNT(*) FROM clean_transactions")
total = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM clean_transactions WHERE is_elderly = 1")
elderly_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM clean_transactions WHERE age_unknown = 1")
unknown_count = cur.fetchone()[0]

print(f"clean_transactions created: {total} rows")
print(f"  -> elderly (60+): {elderly_count}")
print(f"  -> age unknown (was missing): {unknown_count}")

conn.close()