import sqlite3

conn = sqlite3.connect("data/faq.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM faq")
rows = cursor.fetchall()

print(rows)   # Should print all FAQs
conn.close()