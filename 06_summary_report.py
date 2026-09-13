"""
PIPELINE SUMMARY REPORT
========================
This script queries the clean_transactions table and prints a
formatted summary of all key findings from the pipeline.
 
Think of this as the "executive summary" of the entire project —
instead of opening 6 charts one by one, you run this script and
get all the important numbers in one place, in plain English.
 
This is useful for:
- Quick verification that the pipeline ran correctly
- Presenting findings verbally without needing to open charts
- A record of what the data showed at the time of analysis
 
OUTPUT: printed to terminal
"""


import sqlite3
from datetime import datetime
 
conn = sqlite3.connect("transactions.db")
cur = conn.cursor()
 
print("=" * 60)
print("   ELDEREASE TRANSFERS — PIPELINE SUMMARY REPORT")
print(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)


# -----------------------------------------------------------------
# SECTION 1: Dataset Overview
# -----------------------------------------------------------------
print("\n📊 DATASET OVERVIEW")
print("-" * 40)
 
cur.execute("SELECT COUNT(*) FROM raw_transactions")
raw_total = cur.fetchone()[0]
 
cur.execute("SELECT COUNT(*) FROM clean_transactions")
clean_total = cur.fetchone()[0]
 
cur.execute("SELECT COUNT(*) FROM clean_transactions WHERE is_elderly = 1")
elderly_count = cur.fetchone()[0]
 
cur.execute("SELECT COUNT(*) FROM clean_transactions WHERE is_elderly = 0")
young_count = cur.fetchone()[0]
 
cur.execute("SELECT COUNT(*) FROM clean_transactions WHERE age_unknown = 1")
unknown_count = cur.fetchone()[0]
 
print(f"  Total raw transactions ingested:   {raw_total}")
print(f"  Total clean transactions:          {clean_total}")
print(f"  Elderly senders (60+):             {elderly_count}")
print(f"  Younger senders:                   {young_count}")
print(f"  Records with missing age (flagged):{unknown_count}")


# -----------------------------------------------------------------
# SECTION 2: Failure Rate
# -----------------------------------------------------------------
print("\n❌ TRANSACTION FAILURE RATE")
print("-" * 40)
 
cur.execute("""
    SELECT
        CASE WHEN is_elderly = 1 THEN 'Elderly (60+)' ELSE 'Younger' END AS age_group,
        status,
        COUNT(*) AS count
    FROM clean_transactions
    GROUP BY is_elderly, status
""")
status_results = cur.fetchall()
 
elderly_total = sum(r[2] for r in status_results if r[0] == "Elderly (60+)")
young_total = sum(r[2] for r in status_results if r[0] == "Younger")
elderly_failed = sum(r[2] for r in status_results if r[0] == "Elderly (60+)" and r[1] == "Failed")
young_failed = sum(r[2] for r in status_results if r[0] == "Younger" and r[1] == "Failed")
 
elderly_fail_rate = round(100 * elderly_failed / elderly_total, 1)
young_fail_rate = round(100 * young_failed / young_total, 1)
difference = round(elderly_fail_rate / young_fail_rate, 1)
 
print(f"  Elderly failure rate:   {elderly_fail_rate}%")
print(f"  Younger failure rate:   {young_fail_rate}%")
print(f"  Elderly fail {difference}x more often than younger users")