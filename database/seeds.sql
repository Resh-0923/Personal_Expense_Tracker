-- seeds.sql
-- Sample records for Personal Expense Tracker (Corrected)

-- USERS (5 users)
INSERT INTO user (username, password) VALUES
('demo_user', 'hashed_pw1'),
('student01', 'hashed_pw2'),
('student02', 'hashed_pw3'),
('student03', 'hashed_pw4'),
('student04', 'hashed_pw5');

-- CATEGORIES (4 categories only)
INSERT INTO category (category_name) VALUES
('Food'),
('Transportation'),
('Utilities'),
('Entertainment');

-- EXPENSES (20+ records)
INSERT INTO expense (user_id, category_id, expense_name, amount, date, notes) VALUES
(1, 1, 'Lunch', 120.00, '2024-11-01', 'Cafeteria'),
(1, 1, 'Coffee', 95.00, '2024-11-02', 'Study break'),
(1, 2, 'Jeep Fare', 30.00, '2024-11-02', 'Commute'),
(1, 1, 'Snacks', 45.00, '2024-11-03', 'Afternoon snack'),
(1, 4, 'Movie Ticket', 250.00, '2024-11-04', 'Weekend movie'),

(2, 1, 'Dinner', 150.00, '2024-11-01', 'Fast food'),
(2, 2, 'Bus Fare', 50.00, '2024-11-02', 'Daily commute'),
(2, 4, 'Online Game', 300.00, '2024-11-02', 'Entertainment'),
(2, 3, 'Electric Bill', 500.00, '2024-11-03', 'Monthly bill'),
(2, 4, 'Streaming Subscription', 199.00, '2024-11-04', 'Netflix'),

(3, 1, 'Breakfast', 70.00, '2024-11-01', 'Morning meal'),
(3, 2, 'Tricycle Fare', 40.00, '2024-11-02', 'Short trip'),
(3, 1, 'Lunch', 110.00, '2024-11-03', 'Canteen'),
(3, 4, 'Music Subscription', 149.00, '2024-11-04', 'Monthly plan'),

(4, 1, 'Snacks', 45.00, '2024-11-01', 'Afternoon snack'),
(4, 3, 'Water Bill', 300.00, '2024-11-03', 'Utilities'),
(4, 4, 'Movie Rental', 180.00, '2024-11-04', 'Entertainment'),

(5, 1, 'Lunch', 130.00, '2024-11-02', 'Canteen'),
(5, 2, 'Jeep Fare', 30.00, '2024-11-02', 'School commute'),
(5, 4, 'Mobile Game', 99.00, '2024-11-03', 'In-app purchase');
    