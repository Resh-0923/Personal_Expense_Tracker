-- schema_v1.sql
-- Initial database schema

CREATE TABLE user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE expense (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    expense_name VARCHAR(150) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    date DATE NOT NULL,
    category VARCHAR(100),
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
