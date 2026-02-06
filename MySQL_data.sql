-- Create Database
CREATE DATABASE hotel_reservation_system;
USE hotel_reservation_system; 

-- 1. Users Table
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    role ENUM('ADMIN', 'STAFF', 'CUSTOMER') DEFAULT 'CUSTOMER',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Customers Table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    postal_code VARCHAR(10),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 3. Room Types Table
CREATE TABLE room_types (
    room_type_id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(50) NOT NULL,
    description TEXT,
    base_price DECIMAL(10, 2) NOT NULL,
    max_occupancy INT NOT NULL,
    amenities TEXT
);

-- 4. Rooms Table
CREATE TABLE rooms (
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    room_number VARCHAR(10) UNIQUE NOT NULL,
    room_type_id INT NOT NULL,
    floor_number INT,
    status ENUM('AVAILABLE', 'OCCUPIED', 'MAINTENANCE', 'RESERVED') DEFAULT 'AVAILABLE',
    FOREIGN KEY (room_type_id) REFERENCES room_types(room_type_id) ON DELETE RESTRICT
);

-- 5. Reservations Table
CREATE TABLE reservations (
    reservation_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    room_id INT NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    number_of_guests INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('PENDING', 'CONFIRMED', 'CANCELLED', 'COMPLETED') DEFAULT 'PENDING',
    special_requests TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE RESTRICT,
    CHECK (check_out_date > check_in_date)
);

-- 6. Payments Table
CREATE TABLE payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    reservation_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_method ENUM('CASH', 'CREDIT_CARD', 'DEBIT_CARD', 'UPI', 'NET_BANKING') NOT NULL,
    payment_status ENUM('PENDING', 'COMPLETED', 'FAILED', 'REFUNDED') DEFAULT 'PENDING',
    transaction_id VARCHAR(100),
    FOREIGN KEY (reservation_id) REFERENCES reservations(reservation_id) ON DELETE CASCADE
);

-- 7. Reviews Table
CREATE TABLE reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    room_type_id INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (room_type_id) REFERENCES room_types(room_type_id) ON DELETE CASCADE
);

-- 8. Staff Table
CREATE TABLE staff (
    staff_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position VARCHAR(50),
    salary DECIMAL(10, 2),
    hire_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Indexes for better performance
CREATE INDEX idx_reservation_dates ON reservations(check_in_date, check_out_date);
CREATE INDEX idx_room_status ON rooms(status);
CREATE INDEX idx_customer_email ON users(email);
CREATE INDEX idx_reservation_status ON reservations(status);

-- Sample Data Insertion
INSERT INTO room_types (type_name, description, base_price, max_occupancy, amenities) VALUES
('Standard', 'Comfortable room with basic amenities', 1500.00, 2, 'AC, TV, WiFi'),
('Deluxe', 'Spacious room with premium amenities', 2500.00, 3, 'AC, TV, WiFi, Mini Bar'),
('Suite', 'Luxury suite with living area', 4500.00, 4, 'AC, TV, WiFi, Mini Bar, Jacuzzi');

INSERT INTO rooms (room_number, room_type_id, floor_number, status) VALUES
('101', 1, 1, 'AVAILABLE'),
('102', 1, 1, 'AVAILABLE'),
('201', 2, 2, 'AVAILABLE'),
('202', 2, 2, 'AVAILABLE'),
('301', 3, 3, 'AVAILABLE');
