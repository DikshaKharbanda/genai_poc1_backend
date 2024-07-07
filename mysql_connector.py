import mysql.connector
from mysql.connector import Error

try:
    # Establish the connection
    connection = mysql.connector.connect(
        host='localhost',  # e.g., 'localhost'
        database='EKYC',   # Your database name
        user='root',  # Your MySQL username
        password='kharbanda'  
    )

    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_info)
        cursor = connection.cursor()
        
        # Create the users table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            NAME VARCHAR(100),
            EMAIL VARCHAR(100),
            FATHER'S NAME VARCHAR(100),
            User_ID VARCHAR(100) PRIMARY KEY,
            STATUS VARCHAR(50),
            AADHAR_NO VARCHAR(12),
            PAN_NO VARCHAR(10),
            ADDRESS VARCHAR(20),
            GENDER VARCHAR(10),
            DOB DATE,
            PASSWORD VARCHAR(255)
        );
        """
        cursor.execute(create_table_query)
        print("Table users created or already exists.")
        
        # Insert data into the users table
        insert_query = """
        INSERT INTO users (NAME, User_ID, STATUS, AADHAR_NO, PAN_NO, ADDRESS, GENDER, DOB, PASSWORD) VALUES
        ('Vrinda Bhatt', '1234@56', '0', NULL, NULL, NULL, NULL, NULL, NULL),
        ('Vridhi Talwar', '2436@ee', '1', '456454782649', 'ABCD13254D', 'DELHI', 'F', '1988-03-12', NULL),
        ('Aditi Sharma', '164xts', '0', NULL, NULL, NULL, NULL, NULL, NULL),
        ('Disha Bajaj', '12453', '1', '1236586364582', 'ACFD1234DF', 'MUMBAI', 'F', '2002-09-14', NULL),
        ('Amaira Singh', '123@ams', '0', NULL, NULL, NULL, NULL, NULL, NULL),
        ('Aditya Singh', '2t34@123', '1', '127654890735', 'ADGF128754', 'GOA', 'M', '2001-09-13', NULL),
        ('Agrim Jain', '1287535', '0', NULL, NULL, NULL, NULL, NULL, NULL),
        ('Aashi Kapoor', '45829', '0', NULL, NULL, NULL, NULL, NULL, NULL),
        ('Nandini Jain', '1256973', '0', '357488785791', NULL, 'KERELA', 'F', '2000-11-13', NULL),
        ('Nimisha Jain', '123@nimi', '0', NULL, 'ASDF1234GH', NULL, NULL, NULL, NULL),
        ('Jashit Goel', '2342@jas', '1', '123456783435', 'ASTY12463D', 'DELHI', 'M', '2000-12-12', NULL),
        ('Diksha Sharma', '12233@ds', '0', NULL, 'ASED23435F', NULL, NULL, NULL, NULL);
        """
        cursor.execute(insert_query)
        connection.commit()
        print("Records inserted successfully into users table")

except Error as e:
    print("Failed to insert record into MySQL table", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
