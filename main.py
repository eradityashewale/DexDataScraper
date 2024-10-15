from dbconnection import DBConnection

conn = DBConnection.get_connection()
# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM follows")

# Retrieve query results
records = cur.fetchall()
print(records)





