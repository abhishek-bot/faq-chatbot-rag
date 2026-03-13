import sqlite3  # Built-in with Python but included here for clarity; SQLite is a C library that provides a lightweight disk-based database that doesn’t require a separate server process and allows access to the database using a nonstandard variant of the SQL query language.
import os  # Built-in with Python; provides a way of using operating system dependent functionality, such as file path manipulation.

DB_PATH = "data/faq.db" # Path to the SQLite database file

def seed_database():

    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor object to interact with the database

    # Create the FAQ table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faq (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS unanswered_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')  # Create a table for unanswered queries to log any questions that the system couldn't answer, which can be useful for improving the FAQ database over time.

    # Sample FAQ data to insert into the database
    faqs = [
        # Refunds & Payments
        ("What is refund policy?", "We offer a 30-day refund policy for unused services."),
        ("Can I get a refund if I cancel?", "Refunds are available within 30 days of purchase if the service is unused."),
        ("Do you charge late fees?", "No, we do not charge late fees."),

        # Accounts & Security
        ("How do I reset my password?", "You can reset your password by clicking 'Forgot Password' on the login page."),
        ("Can I change my email address?", "Yes, you can update your email address in the account settings page."),
        ("Is two-factor authentication available?", "Yes, we support two-factor authentication for added security."),

        # Support & Services
        ("Do you offer customer support?", "Yes, we provide 24/7 customer support via email and chat."),
        ("How quickly will support respond?", "Our support team typically responds within 2 hours."),
        ("Do you offer live chat?", "Yes, live chat is available on our website during business hours."),

        # General Policies
        ("Where are you located?", "Our headquarters are in New York City."),
        ("Do you ship internationally?", "Yes, we ship to most countries worldwide."),
        ("What are your business hours?", "We are open Monday to Friday, 9 AM to 6 PM EST.")
    ]


    cursor.executemany('INSERT INTO faq (question, answer) VALUES (?, ?)', faqs)
    print("Sample FAQ data inserted.")

    conn.commit()  # Commit the changes to the database
    conn.close()  # Close the database connection

if __name__ == "__main__":
    seed_database()  # Run the function to seed the database with sample data
