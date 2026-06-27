"""
STEP 4: ANALYTICS + VISUALIZATION
===================================
This is where we actually ask the data questions and turn the
answers into charts. Every query below follows the same basic
shape: SELECT columns FROM table, sometimes with WHERE (a filter)
or GROUP BY (split into buckets, like an Excel pivot table).

OUTPUT: charts/ folder containing PNG images, one per question.
"""

import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect("transactions.db")
cur = conn.cursor()

os.makedirs("charts", exist_ok=True)

# -----------------------------------------------------------------
# QUESTION 1: Do elderly senders fail more often than younger senders?
# -----------------------------------------------------------------
# GROUP BY is_elderly, status -> split rows into buckets by BOTH
# columns at once, then COUNT how many rows fall in each bucket.
query1 = """
SELECT
    CASE WHEN is_elderly = 1 THEN 'Elderly (60+)' ELSE 'Younger' END AS age_group,
    status,
    COUNT(*) AS num_transactions
FROM clean_transactions
GROUP BY is_elderly, status
"""
cur.execute(query1)
results1 = cur.fetchall()
print("Q1: Status counts by age group")
for row in results1:
    print("  ", row)

elderly_total = sum(r[2] for r in results1 if r[0] == "Elderly (60+)")
young_total = sum(r[2] for r in results1 if r[0] == "Younger")

elderly_failed = sum(r[2] for r in results1 if r[0] == "Elderly (60+)" and r[1] == "Failed")
young_failed = sum(r[2] for r in results1 if r[0] == "Younger" and r[1] == "Failed")

elderly_fail_rate = round(100 * elderly_failed / elderly_total, 1)
young_fail_rate = round(100 * young_failed / young_total, 1)

plt.figure(figsize=(5, 4))
plt.bar(["Elderly (60+)", "Younger"], [elderly_fail_rate, young_fail_rate], color=["#d9534f", "#5cb85c"])
plt.ylabel("Failure rate (%)")
plt.title("Transaction Failure Rate: Elderly vs Younger")
for i, v in enumerate([elderly_fail_rate, young_fail_rate]):
    plt.text(i, v + 0.5, f"{v}%", ha="center")
plt.tight_layout()
plt.savefig("charts/q1_failure_rate.png")
plt.close()
print(f"  -> Elderly fail rate: {elderly_fail_rate}% | Younger fail rate: {young_fail_rate}%\n")

# -----------------------------------------------------------------
# QUESTION 2: How much further do elderly senders travel?
# -----------------------------------------------------------------
query2 = """
SELECT
    CASE WHEN is_elderly = 1 THEN 'Elderly (60+)' ELSE 'Younger' END AS age_group,
    AVG(distance_km) AS avg_distance
FROM clean_transactions
GROUP BY is_elderly
"""
cur.execute(query2)
results2 = cur.fetchall()
print("Q2: Average distance traveled by age group")
for row in results2:
    print("  ", row)

labels2 = [r[0] for r in results2]
values2 = [round(r[1], 1) for r in results2]

plt.figure(figsize=(5, 4))
plt.bar(labels2, values2, color=["#d9534f", "#5cb85c"])
plt.ylabel("Average distance (km)")
plt.title("Average Distance Traveled to Complete a Transaction")
for i, v in enumerate(values2):
    plt.text(i, v + 0.1, f"{v} km", ha="center")
plt.tight_layout()
plt.savefig("charts/q2_distance.png")
plt.close()
print()

# -----------------------------------------------------------------
# QUESTION 3: How often does an elderly sender need a third person's help?
# -----------------------------------------------------------------
query3 = """
SELECT
    CASE WHEN is_elderly = 1 THEN 'Elderly (60+)' ELSE 'Younger' END AS age_group,
    AVG(needed_assistance) * 100 AS pct_needed_assistance
FROM clean_transactions
GROUP BY is_elderly
"""
cur.execute(query3)
results3 = cur.fetchall()
print("Q3: % of transactions needing third-party assistance")
for row in results3:
    print("  ", row)

labels3 = [r[0] for r in results3]
values3 = [round(r[1], 1) for r in results3]

plt.figure(figsize=(5, 4))
plt.bar(labels3, values3, color=["#d9534f", "#5cb85c"])
plt.ylabel("% needing assistance")
plt.title("Transactions Requiring a Third Person's Help")
for i, v in enumerate(values3):
    plt.text(i, v + 1, f"{v}%", ha="center")
plt.tight_layout()
plt.savefig("charts/q3_assistance.png")
plt.close()
print()

# -----------------------------------------------------------------
# QUESTION 4: Which method is most common, elderly vs younger?
# -----------------------------------------------------------------
query4 = """
SELECT
    CASE WHEN is_elderly = 1 THEN 'Elderly (60+)' ELSE 'Younger' END AS age_group,
    method,
    COUNT(*) AS num_transactions
FROM clean_transactions
GROUP BY is_elderly, method
"""
cur.execute(query4)
results4 = cur.fetchall()
print("Q4: Method usage by age group")
for row in results4:
    print("  ", row)

methods = sorted(set(r[1] for r in results4))
elderly_counts = [next((r[2] for r in results4 if r[0] == "Elderly (60+)" and r[1] == m), 0) for m in methods]
young_counts = [next((r[2] for r in results4 if r[0] == "Younger" and r[1] == m), 0) for m in methods]

x = np.arange(len(methods))
width = 0.35

plt.figure(figsize=(7, 4.5))
plt.bar(x - width/2, elderly_counts, width, label="Elderly (60+)", color="#d9534f")
plt.bar(x + width/2, young_counts, width, label="Younger", color="#5cb85c")
plt.xticks(x, methods, rotation=20, ha="right")
plt.ylabel("Number of transactions")
plt.title("Transaction Method Used: Elderly vs Younger")
plt.legend()
plt.tight_layout()
plt.savefig("charts/q4_methods.png")
plt.close()
print()

# -----------------------------------------------------------------
# QUESTION 5: When do elderly users transact most? (by day of month)
# -----------------------------------------------------------------
# strftime('%d', timestamp) pulls just the DAY number out of a full
# date+time value, e.g. "2025-05-26 07:24:00" -> "26"
query5 = """
SELECT
    strftime('%d', timestamp) AS day_of_month,
    COUNT(*) AS num_transactions
FROM clean_transactions
WHERE is_elderly = 1
GROUP BY day_of_month
ORDER BY day_of_month
"""
cur.execute(query5)
results5 = cur.fetchall()
print("Q5: Elderly transactions by day of month")
for row in results5:
    print("  ", row)

days = [r[0] for r in results5]
counts = [r[1] for r in results5]

plt.figure(figsize=(9, 4))
plt.bar(days, counts, color="#5b9bd5")
plt.xlabel("Day of month")
plt.ylabel("Number of elderly transactions")
plt.title("Elderly Transactions by Day of Month (peaks near pension pay-out)")
plt.tight_layout()
plt.savefig("charts/q5_timing.png")
plt.close()

conn.close()
print("\nAll charts saved to charts/ folder.")