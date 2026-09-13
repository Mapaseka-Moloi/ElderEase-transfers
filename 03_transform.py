import sqlite3

conn = sqlite3.connect("transactions.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS clean_transactions")

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

elderly
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
