
import sys

from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QTabWidget, \
    QVBoxLayout, QFormLayout, QLineEdit, QDateEdit, QCheckBox, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QDateTime
from RegEx import Validator
from db import DBCon


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'CRM & Email Marketing System'
        self.left = 0
        self.top = 0
        self.width = 500
        self.height = 400
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('crm.png'))
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        # self.setCentralWidget(self.table_widget)
        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Add Customer")
        self.tabs.addTab(self.tab2, "Advertisement")
        self.tabs.addTab(self.tab3, "Delete Previous Records")

        # Creating First tab
        self.tab1.layout = QFormLayout(self)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Type Customer Name")
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Type Customer E-mail Id")
        self.mobile_edit = QLineEdit()
        self.mobile_edit.setPlaceholderText("Type Customer Mobile Number")
        self.v_date = QDateEdit()
        self.v_date.setDateTime(QDateTime.currentDateTime())
        self.add_btn = QPushButton("Add Customer To System")
        self.del_year_btn = QPushButton("Delete Previous year Record")
        self.del_month_btn = QPushButton("Delete Previous month Record")
        self.del_all = QPushButton("Delete All Record")
        self.email_del_edit = QLineEdit()
        self.email_del_edit.setPlaceholderText("Type Customer E-mail Id to delete")
        self.tab1.layout.addRow("Enter Name : ", self.name_edit)
        self.tab1.layout.addRow("Enter E-mail Id : ", self.email_edit)
        self.tab1.layout.addRow("Enter Mobile Number : ", self.mobile_edit)
        self.tab1.layout.addRow("Select Visiting Date : ", self.v_date)
        self.tab1.layout.addWidget(self.add_btn)
        self.tab1.layout.addWidget(self.del_year_btn)
        self.tab1.layout.addWidget(self.del_month_btn)
        self.tab1.layout.addWidget(self.del_all)
        self.tab1.layout.addRow("Delete this email", self.email_del_edit)
        self.tab1.setLayout(self.tab1.layout)
        self.add_btn.clicked.connect(self.addtodb)
        self.del_year_btn.clicked.connect(self.delthis)
        self.del_month_btn.clicked.connect(self.delthis)
        self.del_all.clicked.connect(self.delthis)

        # Creating Second Tab
        self.layout.addWidget(self.tabs)
        self.tab2.layout = QFormLayout()
        self.all_chbox = QCheckBox("Send To All")
        self.send_btn = QPushButton("Send")
        self.tab2.layout.addWidget(self.all_chbox)
        self.tab2.layout.addWidget(self.send_btn)
        self.tab2.setLayout(self.tab2.layout)
        self.send_btn.clicked.connect(self.sendmail)

    def addtodb(self):
        print("in DB")
        if not Validator.checkemail(self.email_edit.text()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("Enter Valid Email Address")
            msg_box.setWindowIcon(QIcon('crm.png'))
            msg_box.setWindowTitle("Incorrect Email-id")
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = msg_box.exec_()
            return
        elif not Validator.checkmob(self.mobile_edit.text()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("Enter Valid Mobile Number")
            msg_box.setWindowIcon(QIcon('crm.png'))
            msg_box.setWindowTitle("Incorrect Mobile No.")
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = msg_box.exec_()
            return
        else:
            ch = DBCon.dbinitop(self)
            if ch == 1:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setText("Customer added to System successfully")
                msg_box.setWindowIcon(QIcon('crm.png'))
                msg_box.setWindowTitle("Added Customer")
                msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                retval = msg_box.exec_()
                self.name_edit.setText("")
                self.email_edit.setText("")
                self.mobile_edit.setText("")
            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("Problem With Database....Restart Database")
                msg_box.setWindowIcon(QIcon('crm.png'))
                msg_box.setWindowTitle("Restart Database")
                msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                retval = msg_box.exec_()


    def sendmail(self):
        if self.all_chbox.isChecked():
            print("mailing")
            DBCon.dbpickup()
        self.all_chbox.setChecked(False)

    def delprevyear(self, btn):
        DBCon.delfromdb(1)

    def delprevmonth(self, btn):
        DBCon.delfromdb(2)

    def delall(self, btn):
        DBCon.delfromdb(4)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(),
                  currentQTableWidgetItem.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
