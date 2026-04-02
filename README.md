# Fintech Data Engineering Pipeline

This project demonstrates an **end-to-end ETL pipeline** for fintech data, including data cleaning, analytics table creation, and exposure via a **Flask API**.

---

## Project Overview

- Built an **ETL pipeline** using Python and SQL to process multiple raw fintech datasets (`loans`, `transactions`, `customers`).
- Cleaned and transformed data to create **analytics tables**:
  - `loans_by_customer` – total loans per customer  
  - `loans_by_country` – total loans per country  
  - `monthly_loans` – monthly loan trends  
  - `repayment_status` – repayment tracking per customer
- Stored cleaned data in a **SQLite database (`fintech.db`)**.
- Developed a **Flask API** to expose processed datasets for downstream applications.

**Skills demonstrated:** Python (Pandas, SQLAlchemy, Flask), SQL, ETL pipelines, data cleaning, API development, data analytics.

---

## Project Structure


fintech-pipeline-project/
│
├── DATA/ # Raw CSV files
│ ├── loans.csv
│ ├── transactions.csv
│ ├── customers.csv
│ └── ...
│
├── DATA/cleaned/ # Cleaned CSV files (auto-generated)
│ ├── cleaned_loans.csv
│ ├── cleaned_transactions.csv
│ └── ...
│
│
├── fintech_etl_pipeline.py # Main ETL + Analytics + Flask API script
├── fintech.db # SQLite database (generated locally)
├── requirements.txt # Python dependencies
└── README.md # Project overview and instructions


---

## Running the Project Locally

1. **Install dependencies:**

```bash
pip install -r requirements.txt
Run the ETL + API script:
python fintech_etl_pipeline.py
Open your browser to explore API endpoints:
http://127.0.0.1:5000/tables → list all tables
http://127.0.0.1:5000/analytics/loans_by_customer
http://127.0.0.1:5000/analytics/loans_by_country
http://127.0.0.1:5000/analytics/monthly_loans
http://127.0.0.1:5000/analytics/repayment_status

Optional HTML table endpoints (for screenshots):

http://127.0.0.1:5000/analytics/loans_by_customer_html
http://127.0.0.1:5000/analytics/loans_by_country_html
API Usage Example
List All Tables
curl http://127.0.0.1:5000/tables

Example Output:

["loans","transactions","customers","loans_by_customer","loans_by_country","monthly_loans","repayment_status"]
Get Loans by Customer
curl http://127.0.0.1:5000/analytics/loans_by_customer

Example Output:

[
  {"customer_id":1,"loan_amount":5000},
  {"customer_id":2,"loan_amount":12000},
  {"customer_id":3,"loan_amount":7500}
]