"""
STEP 4b: ADDITIONAL ANALYSIS
==============================
This script adds a 6th insight to the analytics layer:
Average transaction amount sent by elderly vs younger users.

This matters because it reveals the financial scale of the problem —
elderly users typically send smaller amounts more frequently (pension-
linked behaviour), while younger users send larger, less frequent
transfers. Understanding this helps inform transfer limits and fee
structures for an accessibility-first system.

OUTPUT: charts/q6_avg_amount.png
"""

import sqlite3
import matplotlib.pyplot as plt
import os

conn = sqlite3.connect("transactions.db")
cur = conn.cursor()

os.makedirs("charts", exist_ok=True)

query = """
SELECT
    CASE WHEN is_elderly = 1 THEN 'Elderly (60+)' ELSE 'Younger' END AS age_group,
    ROUND(AVG(amount), 2) AS avg_amount,
    COUNT(*) AS num_transactions,
    ROUND(MIN(amount), 2) AS min_amount,
    ROUND(MAX(amount), 2) AS max_amount
FROM clean_transactions
GROUP BY is_elderly
"""

cur.execute(query)
results = cur.fetchall()

print("Q6: Average transaction amount by age group")
print(f"{'Age Group':<20} {'Avg Amount':>12} {'Count':>8} {'Min':>10} {'Max':>10}")
print("-" * 62)
for row in results:
    print(f"{row[0]:<20} R{row[1]:>10} {row[2]:>8} R{row[3]:>8} R{row[4]:>8}")

labels = [r[0] for r in results]
averages = [r[1] for r in results]
counts = [r[2] for r in results]

fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(labels, averages, color=["#d9534f", "#5cb85c"], width=0.5)
ax.set_ylabel("Average amount sent (R)")
ax.set_title("Average Transaction Amount: Elderly vs Younger")

for bar, avg, count in zip(bars, averages, counts):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 5,
        f"R{avg}\n({count} transactions)",
        ha="center", va="bottom", fontsize=9
    )

plt.tight_layout()
plt.savefig("charts/q6_avg_amount.png")
plt.close()

conn.close()
print("\nChart saved to charts/q6_avg_amount.png")