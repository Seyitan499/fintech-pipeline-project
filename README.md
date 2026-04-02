📌 Fintech Data Pipeline: Loan & Transaction Analytics System
🚀 Project Overview

This project simulates a fintech data system, similar to platforms like Moniepoint, where raw financial data is processed into structured, analytics-ready datasets.

It demonstrates how transactional and loan data flows through a data pipeline — from raw ingestion to transformation and data serving.

🏗 Architecture
Raw CSV Data → Python (Data Cleaning) → SQL Database → SQL Transformations → Flask API
⚙️ Tech Stack
Python (Pandas)
SQL (PostgreSQL/MySQL)
Flask (API Development)
Git & GitHub

🔄 Data Pipeline
Extracted raw datasets (customers, accounts, transactions, loans, repayments)
Cleaned and transformed data using Python
Loaded structured data into a relational database
Performed SQL transformations to create analytics-ready tables

🧱 Data Modeling

Implemented a layered data architecture:
Raw Layer (Bronze): Original datasets
Clean Layer (Silver): Cleaned and structured data
Analytics Layer (Gold): Aggregated tables for reporting

🔌 API Endpoints
/customers → Customer summary
/transactions → Transaction data
/loans → Loan performance

📊 Key Insights
Loan default rates across customers
Transaction trends over time
Customer-level financial behavior
