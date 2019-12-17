from datetime import datetime

import mysql
from mysql.connector import Error
from numpy import unicode
from mail import Mailer

class DBCon:
    def dbinitop(obj):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="crm"
            )
            mycursor = mydb.cursor(buffered=True)
            print("connected")
            myd = datetime.strptime(obj.dateEdit.text(), '%m/%d/%Y').date()
            query = "select name from customer_master where email_id = %s"
            val = (obj.lineEdit_3.text(),)
            mycursor.execute(query, val)
            # print(mycursor.rowcount)
            if mycursor.rowcount > 0:
                query = "update customer_master set visiting_date = %s where email_id = %s"
                val = (unicode(myd).__str__(), obj.line_Edit3.text(),)
                mycursor.execute(query, val)
                mydb.commit()
            else:
                query = "insert into customer_master values(%s, %s, %s, %s);"
                val = (obj.lineEdit_2.text(), obj.lineEdit_3.text(), obj.lineEdit_4.text(), unicode(myd).__str__())
                # querytemp = "insert into customer_master values('" + self.name_edit.text() + "', '" + self.email_edit.text() + "', '" + self.mobile_edit.text() + "', STR_TO_DATE(\"" + unicode(myd) + "\", \"%Y-%m-%d\"));"
                mycursor.execute(query, val)
                mydb.commit()
            return 1
        except Error as e:
            print("There is a problem with MySQL", e)
            return 0
        finally:
            mycursor.close()
            mydb.close()
            print("Inserted Properly...")

    def dbpickup(choice, obj):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="crm"
            )
            mycursor = mydb.cursor(buffered=True)
            if choice == 1:
                mycursor.execute("select email_id from customer_master")
                result = mycursor.fetchall()
                for x in result:
                    Mailer.send(x[0])
                    print("Mailed to " + str(x[0]))
            elif choice == 2:
                myd = datetime.strptime(obj.dateEdit_2.text(), '%m/%d/%Y').date()
                myd2 = datetime.strptime(obj.dateEdit_3.text(), '%m/%d/%Y').date()
                mycursor.execute("select email_id from customer_master where visiting_date >= %s AND visiting_date <= "
                                 "%s", (unicode(myd).__str__(), unicode(myd2).__str__(),))
                result = mycursor.fetchall()
                for x in result:
                    Mailer.send(x[0])
                    print("Mailed to " + str(x[0]))
            return 1
        except Error as e:
            print("There is a problem with MySQL", e)
            return 0
        finally:
            mycursor.close()
            mydb.close()
            print("Advertised Successfully...")

    def delfromdb(choice, obj):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="crm"
            )
            mycursor = mydb.cursor(buffered=True)
            if choice == 1:
                mycursor.execute("delete from customer_master where visiting_date < DATE_SUB(CURDATE(), INTERVAL 1 YEAR)")
            elif choice == 2:
                mycursor.execute("delete from customer_master where visiting_date <= DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND visiting_date >= DATE_SUB(CURDATE(), INTERVAL 2 MONTH)")
            elif choice == 3:
                mycursor.execute("select name from customer_master where email_id = %s", (obj.lineEdit_5.text(),))
                if mycursor.rowcount > 0:
                    mycursor.execute("delete from customer_master where email_id = %s", (obj.lineEdit_5.text(),))
                else:
                    return 2
            elif choice == 4:
                mycursor.execute("delete from customer_master")
            mydb.commit()
            return 1
        except Error as e:
            print("There is a problem with MySQL", e)
            return 0
        finally:
            mycursor.close()
            mydb.close()
            print("Deleted Successfully...")

    def selectfromdb(choice, obj):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="crm"
            )
            mycursor = mydb.cursor()
            data = "Name\t\tE-mail Address\t\t\tMobile Number\tVisiting Date\t"
            if choice == 1:
                mycursor.execute("select * from customer_master")
                result = mycursor.fetchall()
                for x in result:
                    data += "\n" + str(x[0]) + "\t\t" + str(x[1]) + "\t" + str(x[2]) + "\t\t" + str(x[3])
            elif choice == 2:
                mycursor.execute("select * from customer_master where visiting_date > %s AND visiting_date < %s", ("d1", "d2", ))
                result = mycursor.fetchall()
                for x in result:
                    data += "\n" + str(x[0]) + "\t\t" + str(x[1]) + "\t\t" + str(x[2]) + "\t\t" + str(x[3])
            elif choice == 3:
                mycursor.execute("select * from customer_master where email_id = %s", (obj.lineEdit_6.text(), ))
                result = mycursor.fetchall()
                for x in result:
                    data += "\n" + str(x[0]) + "\t\t" + str(x[1]) + "\t\t" + str(x[2]) + "\t\t" + str(x[3])
            return data
        except Error as e:
            print("There is a problem with MySQL", e)
            return "failed"
        finally:
            data = ""
            mycursor.close()
            mydb.close()
            print("Shown Successfully...")
