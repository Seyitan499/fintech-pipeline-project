# fintech_pipeline_api_updated.py

import os
import pandas as pd
from sqlalchemy import create_engine, inspect
from flask import Flask, jsonify

# =====================
# 1. Setup Paths and Database
# =====================
data_folder = "DATA"  # Folder containing all raw CSVs
cleaned_folder = os.path.join(data_folder, "cleaned")
os.makedirs(cleaned_folder, exist_ok=True)

# SQLite database
engine = create_engine('sqlite:///fintech.db', echo=False)

# =====================
# 2. Load, Clean, and Save CSVs
# =====================
csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

for file in csv_files:
    file_path = os.path.join(data_folder, file)
    table_name = file.replace('.csv', '').lower()
    
    # Load CSV
    df = pd.read_csv(file_path)
    
    # Clean data
    df = df.drop_duplicates()
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()
    for col in df.columns:
        if 'date' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Save cleaned CSV
    cleaned_csv_path = os.path.join(cleaned_folder, f"cleaned_{file}")
    df.to_csv(cleaned_csv_path, index=False)
    
    # Load into SQLite
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"Processed {file} → Table: {table_name}")

# =====================
# 3. Create Analytics Tables
# =====================
try:
    # Load key tables
    loans = pd.read_sql("SELECT * FROM loans", engine)
    transactions = pd.read_sql("SELECT * FROM transactions", engine)
    customers = pd.read_sql("SELECT * FROM customers", engine)

    # a) Loans by customer
    loans_by_customer = loans.groupby('customer_id')['loan_amount'].sum().reset_index()
    loans_by_customer.to_sql('loans_by_customer', engine, if_exists='replace', index=False)

    # b) Loans by country
    if 'country' in customers.columns:
        loans_with_country = loans.merge(customers[['customer_id','country']], on='customer_id', how='left')
        loans_by_country = loans_with_country.groupby('country')['loan_amount'].sum().reset_index()
        loans_by_country.to_sql('loans_by_country', engine, if_exists='replace', index=False)

    # c) Monthly loan trends
    loans['loan_month'] = loans['loan_date'].dt.to_period('M')
    monthly_loans = loans.groupby('loan_month')['loan_amount'].sum().reset_index()
    monthly_loans.to_sql('monthly_loans', engine, if_exists='replace', index=False)

    # d) Customer repayment status
    transactions['repayment'] = transactions['amount']  # assumes amount column = repayment
    repayment_status = transactions.groupby('customer_id')['repayment'].sum().reset_index()
    repayment_status = repayment_status.merge(loans_by_customer, on='customer_id', how='left')
    repayment_status['status'] = repayment_status.apply(
        lambda x: 'Paid' if x['repayment'] >= x['loan_amount'] else 'Pending', axis=1)
    repayment_status.to_sql('repayment_status', engine, if_exists='replace', index=False)

    print("\nAnalytics tables created successfully!")
except Exception as e:
    print("Analytics creation skipped due to error:", e)

# =====================
# 4. Setup Flask API
# =====================
app = Flask(__name__)

def get_table_json(table_name, limit=None):
    query = f"SELECT * FROM {table_name}"
    if limit:
        query += f" LIMIT {limit}"
    df = pd.read_sql(query, engine)
    return df.to_dict(orient='records')

@app.route("/tables")
def list_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return jsonify(tables)

@app.route("/table/<table_name>")
def table_data(table_name):
    try:
        data = get_table_json(table_name, limit=100)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/analytics/loans_by_customer")
def api_loans_by_customer():
    return jsonify(get_table_json("loans_by_customer"))

@app.route("/analytics/loans_by_country")
def api_loans_by_country():
    return jsonify(get_table_json("loans_by_country"))

@app.route("/analytics/monthly_loans")
def api_monthly_loans():
    return jsonify(get_table_json("monthly_loans"))

@app.route("/analytics/repayment_status")
def api_repayment_status():
    return jsonify(get_table_json("repayment_status"))

# =====================
# 5. Run Flask API
# =====================
if __name__ == "__main__":
    print("\nETL + Analytics + API is ready! Visit http://127.0.0.1:5000/tables to explore.")
    app.run(debug=True)