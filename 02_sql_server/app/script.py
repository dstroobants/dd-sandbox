import pyodbc
import time

# Connect to the SQL Server
SERVER = 'sqlserver'
DATABASE = 'sample_db'
USERNAME = 'sample_user'
PASSWORD = 'S4mple_p4ssword'

CONNECTIONSTRING = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={SERVER};'
    f'DATABASE={DATABASE};'
    f'UID={USERNAME};'
    f'PWD={PASSWORD};'
    f'TrustServerCertificate=yes;'
)

def test_db_connection():
    try:
        conn = pyodbc.connect(CONNECTIONSTRING)
        conn.close()
        print("Connection to the database was successful.")
        return True
    except Exception as e:
        print(f'Error occurred while connecting to DB: {e}')
        return False

def fetch_and_print_orders():
    try:
        conn = pyodbc.connect(CONNECTIONSTRING)
        cursor = conn.cursor()

        # Execute a query to select all orders
        cursor.execute('SELECT * FROM orders')

        # Fetch all rows from the query result
        rows = cursor.fetchall()

        # Print each row
        for row in rows:
            print(row)

        # Close the cursor and connection
        cursor.close()
        conn.close()
    except Exception as e:
        print(f'Error occurred while fetching orders: {e}')

def insert_new_order(index):
    try:
        conn = pyodbc.connect(CONNECTIONSTRING)
        cursor = conn.cursor()

        # Execute a query to insert a new row
        cursor.execute(
            "INSERT INTO orders (order_id, order_date, order_amount, customer_name) VALUES (?, ?, ?, ?)", (index, '2023-02-01', 100.00, 'John Doe')
        )

        # Commit the changes
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()
    except Exception as e:
        print(f'Error occurred while inserting a new order: {e}')

def delete_oldest_order():
    try:
        conn = pyodbc.connect(CONNECTIONSTRING)
        cursor = conn.cursor()

        # Execute a query to delete the oldest row
        cursor.execute("DELETE FROM orders WHERE order_id = (SELECT MIN(order_id) FROM orders)")

        # Commit the changes
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()
    except Exception as e:
        print(f'Error occurred while deleting the oldest order: {e}')

if __name__ == "__main__":
    index = 4
    while True:
        if test_db_connection():
            fetch_and_print_orders()
            insert_new_order(index)
            #delete_oldest_order()
            index+=1
        # Wait for 30 seconds before the next iteration
        time.sleep(30)
