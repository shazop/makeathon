import mysql.connector

# ✅ Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "makeathon",
}

# ✅ Function to Get Database Connection
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ✅ Function to Initialize the Database
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ Create Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('admin', 'student', 'incharge') NOT NULL
        )
    """)

    # ✅ Create Reports Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(255) NOT NULL,
            subcategory VARCHAR(255) NOT NULL,
            priority ENUM('Critical', 'High', 'Medium', 'Low') NOT NULL,
            description TEXT NOT NULL,
            status ENUM('Pending', 'In Progress', 'Resolved') DEFAULT 'Pending',
            image LONGBLOB,
            video LONGBLOB,
            student_username VARCHAR(255) NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# ✅ Function to Authenticate User
def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()
    return user
