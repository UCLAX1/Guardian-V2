import mysql.connector
import datetime
import random

mydb = mysql.connector.connect(
        host="localhost",
        user="tate",
        passwd="pass123",
        database="x1_guardian"
        )

mycursor = mydb.cursor()

createTable = ("CREATE TABLE IF NOT EXISTS Position_Data "
              "(ID INT, Link_X INT, Link_Y INT, "
              "Laser_X INT, Laser_Y INT, "
              "Distance_Offset INT, Angle_Offset INT, "
              "Time VARCHAR(255))")

mycursor.execute(createTable)

random.seed()

i = 1
while True:
        sql = ("INSERT INTO Position_Data (ID, Link_X, Link_Y, Laser_X, "
               "Laser_Y, Distance_Offset, Angle_Offset, Time) VALUES(%s,%s,%s,%s, %s, %s,%s,%s)")
        link_x = str((int)(random.random()*100))
        link_y = str((int)(random.random()*100))
        laser_x = str((int)(random.random()*100))
        laser_y = str((int)(random.random()*100))
        distance = str((int)(random.random()*100))
        angle = str((int)(random.random()*100))
        raw_time = datetime.datetime.now()
        val = (i, link_x, link_y, laser_x, laser_y, distance, angle, str(raw_time))
        mycursor.execute(sql, val)
        i += 1
        mydb.commit()