# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '365d.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import psycopg2
from psycopg2 import sql

class Ui_MainWindowTd(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1800, 900)
        MainWindow.setStyleSheet("background-color: rgb(52, 52, 52);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 1800, 900))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../Downloads/365d sub.jpg"))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(1010, 300, 721, 71))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color: rgb(231, 231, 231);\n"
"border-radius: 20px;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(1430, 450, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color: rgb(231, 231, 231);\n"
"border-radius: 20px;")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(1010, 450, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setStyleSheet("background-color: rgb(231, 231, 231);\n"
"border-radius: 20px;")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(1010, 590, 721, 71))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setStyleSheet("background-color: rgb(231, 231, 231);\n"
"border-radius: 20px;")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(740, 760, 341, 81))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(4, 255, 0);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.subscribe)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "CONTINUE"))

    def subscribe(self):
        # Get user input
        card_number= self.lineEdit.text()
        expiry_date= self.lineEdit_3.text()
        cvv = self.lineEdit_2.text()
        name = self.lineEdit_4.text()

        # Check if the name is already registered
        if self.is_name_registered(name):
            QtWidgets.QMessageBox.warning(
                None, "Registration Failed", "This name is already registered."
            )
            return

        # Insert data into the database
        if self.insert_subscription(card_number, expiry_date, cvv, name):
            QtWidgets.QMessageBox.information(
                None, "Subscription Successful", "Your subscription was successful."
            )
        else:
            QtWidgets.QMessageBox.critical(
                None, "Error", "Failed to register your subscription. Please try again."
            )

    def is_name_registered(self, name):
        # Establish a database connection
        connection = psycopg2.connect(
            host="localhost",
            database="dvdrental",
            user="postgres",
            password="12345",
        )
        cursor = connection.cursor()

        # Check if the name exists in the database
        query = sql.SQL("SELECT COUNT(*) FROM subs WHERE name = %s")
        cursor.execute(query, (name,))
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return count > 0

    def insert_subscription(self, card_number, expiry_date, cvv, name):
        # Establish a database connection
        connection = psycopg2.connect(
            host="localhost",
            database="dvdrental",
            user="postgres",
            password="12345",
        )
        cursor = connection.cursor()

        # Insert subscription data into the database
        query = sql.SQL("INSERT INTO subs (card_num, MM_YY, CVV, name) VALUES (%s, %s, %s, %s)")
        try:
            cursor.execute(query, (card_number, expiry_date, cvv, name))
            connection.commit()
        except psycopg2.Error as e:
            print(f"Error inserting data: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()

        return True

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindowTd()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
