"""
REFLECTION:
1. Python vs. Excel for ETL:
Python excels at automating repetitive transformations across large or multiple CSV files without manual clicking, ensuring exact reproducibility every time the script runs. Excel is easier for quick visual inspection, ad-hoc formatting, and building interactive charts for non-technical stakeholders, though manual edits in Excel are harder to audit and prone to accidental overwrites.

2. Real-World Business Process for Append-Mode Logs:
An automated nightly inventory sync or payment reconciliation job benefits from an append-mode log file because every execution needs to leave an immutable audit trail of timestamps, record counts, and totals. Append mode ("a") guarantees that historical run records are preserved rather than overwritten, allowing analysts to trace when anomalies or missing batches occurred.
"""

import csv
from datetime import datetime

# --- EXERCISE 1: Verify file path ---
input_file = "data/sales.csv"

# --- EXERCISE 2: Read and print raw rows ---
print("=== EXERCISE 2: Raw Rows ===")
with open(input_file, mode="r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# --- EXERCISE 3: Skip the header ---
print("\n=== EXERCISE 3: Skip Header ===")
with open(input_file, mode="r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f"Header: {header}")
    for row in reader:
        print(row)

# --- EXERCISE 4: Compute totals ---
print("\n=== EXERCISE 4: Compute Totals ===")
overall_revenue = 0.0
with open(input_file, mode="r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        total = price * quantity
        overall_revenue += total
        print(f"{product}: {quantity} units × ${price:.2f} = ${total:.2f}")

print(f"Overall Total Revenue: ${overall_revenue:.2f}")

# --- EXERCISE 5: Filter and write ---
print("\n=== EXERCISE 5: Filter and Write ===")
cleaned_file = "data/cleaned.csv"
total_rows = 0
written_rows = 0

with open(input_file, mode="r", newline="", encoding="utf-8") as infile, \
     open(cleaned_file, mode="w", newline="", encoding="utf-8") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    next(reader)  # Skip original header
    writer.writerow(["Product", "Price", "Qty", "Total"])

    for row in reader:
        total_rows += 1
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        total = price * quantity

        if total > 100:
            writer.writerow([product, f"{price:.2f}", quantity, f"{total:.2f}"])
            written_rows += 1

print(f"Wrote {written_rows} qualifying rows out of {total_rows} original rows to {cleaned_file}.")

# --- EXERCISE 6: csv.DictReader ---
print("\n=== EXERCISE 6: csv.DictReader ===")
# csv.DictReader is preferable when CSV files have many columns or columns might be reordered, making code self-documenting by column name.
# csv.reader is preferable for simple, fixed-structure files where minimal memory overhead and slightly faster iteration are priorities.
dict_overall_revenue = 0.0
with open(input_file, mode="r", newline="", encoding="utf-8") as f:
    dict_reader = csv.DictReader(f)
    for row in dict_reader:
        product = row["product"]
        price = float(row["price"])
        quantity = int(row["quantity"])
        total = price * quantity
        dict_overall_revenue += total
        print(f"{product}: {quantity} units × ${price:.2f} = ${total:.2f}")

print(f"DictReader Overall Total Revenue: ${dict_overall_revenue:.2f}")

# --- EXERCISE 7: Sales summary by product ---
print("\n=== EXERCISE 7: Sales Summary by Product ===")
product_summary = {}
with open(input_file, mode="r", newline="", encoding="utf-8") as f:
    dict_reader = csv.DictReader(f)
    for row in dict_reader:
        product = row["product"]
        total = float(row["price"]) * int(row["quantity"])
        product_summary[product] = product_summary.get(product, 0.0) + total

for product in sorted(product_summary):
    print(f"{product}: ${product_summary[product]:.2f}")

# --- EXERCISE 8: Append mode log ---
print("\n=== EXERCISE 8: Append Mode Log ===")
log_file = "data/run_log.txt"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(log_file, mode="a", encoding="utf-8") as f:
    f.write(f"[{timestamp}] Pipeline completed. Total Revenue: ${overall_revenue:.2f}\n")

print(f"Logged run at {timestamp} to {log_file}.")