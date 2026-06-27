"""
STEP 1: GENERATE RAW DATA
=========================
This script pretends to be "the real world" — it invents transaction
records similar to what Shoprite/a bank would actually capture every
time someone sends money via Cash Send.

We are faking this because we don't have access to real bank data.
In a real company, THIS step wouldn't exist — the data would already
exist in their systems. We build it ourselves only so we have
something to feed into the rest of our pipeline.

OUTPUT: raw_transactions.csv  (this is our "source data")
"""

import csv
import random
from datetime import datetime, timedelta

# -----------------------------------------------------------------
# 1. SET UP THE BUILDING BLOCKS
# -----------------------------------------------------------------
# These are just lists we'll randomly pick from to build each row.
# Nothing clever here — just realistic-looking raw material.

random.seed(42)  # this makes the "randomness" repeatable —
                  # every time you run this script you get the SAME
                  # fake data, which is useful for testing and demoing.

elderly_senders = [
    ("Nomvula Dlamini", 71), ("Petrus Mokoena", 68), ("Agnes Sithole", 74),
    ("Johannes van Wyk", 70), ("Beauty Nkosi", 66), ("Samuel Mahlangu", 73),
    ("Maria Khumalo", 69), ("David Mthembu", 72), ("Elsie Ndlovu", 67),
    ("Joseph Radebe", 75),
]

young_senders = [
    ("Thabo Molefe", 28), ("Sarah Botha", 24), ("Kagiso Tau", 31),
    ("Lindiwe Zulu", 22), ("Pieter Smit", 35), ("Naledi Mokwena", 27),
    ("Sipho Buthelezi", 29), ("Anna Pretorius", 33), ("Karabo Sefolo", 26),
    ("Zanele Cele", 30),
]

receivers = [
    "Lwazi Dlamini", "Tumi Mokoena", "Refilwe Sithole", "Andile van Wyk",
    "Nkosana Nkosi", "Boitumelo Mahlangu", "Sibusiso Khumalo", "Palesa Mthembu",
    "Mandla Ndlovu", "Thandeka Radebe", "Lerato Molefe", "Bongani Botha",
]

methods = ["Cash Send (In-Store)", "ATM Cash Send", "Bank App Transfer", "EFT"]

# elderly users overwhelmingly rely on the in-store method —
# that's the whole point of the project, so we weight it heavily
elderly_method_weights = [0.75, 0.15, 0.07, 0.03]
young_method_weights   = [0.10, 0.10, 0.50, 0.30]

locations = [
    "Shoprite Bramley", "Shoprite Alex", "Shoprite Tembisa",
    "Shoprite Diepsloot", "Shoprite Soweto", "Pick n Pay Sandton",
    "Checkers Midrand", "Shoprite Soshanguve",
]

statuses = ["Completed", "Failed", "Pending"]
elderly_status_weights = [0.78, 0.15, 0.07]  # elderly fail more often
young_status_weights   = [0.92, 0.06, 0.02]  # younger users fail less

# -----------------------------------------------------------------
# 2. BUILD EACH ROW
# -----------------------------------------------------------------
rows = []
start_date = datetime(2025, 1, 1)

def make_transaction(sender_pool, method_weights, status_weights, is_elderly):
    name, age = random.choice(sender_pool)
    receiver = random.choice(receivers)
    method = random.choices(methods, weights=method_weights)[0]
    location = random.choice(locations)
    status = random.choices(statuses, weights=status_weights)[0]

    # elderly users send smaller, more frequent amounts (pension-linked)
    amount = round(random.uniform(50, 400), 2) if is_elderly else round(random.uniform(100, 1500), 2)

    # distance to store: elderly users in this story tend to live further
    # from a store that supports cash send (this is the "her feet hurt"
    # reality translated into a number)
    distance_km = round(random.uniform(2.5, 12.0), 1) if is_elderly else round(random.uniform(0.5, 8.0), 1)

    # random timestamp within a 6 month window, with elderly transactions
    # clustering around typical pension pay-out days (around the 25th-28th)
    if is_elderly and random.random() < 0.5:
        month_offset = random.randint(0, 5)
        day = random.randint(25, 28)
        ts = start_date + timedelta(days=30 * month_offset + day)
    else:
        ts = start_date + timedelta(days=random.randint(0, 180), hours=random.randint(6, 20))

    ts = ts + timedelta(hours=random.randint(0, 14), minutes=random.randint(0, 59))

    # a third person (e.g. another child) had to assist — common for
    # elderly + in-store method, rare otherwise
    if is_elderly and method == "Cash Send (In-Store)":
        needed_assistance = random.random() < 0.6
    else:
        needed_assistance = random.random() < 0.05

    return {
        "sender_name": name,
        "sender_age": age,
        "receiver_name": receiver,
        "amount": amount,
        "method": method,
        "location": location,
        "distance_km": distance_km,
        "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "needed_assistance": needed_assistance,
    }

# generate 350 elderly transactions, 350 younger transactions
for _ in range(350):
    rows.append(make_transaction(elderly_senders, elderly_method_weights, elderly_status_weights, is_elderly=True))

for _ in range(350):
    rows.append(make_transaction(young_senders, young_method_weights, young_status_weights, is_elderly=False))

# -----------------------------------------------------------------
# 3. DELIBERATELY MESS UP SOME ROWS
# -----------------------------------------------------------------
# Real-world data is never clean. We inject realistic problems on
# purpose so that Day 2 (cleaning) has genuine work to do, and so
# you can explain WHY each cleaning rule exists.

for row in rows:
    # 5% chance the age is missing (cashier didn't record it)
    if random.random() < 0.05:
        row["sender_age"] = ""
    # 3% chance the amount is negative due to a data entry glitch
    if random.random() < 0.03:
        row["amount"] = -abs(row["amount"])
    # 4% chance the status field has inconsistent casing/spacing
    if random.random() < 0.04:
        row["status"] = row["status"].upper() + "  "

# shuffle so elderly/young rows are mixed, like real data would be
random.shuffle(rows)

# -----------------------------------------------------------------
# 4. WRITE TO CSV
# -----------------------------------------------------------------
fieldnames = list(rows[0].keys())

with open("raw_transactions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Done. Generated {len(rows)} rows -> raw_transactions.csv")