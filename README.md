# ElderEase-transfers

# ElderEase Transfers — Accessibility-First Transaction Analytics Pipeline

## The Problem

In many South African households, elderly and low-literacy family members rely on in-person Cash Send services (e.g. at Shoprite) to send money to relatives — often a child away at school. This process requires:

- Physically traveling to a store, which is difficult for elderly users with mobility issues
- The receiver also traveling to a store, with an ID, to collect the cash
- Frequent reliance on a third family member to assist with the process

This project is inspired by a real situation: an elderly woman who sends money to her child via in-store Cash Send, despite physical pain from walking, because she has no simpler alternative.

## What This Project Actually Is

**This is not a money transfer app.** It does not move real money, and elderly users do not use it directly.

This is a **data engineering pipeline** that simulates and analyzes transaction data to answer a real question: *where exactly does the process break down for elderly users, and by how much?*

The goal is to produce evidence, not a product that could justify and inform the design of a real accessibility-first transfer system in the future (e.g. an SMS or voice-based interface, discussed under Future Work below).

## Pipeline Stages

| Stage | What it does | File |
|---|---|---|
| 1. Data Generation | Creates realistic synthetic transaction data (since real bank data isn't accessible) | `01_generate_data.py` |
| 2. Ingestion | Loads raw CSV data into a structured SQLite database | `02_ingest.py` |
| 3. Transformation | Cleans messy data (missing values, inconsistent text, bad entries) and adds calculated fields | `03_transform.py` |
| 4. Analytics & Visualization | Runs SQL queries to answer key questions and produces charts | `04_analyze.py` |

Each stage writes its output before the next stage begins, and raw data is never overwritten, only added to, so the original source data can always be re-checked.

## Key Questions This Pipeline Answers

- Do elderly senders (60+) experience a higher transaction failure rate than younger senders?
- How much further do elderly senders travel to complete a transaction?
- How often does an elderly sender need a third person's assistance to complete a transaction?
- Which transaction method is most common among elderly vs. younger users?
- When do elderly users transact most, and does it line up with pension pay-out dates?

## Tech Stack

- **Python** — data generation and scripting
- **SQLite** — lightweight database for structured storage
- **SQL** — data cleaning and analysis queries
- **Matplotlib** — chart generation

Chosen deliberately for a solo project: no cloud setup overhead, fully runnable on a single laptop, while still demonstrating the same pipeline stages (ingestion, storage, transformation, analytics, visualization) used in production tools like Azure Data Factory, Blob Storage, and Power BI.

## How to Run

```bash
pip install -r requirements.txt
python3 01_generate_data.py
python3 02_ingest.py
python3 03_transform.py
python3 04_analyze.py
```

Charts will be saved to the `charts/` folder.

## Honest Scope & Limitations

- All transaction data is **synthetic**, generated to reflect realistic patterns, not pulled from any real financial institution.
- This project does not include a user-facing app, SMS system, or chatbot. Elderly users do not interact with this system directly.
- The purpose is to demonstrate a complete, defensible data pipeline and produce data-driven evidence of a real accessibility gap — not to deliver a finished product.

## Future Work (Not Built — Roadmap Only)

- A voice or SMS-based interface for low-literacy users, built on top of the insights from this pipeline
- A family-linked monitoring feature, so a relative can check transaction status without traveling
- Real-time fraud/anomaly flagging for unusual transaction patterns



## Author

Mapaseka — WeThinkCode_ Data Engineering Elective Project