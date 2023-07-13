import psycopg2

# Database connection details
db_host = "localhost"
db_user = "cars_999"
db_password = "password"
db_name = "999"
db_port = 5432

# Table name in the database
table = "apartamente"

# Connect to the database
db = psycopg2.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
    port=db_port
)

# Create a cursor to execute SQL commands
cursor = db.cursor()

# Execute SQL command to create the table (if it doesn't exist)
cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (url VARCHAR(255), name VARCHAR(255), price VARCHAR(255), currency VARCHAR(255), surface VARCHAR(255), Phone VARCHAR(255))")


def execute_query(query, values=None):
    """
    Execute a SQL query and return the results
    """
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)

def fetch_one():
    """
    Fetch the first result from the last executed query
    """
    return cursor.fetchone()

def commit():
    """
    Commit the changes to the database
    """
    db.commit()

def close():
    """
    Close the database connection
    """
    db.close()
