import pymysql


class Database:
    def __init__(self, host, username, password, db):
        self.connection = pymysql.connect(
            host=host,
            user=username,
            password=password,
            db=db,
            cursorclass=pymysql.cursors.DictCursor
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def get_urls(self, table_name):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT url FROM {table_name}")
            results = cursor.fetchall()
            return [result["url"] for result in results]


if __name__ == "__main__":
    # Define database connection parameters
    host = "localhost"
    username = "999_cars"
    password = "password"
    db = "999_cars"

    # Create Database instances for old and new tables
    with Database(host, username, password, db) as old_db, \
            Database(host, username, password, db) as new_db:
        # Get lists of old and new URLs from their respective tables
        old_urls = old_db.get_urls("megane_17_martie")
        new_urls = new_db.get_urls("megane_18_martie")

        # Find new URLs that are not in the old list
        new_urls_list = list(set(new_urls) - set(old_urls))

        # Find old URLs that are not in the new list
        old_urls_list = list(set(old_urls) - set(new_urls))

        # Print the results

        print("Sold Cars: ")
        for i in old_urls_list:
            print(i)

        print("New Cars: ")
        for i in new_urls_list:
            print(i)