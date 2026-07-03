import csv
import random
from datetime import datetime, timedelta


random.seed(42)  
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


elderly_method_weights = [0.75, 0.15, 0.07, 0.03]
young_method_weights   = [0.10, 0.10, 0.50, 0.30]

locations = [
    "Shoprite Bramley", "Shoprite Alex", "Shoprite Tembisa",
    "Shoprite Diepsloot", "Shoprite Soweto", "Pick n Pay Sandton",
    "Checkers Midrand", "Shoprite Soshanguve",
]

statuses = ["Completed", "Failed", "Pending"]
elderly_status_weights = [0.78, 0.15, 0.07]  
young_status_weights   = [0.92, 0.06, 0.02]  


rows = []
start_date = datetime(2025, 1, 1)

def make_transaction(sender_pool, method_weights, status_weights, is_elderly):
    name, age = random.choice(sender_pool)
    receiver = random.choice(receivers)
    method = random.choices(methods, weights=method_weights)[0]
    location = random.choice(locations)
    status = random.choices(statuses, weights=status_weights)[0]

    
    amount = round(random.uniform(50, 400), 2) if is_elderly else round(random.uniform(100, 1500), 2)

   
    distance_km = round(random.uniform(2.5, 12.0), 1) if is_elderly else round(random.uniform(0.5, 8.0), 1)

    
    if is_elderly and random.random() < 0.5:
        month_offset = random.randint(0, 5)
        day = random.randint(25, 28)
        ts = start_date + timedelta(days=30 * month_offset + day)
    else:
        ts = start_date + timedelta(days=random.randint(0, 180), hours=random.randint(6, 20))

    ts = ts + timedelta(hours=random.randint(0, 14), minutes=random.randint(0, 59))

    
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

for _ in range(350):
    rows.append(make_transaction(elderly_senders, elderly_method_weights, elderly_status_weights, is_elderly=True))

for _ in range(350):
    rows.append(make_transaction(young_senders, young_method_weights, young_status_weights, is_elderly=False))


for row in rows:
  
    if random.random() < 0.05:
        row["sender_age"] = ""
   
    if random.random() < 0.03:
        row["amount"] = -abs(row["amount"])
    
    if random.random() < 0.04:
        row["status"] = row["status"].upper() + "  "


random.shuffle(rows)


fieldnames = list(rows[0].keys())

with open("raw_transactions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Done. Generated {len(rows)} rows -> raw_transactions.csv")
