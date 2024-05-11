import sqlite3

# Connect to the practice.db database:
database = sqlite3.connect('practice.db')
cursor = database.cursor()

# Create the 'students' table if not already there:
sql_query = "CREATE TABLE IF NOT EXISTS students (last_name TEXT, first_name TEXT, grad_year INT)"
cursor.execute(sql_query)

# Collect values for the 3 table columns:
last_name = input("Enter your last name: ").capitalize()
first_name = input("Enter your first name: ").capitalize()
grad_year = int(input("Enter your graduation year: "))

# Add a new row to the 'students' table, them commit.
sql_query = "INSERT INTO students (last_name, first_name, grad_year) VALUES (?, ?, ?)"
cursor.execute(sql_query, (last_name, first_name, grad_year))
database.commit()


cursor.execute('SELECT last_name, first_name, grad_year FROM students')
for row in cursor:
    print(row)
    
cursor.close()