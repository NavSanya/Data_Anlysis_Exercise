import json
import datetime

unix_timestamp = 1609687537858
datetime_object = datetime.datetime.fromtimestamp(unix_timestamp / 1000)
sql_datetime_format = datetime_object.strftime("%Y-%m-%d %H:%M:%S")

print(sql_datetime_format)

# Function to generate SQL insert statements for Users table
def generate_users_sql(users_data):
    sql_statements = []
    for user in users_data:
        user_id = user['_id'].get('$oid', '').replace("'", "''")
        state = user.get('state', '').replace("'", "''")
        created_date = user['createdDate'].get('$date', '')
        datetime_object = datetime.datetime.fromtimestamp(created_date / 1000)
        created_date = datetime_object.strftime("%Y-%m-%d %H:%M:%S")
        last_login = user.get('lastLogin', {}).get('$date', '')
        if last_login:
            datetime_object = datetime.datetime.fromtimestamp(last_login / 1000)
            last_login = f"'{datetime_object.strftime('%Y-%m-%d %H:%M:%S')}'"
        else:
            last_login = 'NULL'
        role = user.get('role', '').replace("'", "''")
        active = user.get('active', False)  # Assuming default value if 'active' key is missing or null
        sql = f"INSERT IGNORE INTO Users (user_id, state, created_date, last_login, role, active) VALUES ('{user_id}', '{state}', '{created_date}', {last_login}, '{role}', {active});"
        sql_statements.append(sql)
    return sql_statements



# Function to generate SQL insert statements for Receipts table
def generate_receipts_sql(receipts_data):
    sql_statements = []
    for receipt in receipts_data:
        receipt_id = receipt['_id'].get('$oid', '').replace("'", "''")
        user_id = receipt.get('userId', '').replace("'", "''")
        bonus_points_earned = receipt.get('bonusPointsEarned', 'NULL')  # Treat as NULL if missing
        bonus_points_earned_reason = receipt.get('bonusPointsEarnedReason', '').replace("'", "''")
        create_date = datetime.datetime.fromtimestamp(receipt['createDate'].get('$date', 0) / 1000).strftime("%Y-%m-%d %H:%M:%S")
        date_scanned = datetime.datetime.fromtimestamp(receipt['dateScanned'].get('$date', 0) / 1000).strftime("%Y-%m-%d %H:%M:%S")
        finished_date = receipt.get('finishedDate', {}).get('$date', 'NULL')  # Treat as NULL if missing
        if finished_date!= 'NULL':
            finished_date = f"'{datetime.datetime.fromtimestamp(finished_date / 1000).strftime('%Y-%m-%d %H:%M:%S')}'"
        modify_date = datetime.datetime.fromtimestamp(receipt['modifyDate'].get('$date', 0) / 1000).strftime("%Y-%m-%d %H:%M:%S")
        points_awarded_date = receipt.get('pointsAwardedDate', {}).get('$date', 'NULL')  # Treat as NULL if missing
        if points_awarded_date!= 'NULL':
            points_awarded_date = f"'{datetime.datetime.fromtimestamp(points_awarded_date / 1000).strftime('%Y-%m-%d %H:%M:%S')}'"
        points_earned = receipt.get('pointsEarned', 'NULL')  # Treat as NULL if missing
        purchased_item_count = receipt.get('purchasedItemCount', 'NULL')  # Treat as NULL if missing
        rewards_receipt_status = receipt.get('rewardsReceiptStatus', '').replace("'", "''")
        total_spent = receipt.get('totalSpent', '')
        if total_spent == '':
            total_spent = 'NULL'  # If total_spent is an empty string, treat as NULL in SQL
        else:
            total_spent = f"'{total_spent}'"
        
        purchase_date = receipt.get('purchaseDate', {}).get('$date', 'NULL')  # Treat as NULL if missing
        if purchase_date!= 'NULL':
            purchase_date = datetime.datetime.fromtimestamp(purchase_date / 1000).strftime("%Y-%m-%d %H:%M:%S")
            purchase_date = f"'{purchase_date}'"

        sql = f"INSERT IGNORE INTO Receipts (receipt_id, user_id, bonus_points_earned, bonus_points_earned_reason, create_date, date_scanned, finished_date, modify_date, points_awarded_date, points_earned, purchase_date, purchased_item_count, rewards_receipt_status, total_spent) VALUES ('{receipt_id}', '{user_id}', {bonus_points_earned}, '{bonus_points_earned_reason}', '{create_date}', '{date_scanned}', {finished_date}, '{modify_date}', {points_awarded_date}, {points_earned}, {purchase_date}, {purchased_item_count}, '{rewards_receipt_status}', {total_spent});"
        sql_statements.append(sql)
    return sql_statements



# Function to generate SQL insert statements for Receipt_Items table
def generate_receipt_items_sql(receipts_data):
    sql_statements = []
    for receipt in receipts_data:
        receipt_id = receipt['_id'].get('$oid', '').replace("'", "''")
        for item in receipt.get('rewardsReceiptItemList', []):
            brand_id = item.get('brandId', 'NULL').replace("'", "''")
            if brand_id == 'NULL':
                brand_id = 'NULL'
            else:
                brand_id = f"'{brand_id}'"
            item_description = item.get('description', '').replace("'", "''")
            item_price = item.get('finalPrice', 'NULL')  # Assuming item price is represented by 'finalPrice'
            if item_price != 'NULL':
                item_price = f"'{item_price}'"
            quantity = item.get('quantityPurchased', 'NULL')
            if quantity != 'NULL':
                quantity = f"'{quantity}'"
            
            sql = f"INSERT IGNORE INTO Receipt_Items (receipt_id, brand_id, item_description, item_price, quantity) VALUES ('{receipt_id}', {brand_id}, '{item_description}', {item_price}, {quantity});"
            sql_statements.append(sql)
    return sql_statements






# Function to generate SQL insert statements for Brands table
def generate_brands_sql(brands_data):
    sql_statements = []
    for brand in brands_data:
        brand_id = brand['_id'].get('$oid', '').replace("'", "''")
        barcode = brand.get('barcode', '').replace("'", "''")
        brand_code = brand.get('brandCode', '').replace("'", "''")
        category = brand.get('category', '').replace("'", "''")
        category_code = brand.get('categoryCode', '').replace("'", "''")
        cpg = brand['cpg']['$id'].get('$oid', '')
        name = brand.get('name', '').replace("'", "''")
        top_brand = brand.get('topBrand', False)  # Assuming default value if 'topBrand' key is missing
        sql = f"INSERT INTO Brands (brand_id, barcode, brand_code, category, category_code, cpg, name, top_brand) VALUES ('{brand_id}', '{barcode}', '{brand_code}', '{category}', '{category_code}', '{cpg}', '{name}', {top_brand});"
        sql_statements.append(sql)
    return sql_statements



users_data = []
receipts_data = []
brands_data = []

# Read data from JSON files
with open('users.json', 'r') as f:
        for line in f:
                # Parse the line as JSON
                data = json.loads(line)
                # Process the JSON data
                # print(data)
                users_data.append(data)
        print("Users")
        print(data)

with open('receipts.json', 'r') as f:
        for line in f:
                # Parse the line as JSON
                data = json.loads(line)
                # Process the JSON data
                # print(data)
                receipts_data.append(data)
        print("Reciepts")
        print(data)

with open('brands.json', 'r') as f:
        for line in f:
                # Parse the line as JSON
                data = json.loads(line)
                # Process the JSON data
                # print(data)
                brands_data.append(data)
        print("Brands")
        print(data)

# Generate SQL insert statements for each table
users_sql = generate_users_sql(users_data)
receipts_sql = generate_receipts_sql(receipts_data)
receipt_items_sql = generate_receipt_items_sql(receipts_data)
brands_sql = generate_brands_sql(brands_data)

# Write SQL insert statements to files
with open('users_insert.sql', 'w') as f:
    f.write('\n'.join(users_sql))

with open('receipts_insert.sql', 'w') as f:
    f.write('\n'.join(receipts_sql))

with open('receipt_items_insert.sql', 'w') as f:
    f.write('\n'.join(receipt_items_sql))

with open('brands_insert.sql', 'w') as f:
    f.write('\n'.join(brands_sql))
