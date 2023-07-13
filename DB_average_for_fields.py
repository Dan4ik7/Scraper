import psycopg2

host = "localhost"
user = "cars_999"
password = "password"
db = "999_cars"
port_id = 5432

class Database:
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def connect(self):
        self.connection = psycopg2.connect(host=self.host,
                                          user=self.user,
                                          password=self.password,
                                          db=self.db,
                                          port_id=self.port_id,
                                          cursorclass=psycopg2.cursors.DictCursor)

    def disconnect(self):
        self.connection.close()

    def get_field_average(self, table, field):
        self.connect()
        cursor = self.connection.cursor()

        query = "SELECT {} FROM {}".format(field, table)
        cursor.execute(query)

        values = []
        for row in cursor.fetchall():
            value = int(row[field])
            values.append(value)

        average = sum(values) / len(values)

        self.disconnect()

        return average


db = Database(host,user,password,db)
average = db.get_field_average(table="megane_4_17_martie", field="price")
print("The average of values in 'price' is: {}".format(average))

