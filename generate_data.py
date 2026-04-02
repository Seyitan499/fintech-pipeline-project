import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

num_customers = 100

# Customers
customers = []
for i in range(num_customers):
    customers.append([
        f"C{i+1:03}",
        fake.first_name(),
        fake.last_name(),
        random.choice(["Male", "Female"]),
        random.choice(["Lagos", "Abuja", "Port Harcourt"]),
        fake.date_between(start_date='-2y', end_date='today')
    ])

customers_df = pd.DataFrame(customers, columns=[
    "customer_id", "first_name", "last_name", "gender", "city", "signup_date"
])

# Accounts
accounts = []
for i in range(num_customers):
    accounts.append([
        f"A{i+1:03}",
        customers_df.iloc[i]["customer_id"],
        random.choice(["Savings", "Current"]),
        random.randint(10000, 500000),
        fake.date_between(start_date='-2y', end_date='today')
    ])

accounts_df = pd.DataFrame(accounts, columns=[
    "account_id", "customer_id", "account_type", "balance", "created_at"
])

# Transactions
transactions = []
for i in range(500):
    acc = random.choice(accounts_df["account_id"].tolist())
    transactions.append([
        f"T{i+1:04}",
        acc,
        random.choice(["credit", "debit"]),
        random.randint(1000, 100000),
        fake.date_between(start_date='-1y', end_date='today')
    ])

transactions_df = pd.DataFrame(transactions, columns=[
    "transaction_id", "account_id", "transaction_type", "amount", "transaction_date"
])

# Loans
loans = []
for i in range(50):
    cust = random.choice(customers_df["customer_id"].tolist())
    loans.append([
        f"L{i+1:03}",
        cust,
        random.randint(50000, 500000),
        round(random.uniform(0.1, 0.2), 2),
        fake.date_between(start_date='-1y', end_date='today'),
        random.choice(["active", "closed", "defaulted"])
    ])

loans_df = pd.DataFrame(loans, columns=[
    "loan_id", "customer_id", "loan_amount", "interest_rate", "loan_date", "loan_status"
])

# Repayments
repayments = []
for i in range(100):
    loan = random.choice(loans_df["loan_id"].tolist())
    repayments.append([
        f"R{i+1:03}",
        loan,
        random.randint(10000, 100000),
        fake.date_between(start_date='-1y', end_date='today')
    ])

repayments_df = pd.DataFrame(repayments, columns=[
    "repayment_id", "loan_id", "amount_paid", "payment_date"
])

# Save files
customers_df.to_csv("data/customers.csv", index=False)
accounts_df.to_csv("data/accounts.csv", index=False)
transactions_df.to_csv("data/transactions.csv", index=False)
loans_df.to_csv("data/loans.csv", index=False)
repayments_df.to_csv("data/repayments.csv", index=False)

print("Datasets generated successfully!")