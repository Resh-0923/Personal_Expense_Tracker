-- USERS
INSERT INTO user (username, password) VALUES
('demo_user', 'hashed_pw1'),
('student01', 'hashed_pw2'),
('student02', 'hashed_pw3'),
('student03', 'hashed_pw4'),
('student04', 'hashed_pw5');

-- EXPENSES
INSERT INTO expense (user_id, name, amount, date, category, notes) VALUES
(1, 'Lunch', 120.00, '2024-11-01', 'Food', 'Cafeteria'),
(1, 'Coffee', 95.00, '2024-11-02', 'Food', 'Study break'),
(1, 'Jeep Fare', 30.00, '2024-11-02', 'Transportation', 'Commute'),
(1, 'Snacks', 45.00, '2024-11-03', 'Food', 'Afternoon snack'),
(1, 'Movie Ticket', 250.00, '2024-11-04', 'Entertainment', 'Weekend movie'),

(2, 'Dinner', 150.00, '2024-11-01', 'Food', 'Fast food'),
(2, 'Bus Fare', 50.00, '2024-11-02', 'Transportation', 'Daily commute'),
(2, 'Online Game', 300.00, '2024-11-02', 'Entertainment', 'Gaming'),
(2, 'Electric Bill', 500.00, '2024-11-03', 'Utilities', 'Monthly bill'),
(2, 'Streaming Subscription', 199.00, '2024-11-04', 'Entertainment', 'Netflix'),

(3, 'Breakfast', 70.00, '2024-11-01', 'Food', 'Morning meal'),
(3, 'Tricycle Fare', 40.00, '2024-11-02', 'Transportation', 'Short trip'),
(3, 'Lunch', 110.00, '2024-11-03', 'Food', 'Canteen'),
(3, 'Music Subscription', 149.00, '2024-11-04', 'Entertainment', 'Monthly plan'),

(4, 'Snacks', 45.00, '2024-11-01', 'Food', 'Afternoon snack'),
(4, 'Water Bill', 300.00, '2024-11-03', 'Utilities', 'Utilities'),
(4, 'Movie Rental', 180.00, '2024-11-04', 'Entertainment', 'Movie night'),

(5, 'Lunch', 130.00, '2024-11-02', 'Food', 'Canteen'),
(5, 'Jeep Fare', 30.00, '2024-11-02', 'Transportation', 'School commute'),
(5, 'Mobile Game', 99.00, '2024-11-03', 'Entertainment', 'In-app purchase');
