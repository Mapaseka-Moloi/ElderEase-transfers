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


# -----------------------------------------------------------------
# SECTION 3: Distance Traveled
# -----------------------------------------------------------------
print("\n🚶 DISTANCE TRAVELED TO COMPLETE A TRANSACTION")
print("-" * 40)
 
cur.execute("""
    SELECT
        CASE WHEN is_elderly = 1 THEN 'Elderly (60+)' ELSE 'Younger' END AS age_group,
        ROUND(AVG(distance_km), 2) AS avg_distance
    FROM clean_transactions
    GROUP BY is_elderly
""")
distance_results = cur.fetchall()
 
for row in distance_results:
    print(f"  {row[0]:<20} avg distance: {row[1]} km")
 
elderly_dist = next(r[1] for r in distance_results if r[0] == "Elderly (60+)")
young_dist = next(r[1] for r in distance_results if r[0] == "Younger")
print(f"  Elderly travel {round(elderly_dist/young_dist, 1)}x further on average")
 
# -----------------------------------------------------------------
# SECTION 4: Third-Party Assistance
# -----------------------------------------------------------------
print("\n🤝 THIRD-PARTY ASSISTANCE REQUIRED")
print("-" * 40)
 
cur.execute("""
    SELECT
        CASE WHEN is_elderly = 1 THEN 'Elderly (60+)' ELSE 'Younger' END AS age_group,
        ROUND(AVG(needed_assistance) * 100, 1) AS pct_assistance
    FROM clean_transactions
    GROUP BY is_elderly
""")
assistance_results = cur.fetchall()
 
for row in assistance_results:
    print(f"  {row[0]:<20} needed help: {row[1]}% of transactions")


# -----------------------------------------------------------------
# SECTION 5: Transaction Methods
# -----------------------------------------------------------------
print("\n💳 MOST USED TRANSACTION METHOD")
print("-" * 40)
 
cur.execute("""
    SELECT
        CASE WHEN is_elderly = 1 THEN 'Elderly (60+)' ELSE 'Younger' END AS age_group,
        method,
        COUNT(*) AS count
    FROM clean_transactions
    GROUP BY is_elderly, method
    ORDER BY is_elderly, count DESC
""")
method_results = cur.fetchall()
 
current_group = None
for row in method_results:
    if row[0] != current_group:
        current_group = row[0]
        print(f"\n  {current_group}:")
    print(f"    {row[1]:<30} {row[2]} transactions")


# -----------------------------------------------------------------
# SECTION 6: Average Amount Sent
# -----------------------------------------------------------------
print("\n💰 AVERAGE AMOUNT SENT")
print("-" * 40)
 
cur.execute("""
    SELECT
        CASE WHEN is_elderly = 1 THEN 'Elderly (60+)' ELSE 'Younger' END AS age_group,
        ROUND(AVG(amount), 2) AS avg_amount
    FROM clean_transactions
    GROUP BY is_elderly
""")
amount_results = cur.fetchall()
 
for row in amount_results:
    print(f"  {row[0]:<20} avg amount: R{row[1]}")

