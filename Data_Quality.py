import json
import csv

# Save data quality issues to a CSV file
def save_data_quality_to_csv(issues, file_name):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File Name', 'Issue Type', 'Details'])
        for issue in issues:
            writer.writerow(issue)

# Data quality issues encountered during the check
data_quality_issues = []

# Load JSON data
def load_json(file_path):
        data_json = []
        with open(file_path, 'r') as file:
                for line in file:
                        # Parse the line as JSON
                        data = json.loads(line)
                        # Process the JSON data
                        # print(data)
                        data_json.append(data)
        return data_json

users = load_json('users.json')
receipts = load_json('receipts.json')
brands = load_json('brands.json')

# Check for missing values
def check_missing_values(data, file_name):
    for record in data:
        for key, value in record.items():
            if value is None or value == "":
                data_quality_issues.append((file_name, "Missing Value", f"Key: {key}, Record: {record}"))

# Check for duplicates based on primary key
def check_duplicates(data, primary_key, file_name):
    seen = set()
    for record in data:
        key = record.get(primary_key)
        if key is not None:  # Ensure key exists and is not None
            if key in seen:
                data_quality_issues.append((file_name, "Duplicate", f"Duplicate Key: {key}, Record: {record}"))
            else:
                seen.add(key)
        else:
            data_quality_issues.append((file_name, "Missing Primary Key", f"Primary key '{primary_key}' not found in record: {record}"))

# Checking data quality issues
print("Checking users.json for data quality issues...")
check_missing_values(users, "users.json")
check_duplicates(users, "user_id", "users.json")  # Update primary key to "user_id"

print("\nChecking receipts.json for data quality issues...")
check_missing_values(receipts, "receipts.json")
check_duplicates(receipts, "receipt_id", "receipts.json")  # Update primary key to "receipt_id"

print("\nChecking brands.json for data quality issues...")
check_missing_values(brands, "brands.json")
check_duplicates(brands, "brand_id", "brands.json")  # Update primary key to "brand_id"

# Save data quality issues to CSV file
csv_file_name = "data_quality_issues.csv"
save_data_quality_to_csv(data_quality_issues, csv_file_name)
print(f"Data quality issues saved to {csv_file_name}.")