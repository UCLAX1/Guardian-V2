import datetime
import mysql.connector



def create_db():

    create_db_query = (
        "CREATE TABLE IF NOT EXISTS Guardian_Data "
        "(ID INT NOT NULL AUTO_INCREMENT, "
        "Link_X INT NOT NULL, Link_Y INT NOT NULL, "
        "Laser_X INT NOT NULL, Laser_Y INT NOT NULL, "
        "Distance_Offset DECIMAL(8,2) NOT NULL, Angle_Offset DECIMAL(8,2) NOT NULL, "
        "Time VARCHAR(255) NOT NULL, "
        "PRIMARY KEY (ID))"
    )

    my_db = mysql.connector.connect(
        host="localhost",
        user="x1",
        passwd="asme",
        database="x1_guardian"
    )
    my_cursor = my_db.cursor()

    my_cursor.execute(create_db_query)



def insert_data(laser_coords, link_coords, link_pos):

    laser_x, laser_y = laser_coords
    link_x, link_y = link_coords
    distance_offset, angle_offset = link_pos
    timestamp = datetime.datetime.now()

    data = (link_x, link_y, laser_x, laser_y, distance_offset, angle_offset, str(timestamp))
    insert_query = (
        "INSERT INTO Guardian_Data "
        "(Link_X, Link_Y, "
        "Laser_X, Laser_Y, "
        "Distance_Offset, Angle_Offset, "
        "Time) "
        "VALUES(%s,%s,%s,%s,%s,%s,%s)"
    )

    my_db = mysql.connector.connect(
        host="localhost",
        user="x1",
        passwd="asme",
        database="x1_guardian"
    )
    my_cursor = my_db.cursor()

    my_cursor.execute(insert_query, data)
    my_db.commit()



def retrieve_specific_data():

    retrieve_query = "SELECT * FROM Guardian_Data ORDER BY ID DESC LIMIT 5"

    my_db = mysql.connector.connect(
        host="localhost",
        user="x1",
        passwd="asme",
        database="x1_guardian"
    )
    my_cursor = my_db.cursor()

    my_cursor.execute(retrieve_query)
    my_result = my_cursor.fetchall()

    for i in range(len(my_result)):
        my_result[i] = ",".join(map(str,my_result[i]))
    my_result = "\n".join(my_result)

    return my_result



def retrieve_all_data():

    retrieve_query = "SELECT * FROM Guardian_Data"

    my_db = mysql.connector.connect(
        host="localhost",
        user="x1",
        passwd="asme",
        database="x1_guardian"
    )
    my_cursor = my_db.cursor()

    my_cursor.execute(retrieve_query)
    my_result = my_cursor.fetchall()

    for i in range(len(my_result)):
        my_result[i] = ",".join(map(str,my_result[i]))
    my_result = "\n".join(my_result)

    return my_result



def truncate_table():

    truncate_query = "TRUNCATE TABLE Guardian_Data"

    my_db = mysql.connector.connect(
        host="localhost",
        user="x1",
        passwd="asme",
        database="x1_guardian"
    )
    my_cursor = my_db.cursor()

    my_cursor.execute(truncate_query)
