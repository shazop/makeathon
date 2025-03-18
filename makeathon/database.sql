CREATE DATABASE makeathon;
USE makeathon;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    role ENUM('admin', 'student') NOT NULL
);

CREATE TABLE issues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_username VARCHAR(50) NOT NULL,
    category VARCHAR(100) NOT NULL,
    priority ENUM('Critical', 'High', 'Medium', 'Low') NOT NULL,
    status ENUM('Open', 'Forwarded', 'Closed') DEFAULT 'Open'
);
