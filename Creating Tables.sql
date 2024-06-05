CREATE DATABASE IF NOT EXISTS mydb;
USE mydb;
CREATE TABLE IF NOT EXISTS  Users (
    user_id VARCHAR(24) PRIMARY KEY,
    state VARCHAR(2),
    created_date DATETIME,
    last_login DATETIME,
    role VARCHAR(255),
    active BOOLEAN
);

CREATE TABLE IF NOT EXISTS Brands (
    brand_id VARCHAR(24) PRIMARY KEY,
    barcode VARCHAR(255),
    brand_code VARCHAR(255),
    category VARCHAR(255),
    category_code VARCHAR(255),
    cpg VARCHAR(24),
    name VARCHAR(255),
    top_brand BOOLEAN
);

CREATE TABLE IF NOT EXISTS Receipts (
    receipt_id VARCHAR(24) PRIMARY KEY,
    user_id VARCHAR(24),
    bonus_points_earned INT,
    bonus_points_earned_reason VARCHAR(255),
    create_date DATETIME,
    date_scanned DATETIME,
    finished_date DATETIME,
    modify_date DATETIME,
    points_awarded_date DATETIME,
    points_earned FLOAT,
    purchase_date DATETIME,
    purchased_item_count INT,
    rewards_receipt_status VARCHAR(255),
    total_spent FLOAT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Receipt_Items (
    receipt_item_id INT AUTO_INCREMENT PRIMARY KEY,
    receipt_id VARCHAR(24),
    brand_id VARCHAR(24),
    item_description VARCHAR(255),
    item_price FLOAT,
    quantity INT,
    FOREIGN KEY (receipt_id) REFERENCES Receipts(receipt_id),
    FOREIGN KEY (brand_id) REFERENCES Brands(brand_id)
);

