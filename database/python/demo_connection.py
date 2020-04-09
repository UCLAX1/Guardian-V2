import mysql.connector
import datetime
import random

"""
mydb = mysql.connector.connect(
        host="localhost",
        user="tate",
        passwd="pass123",
        )
"""
mydb = mysql.connector.connect(
        host="localhost",
        user="tate",
        passwd="pass123",
        database="x1_guardian"
        )

mycursor = mydb.cursor()

# this line was used to create a database
"""
mycursor.execute("CREATE DATABASE x1_guardian")
"""

# this block was to list all databases
"""
mycursor.execute("SHOW DATABASES")
for x in mycursor:
       print(x)
"""

# create a table
"""
mycursor.execute("CREATE TABLE test0 (first VARCHAR(255), second VARCHAR(255))")
"""

# list all tables
"""
mycursor.execute("SHOW TABLES")
for x in mycursor:
        print(x)
"""

# put thing into table
"""
sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = ("John", "Highway 21")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted")
"""

createTable = ("CREATE TABLE IF NOT EXISTS Position_Data "
              "(id INT, Link_x VARCHAR(255), Link_y VARCHAR(255), "
              "Laser_x VARCHAR(255), Laser_y VARCHAR(255), "
              "Time VARCHAR(255))")

mycursor.execute(createTable)

random.seed()

i = 0
while True:
        sql = ("INSERT INTO Position_Data (id, Link_x, Link_y, Laser_x, "
               "Laser_y, Time) VALUES(%s,%s,%s,%s,%s,%s)")
        link_x = str(random.random())
        link_y = str(random.random())
        laser_x = str(random.random())
        laser_y = str(random.random())
        raw_time = datetime.datetime.now()
        val = (i, link_x, link_y, laser_x, laser_y, str(raw_time))
        mycursor.execute(sql, val)
        i += 1
        mydb.commit()


# get stuff from databases

# get all
# mycursor.execute("SELECT * FROM customers")

# get specified columns
# mycursor.execute("SELECT name, address FROM customers")

# get all rows
# myresult = mycursor.fetchall()

# get one row
"""
myresult = mycursor.fetchone()
for x in myresult:
        print(x)
"""
