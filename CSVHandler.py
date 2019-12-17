import csv

import mysql
from mysql.connector import Error


class handler:
    def dbtocsv(obj):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="crm"
            )
            mycursor = mydb.cursor()
            mycursor.execute("select * from customer_master")
            result = mycursor.fetchall()

            c = csv.writer(open('dbdumptocsv.csv', 'w'))
            for x in result:
                c.writerow(x)
            return 1
        except Error as e:
            print("There is a problem with MySQL", e)
            return 0
        finally:
            mycursor.close()
            mydb.close()
            print("Imported to CSV Properly...")
