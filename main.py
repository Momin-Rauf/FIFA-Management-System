# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: Jazib, Momin Rauf, Ahsan Ullah
This is a temporary script file.
"""

import sys
from PyQt5 import QtWidgets, QtCore, uic
import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pathlib import Path
import os
from datetime import datetime


# connecting the database along with the user
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jazib@123",
    database="Football_WorldCup_Management"
)
mycursor = mydb.cursor()

# finding path for the UI folder where all the UI files are present
path = os.path.dirname(__file__)
path = '//'.join(path.split("\\"))
absolutePath = path + "//UI//"

# Class for the Main Window which is opened at first (Login Window)


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(absolutePath + "mainwindowLogin.ui", self)
        self.HandleButtonsLogin()
        self.HandleUIChangesLogin()

    def HandleButtonsLogin(self):
        self.pushButton_4.clicked.connect(self.click_Login_Button)
        self.pushButton_3.clicked.connect(self.open_signUp_Widget)
        self.pushButton.clicked.connect(self.click_exit_button)

    def HandleUIChangesLogin(self):
        self.setWindowTitle('Login')

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint |
                            QtCore.Qt.WindowMinimizeButtonHint)
        self.lineEdit.setFont(QFont('Arial', 12))
        self.lineEdit_2.setFont(QFont('Arial', 12))

    def click_exit_button(self):
        self.close()

    def verifyUserAccount(self):
        global email
        global cnic
        email = self.lineEdit.text()
        password = self.lineEdit_2.text()

        accList = []
        check = False
        try:
            # USING STORED PROCEDURE
            mycursor.callproc("loginproc")
            for result in mycursor.stored_results():
                accList = result.fetchall()
            # query = "SELECT * FROM football_fan"
            # mycursor.execute(query)
            # accList = mycursor.fetchall()

        except:
            print("Error!")

        for acc in accList:
            if (email == acc[4] and password == acc[5]):
                global userType
                userType = acc[7]
                check = True

        return check

    def getCNIC(self):
        emailAddress = [email]
        try:
            mycursor.callproc("userDetailsproc", emailAddress)
            for result in mycursor.stored_results():
                details = result.fetchall()

        except:
            print("Error")

        cnic = details[0][0]
        return cnic

    def click_Login_Button(self):
        if (self.verifyUserAccount()):
            if (userType == 'Customer'):
                self.new = FanDashboard(self)
                self.new.show()
                self.close()
            elif (userType == 'Ticket_Mgr'):
                self.new = TicketManager(self)
                self.new.show()
                self.close()
            elif (userType == 'Accommodation_Mgr'):
                self.new = HotelsManager(self)
                self.new.show()
                self.close()
            elif (userType == 'Flight_Mgr'):
                self.new = FlightManager(self)
                self.new.show()
                self.close()

            elif (userType == 'Team_Data_Mgr'):
                self.new = TeamDataManager(self)
                self.new.show()
                self.close()
            elif (userType == 'Fifa_Store_Mgr'):
                self.new = FifaStoreManager(self)
                self.new.show()
                self.close()

        else:
            QMessageBox.about(
                self, "Error", "Wrong Credentials, Try Logging In")

    def open_signUp_Widget(self):
        self.new = SignUpWidget(self)
        self.new.show()
        self.close()


# Class for the SignUp widget where user can register
class SignUpWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "signUp.ui", self)
        self.HandleButtonsSignUp()
        self.HandleUIChangesSignUp()

    def HandleButtonsSignUp(self):
        self.pushButton_4.clicked.connect(self.on_signUpButton)
        self.pushButton_5.clicked.connect(self.open_login_Widget)

    def HandleUIChangesSignUp(self):
        self.setWindowTitle('Sign Up')

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint |
                            QtCore.Qt.WindowMinimizeButtonHint)
        self.lineEdit.setFont(QFont('Arial', 10))
        self.lineEdit_2.setFont(QFont('Arial', 10))
        self.lineEdit_3.setFont(QFont('Arial', 10))
        self.lineEdit_4.setFont(QFont('Arial', 10))
        self.lineEdit_5.setFont(QFont('Arial', 10))

    def open_login_Widget(self):
        self.new = LoginWindow()
        self.new.show()
        self.close()

    def on_signUpButton(self):
        global cnic
        email = self.lineEdit.text()
        first_name = self.lineEdit_2.text()
        last_name = self.lineEdit_3.text()
        password = self.lineEdit_4.text()
        cnic = self.lineEdit_5.text()
        gender = self.comboBox.currentText()
        age = self.spinBox.value()
        userType = 'Customer'

        try:
            mycursor.execute('''INSERT INTO football_fan (CNIC, First_Name, Last_Name, Age, Email_Address, password, Gender, userType)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)''', (cnic, first_name, last_name,
                                                        age, email, password, gender, userType))
            mydb.commit()
            QMessageBox.about(self, "Done", "Account Successfully Created")
        except:
            QMessageBox.about(
                self, "Error", "Account Already Exists, Try Loggin In")


# Class for Fan Dashboard UI Interface
class FanDashboard(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "Dashboard.ui", self)
        self.HandleButtonsDashboard()
        self.HandleUIChangesDashboard()

    def HandleButtonsDashboard(self):
        self.pushButton_4.clicked.connect(self.open_userDetails_widget)
        self.pushButton_5.clicked.connect(self.click_Flight_Apply)
        self.pushButton_10.clicked.connect(self.click_Accommodation_Apply)
        self.pushButton_6.clicked.connect(self.click_Fifa_Store)
        self.pushButton_11.clicked.connect(self.click_Logout_button)

    def HandleUIChangesDashboard(self):
        self.setWindowTitle('Fan Dashboard')

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint |
                            QtCore.Qt.WindowMinimizeButtonHint)

    def open_payment(self):
        self.new = Payment(self)
        self.new.show()
        self.close()

    def click_Logout_button(self):
        self.new = LoginWindow()
        self.new.show()
        self.close()

    def click_Ticket_Apply(self):
        self.new = FifaTickets(self)
        self.new.show()
        self.close()

    def click_Accommodation_Apply(self):
        self.new = AccommodationApply(self)
        self.new.show()
        self.close()

    def open_userDetails_widget(self):
        self.new = UserDetails(self)
        self.new.show()
        self.close()

    def open_Match_Schedules(self):
        self.new = MatchSchedules(self)
        self.new.show()
        self.close()

    def click_Flight_Apply(self):
        self.new = FlightsApply(self)
        self.new.show()
        self.close()

    def click_Fifa_Store(self):
        self.new = FifaStore(self)
        self.new.show()
        self.close()


# Class for the Accommodaion UI Interface


class AccommodationApply(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "Accomodation.ui", self)
        self.HandleButtonsAccommodation()
        self.HandleUIChangesAccommodation()

    def HandleButtonsAccommodation(self):
        self.pushButton_4.clicked.connect(self.click_HotelsApply)
        self.pushButton_5.clicked.connect(self.click_ApartApply)
        self.pushButton_7.clicked.connect(self.click_back)

    def HandleUIChangesAccommodation(self):
        self.setWindowTitle('Apply for Accommodation')

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint |
                            QtCore.Qt.WindowMinimizeButtonHint)

    def click_back(self):
        self.new = FanDashboard(self)
        self.new.show()
        self.close()

    def click_HotelsApply(self):
        self.new = HotelsApply(self)
        self.new.show()
        self.close()

    def click_ApartApply(self):
        self.new = ApartsApply(self)
        self.new.show()
        self.close()

# Class for Hotel Apply UI Interface


class HotelsApply(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "hotelform.ui", self)
        self.HandleButtonsHotels()
        self.HandleUIChangesHotels()

    def HandleButtonsHotels(self):
        self.pushButton_11.clicked.connect(self.click_back)
        self.pushButton.clicked.connect(self.bookHotel1)
        self.pushButton_2.clicked.connect(self.bookHotel2)
        self.pushButton_3.clicked.connect(self.bookHotel3)
        self.pushButton_6.clicked.connect(self.bookHotel4)
        self.pushButton_5.clicked.connect(self.bookHotel5)
        self.pushButton_4.clicked.connect(self.bookHotel6)
        self.pushButton_7.clicked.connect(self.bookHotel7)
        self.pushButton_8.clicked.connect(self.bookHotel8)
        self.pushButton_9.clicked.connect(self.bookHotel9)

    def HandleUIChangesHotels(self):
        self.setWindowTitle('Book Your Hotels')

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint |
                            QtCore.Qt.WindowMinimizeButtonHint)
        hotelList = []
        try:
            query = "SELECT * FROM Hotels"
            mycursor.execute(query)
            hotelList = mycursor.fetchall()
            self.label_2.setText(hotelList[0][0])
            self.label_5.setText(hotelList[1][0])
            self.label_8.setText(hotelList[2][0])
            self.label_3.setText(hotelList[3][0])
            self.label_6.setText(hotelList[4][0])
            self.label_9.setText(hotelList[5][0])
            self.label_4.setText(hotelList[6][0])
            self.label_7.setText(hotelList[7][0])
            self.label_10.setText(hotelList[8][0])

        except:
            print("Error!")

    def open_hotel_priceList(self):
        pass

    def click_back(self):
        self.new = AccommodationApply(self)
        self.new.show()
        self.close()

    def bookHotel1(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_rooms = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        hotel_name = self.label_2.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO hotelreservations (Hotel_Name, CNIC, No_of_Rooms, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (hotel_name, CNIC, no_of_rooms, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "", "Your accommodation is reserved, Go ahead!")
        except:
            print("Error")

    def bookHotel2(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_rooms = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        hotel_name = self.label_5.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO hotelreservations (Hotel_Name, CNIC, No_of_Rooms, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (hotel_name, CNIC, no_of_rooms, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "", "Your accommodation is reserved, Go ahead!")
        except:
            print("Error")

    def bookHotel3(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_rooms = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        hotel_name = self.label_8.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO hotelreservations (Hotel_Name, CNIC, No_of_Rooms, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (hotel_name, CNIC, no_of_rooms, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "", "Your accommodation is reserved, Go ahead!")
        except:
            print("Error")

    def bookHotel4(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_rooms = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        hotel_name = self.label_3.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO hotelreservations (Hotel_Name, CNIC, No_of_Rooms, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (hotel_name, CNIC, no_of_rooms, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "", "Your accommodation is reserved, Go ahead!")
        except:
            print("Error")

    def bookHotel5(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_rooms = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        hotel_name = self.label_6.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO hotelreservations (Hotel_Name, CNIC, No_of_Rooms, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (hotel_name, CNIC, no_of_rooms, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "", "Your accommodation is reserved, Go ahead!")
        except:
            print("Error")

    def bookHotel6(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_rooms = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        hotel_name = self.label_9.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO hotelreservations (Hotel_Name, CNIC, No_of_Rooms, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (hotel_name, CNIC, no_of_rooms, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "", "Your accommodation is reserved, Go ahead!")
        except:
            print("Error")

    def bookHotel7(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_rooms = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        hotel_name = self.label_4.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO hotelreservations (Hotel_Name, CNIC, No_of_Rooms, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (hotel_name, CNIC, no_of_rooms, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "", "Your accommodation is reserved, Go ahead!")
        except:
            print("Error")

    def bookHotel8(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_rooms = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        hotel_name = self.label_7.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO hotelreservations (Hotel_Name, CNIC, No_of_Rooms, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (hotel_name, CNIC, no_of_rooms, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "", "Your accommodation is reserved, Go ahead!")
        except:
            print("Error")

    def bookHotel9(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_rooms = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        hotel_name = self.label_10.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO hotelreservations (Hotel_Name, CNIC, No_of_Rooms, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (hotel_name, CNIC, no_of_rooms, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "", "Your accommodation is reserved, Go ahead!")
        except:
            print("Error")


class ApartsApply(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "Appartments.ui", self)
        self.HandleButtonsApartApply()
        self.HandleUIChangesApartApply()

    def HandleButtonsApartApply(self):
        self.pushButton_11.clicked.connect(self.click_back)
        self.pushButton_5.clicked.connect(self.book_apart1)
        self.pushButton_9.clicked.connect(self.book_apart2)
        self.pushButton_13.clicked.connect(self.book_apart3)
        self.pushButton_4.clicked.connect(self.book_apart4)
        self.pushButton_8.clicked.connect(self.book_apart5)
        self.pushButton_10.clicked.connect(self.book_apart6)
        self.pushButton_6.clicked.connect(self.book_apart7)
        self.pushButton_7.clicked.connect(self.book_apart8)
        self.pushButton_12.clicked.connect(self.book_apart9)

    def HandleUIChangesApartApply(self):
        self.setWindowTitle('Book Your Apartments')

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint |
                            QtCore.Qt.WindowMinimizeButtonHint)
        apartList = []
        try:
            query = "SELECT * FROM Apartments"
            mycursor.execute(query)
            apartList = mycursor.fetchall()
            self.label_5.setText(apartList[0][0])
            self.label_10.setText(apartList[1][0])
            self.label_12.setText(apartList[2][0])
            self.label_6.setText(apartList[3][0])
            self.label_9.setText(apartList[4][0])
            self.label_14.setText(apartList[5][0])
            self.label_7.setText(apartList[6][0])
            self.label_8.setText(apartList[7][0])
            self.label_13.setText(apartList[8][0])

        except:
            print("Error!")

    def book_apart1(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_units = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        apart_name = self.label_5.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO appartmentsreservations (Apartment_Name, CNIC, No_of_Units, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (apart_name, CNIC, no_of_units, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "Response",  "Your request has been sent to Accommodation Manager")
        except:
            print("Error")

    def book_apart2(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_units = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        apart_name = self.label_10.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO appartmentsreservations (Apartment_Name, CNIC, No_of_Units, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (apart_name, CNIC, no_of_units, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "Response",  "Your request has been sent to Accommodation Manager")
        except:
            print("Error")

    def book_apart3(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_units = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        apart_name = self.label_12.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO appartmentsreservations (Apartment_Name, CNIC, No_of_Units, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (apart_name, CNIC, no_of_units, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "Response",  "Your request has been sent to Accommodation Manager")
        except:
            print("Error")

    def book_apart4(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_units = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        apart_name = self.label_6.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO appartmentsreservations (Apartment_Name, CNIC, No_of_Units, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (apart_name, CNIC, no_of_units, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "Response",  "Your request has been sent to Accommodation Manager")
        except:
            print("Error")

    def book_apart5(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_units = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        apart_name = self.label_9.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO appartmentsreservations (Apartment_Name, CNIC, No_of_Units, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (apart_name, CNIC, no_of_units, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "Response",  "Your request has been sent to Accommodation Manager")
        except:
            print("Error")

    def book_apart6(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_units = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        apart_name = self.label_14.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO appartmentsreservations (Apartment_Name, CNIC, No_of_Units, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (apart_name, CNIC, no_of_units, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "Response",  "Your request has been sent to Accommodation Manager")
        except:
            print("Error")

    def book_apart7(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_units = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        apart_name = self.label_7.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO appartmentsreservations (Apartment_Name, CNIC, No_of_Units, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (apart_name, CNIC, no_of_units, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "Response",  "Your request has been sent to Accommodation Manager")
        except:
            print("Error")

    def book_apart8(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_units = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        apart_name = self.label_8.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO appartmentsreservations (Apartment_Name, CNIC, No_of_Units, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (apart_name, CNIC, no_of_units, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "Response",  "Your request has been sent to Accommodation Manager")
        except:
            print("Error")

    def book_apart9(self):
        checkIn = (self.dateEdit.date()).toString(Qt.ISODate)
        checkOut = (self.dateEdit_2.date()).toString(Qt.ISODate)
        no_of_units = self.spinBox.value()
        CNIC = LoginWindow.getCNIC(self)
        apart_name = self.label_13.text()
        status = 'unapproved'
        price = 0
        try:
            mycursor.execute('''INSERT INTO appartmentsreservations (Apartment_Name, CNIC, No_of_Units, Check_In, Check_Out, Price, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s)''', (apart_name, CNIC, no_of_units, checkIn, checkOut, price, status))
            mydb.commit()
            QMessageBox.about(
                self, "Response",  "Your request has been sent to Accommodation Manager")
        except:
            print("Error")

    def click_back(self):
        self.new = AccommodationApply(self)
        self.new.show()
        self.close()
# Class for FIFA Store UI Interface


class FifaStore(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "FIFAStore.ui", self)
        self.HandleButtonsFifaStore()
        self.HandleUIChangesFifaStore()

    def HandleButtonsFifaStore(self):
        self.pushButton_4.clicked.connect(self.open_Jerseys_Tab)
        self.pushButton_6.clicked.connect(self.open_Shoes_Tab)
        self.pushButton_5.clicked.connect(self.open_Others_Tab)
        self.pushButton_11.clicked.connect(self.click_back)
        self.pushButton_2.clicked.connect(self.show_Notifications_tab)
        self.pushButton_3.clicked.connect(self.orderProducts)

    def HandleUIChangesFifaStore(self):
        self.tabWidget.tabBar().setVisible(False)
        self.showProducts()
        self.showNotifications()

    def orderProducts(self):
        CNIC = LoginWindow.getCNIC(self)
        print(CNIC)
        products = self.lineEdit.text().split(" ")
        city = self.lineEdit_2.text()
        address = self.lineEdit_4.text()
        order_status = 'not confirmed'
        prices = []
        odatetime = datetime.now()
        print(products)
        order_datetime = odatetime.strftime("%Y-%m-%d %H:%M:%S")
        print(order_datetime)
        for productID in products:
            try:
                mycursor.callproc("getProductPriceproc", [productID])
                print(mycursor.stored_results())
                for result in mycursor.stored_results():
                    price = result.fetchall()
                    prices.append(price[0][0])

            except:
                QMessageBox(self, "Sorry",
                            "One of the Product is not avaialable")

        totalPrice = sum(prices)
        try:
            mycursor.execute('''INSERT INTO football_worldcup_management.order (CNIC, order_datetime, delivery_address, city_of_delivery, order_status, totalPrice)
            VALUES(%s, %s, %s, %s, %s, %s)''', (CNIC, order_datetime, address, city, order_status, totalPrice))
            mydb.commit()

            mycursor.execute(
                '''set session information_schema_stats_expiry=0''')
            query = f"SELECT AUTO_INCREMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'football_worldcup_management' AND TABLE_NAME = 'order'"

            mycursor.execute(query)
            lastorder = mycursor.fetchall()
            lastorderID = lastorder[0][0]-1

            for productId in products:

                mycursor.execute('''INSERT INTO productsbought (order_No, product_id)
                VALUES(%s, %s)''', (lastorderID, productId))
                mydb.commit()

            QMessageBox.about(self, "Done", "Your order request has been sent")
            self.showNotifications()
        except:
            print("Error")

    def click_back(self):
        self.new = FanDashboard(self)
        self.new.show()
        self.close()

    def showNotifications(self):
        CNIC = [LoginWindow.getCNIC(self)]
        try:
            mycursor.callproc("confirmedordersproc", CNIC)
            for result in mycursor.stored_results():
                confirmorders = result.fetchall()
            self.tableWidget_4.setRowCount(50)
            tableRow = 0
            if len(confirmorders) != 0:
                for row in confirmorders:
                    self.tableWidget_4.setItem(
                        tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget_4.setItem(
                        tableRow, 1, QtWidgets.QTableWidgetItem(row[2]))
                    self.tableWidget_4.setItem(
                        tableRow, 2, QtWidgets.QTableWidgetItem(row[3]))
                    self.tableWidget_4.setItem(
                        tableRow, 3, QtWidgets.QTableWidgetItem(row[4]))
                    self.tableWidget_4.setItem(
                        tableRow, 4, QtWidgets.QTableWidgetItem(str(row[6])))
                    tableRow += 1
            else:
                self.tableWidget_4.setItem(
                    tableRow, 0, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_4.setItem(
                    tableRow, 1, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_4.setItem(
                    tableRow, 2, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_4.setItem(
                    tableRow, 3, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_4.setItem(
                    tableRow, 4, QtWidgets.QTableWidgetItem('NULL'))
                tableRow += 1
        except:
            print("Error")

        try:
            mycursor.callproc("unconfirmedorderproc", CNIC)
            for result in mycursor.stored_results():
                unconfirmorders = result.fetchall()
            self.tableWidget_5.setRowCount(50)
            tableRow = 0
            if len(unconfirmorders) != 0:
                for row in unconfirmorders:
                    self.tableWidget_5.setItem(
                        tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget_5.setItem(
                        tableRow, 1, QtWidgets.QTableWidgetItem(row[2]))
                    self.tableWidget_5.setItem(
                        tableRow, 2, QtWidgets.QTableWidgetItem(row[3]))
                    self.tableWidget_5.setItem(
                        tableRow, 3, QtWidgets.QTableWidgetItem(row[4]))
                    self.tableWidget_5.setItem(
                        tableRow, 4, QtWidgets.QTableWidgetItem(str(row[6])))
                    tableRow += 1
            else:
                self.tableWidget_5.setItem(
                    tableRow, 0, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_5.setItem(
                    tableRow, 1, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_5.setItem(
                    tableRow, 2, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_5.setItem(
                    tableRow, 3, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_5.setItem(
                    tableRow, 4, QtWidgets.QTableWidgetItem('NULL'))
                tableRow += 1
        except:
            print("Error")

    def showProducts(self):
        cateogories = [['Football jerseys'], [
            'Football shoes'], ['Football accessories']]
        try:
            # USING STORED PROCEDURE

            mycursor.callproc("productcategoryproc", cateogories[0])
            for result in mycursor.stored_results():
                jerseys = result.fetchall()
            self.tableWidget.setRowCount(50)
            tableRow = 0
            if len(jerseys) != 0:
                for row in jerseys:
                    self.tableWidget.setItem(
                        tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(
                        tableRow, 1, QtWidgets.QTableWidgetItem(row[2]))
                    self.tableWidget.setItem(
                        tableRow, 2, QtWidgets.QTableWidgetItem(row[3]))
                    self.tableWidget.setItem(
                        tableRow, 3, QtWidgets.QTableWidgetItem(str(row[4])))
                    tableRow += 1
            else:
                self.tableWidget.setItem(
                    tableRow, 0, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget.setItem(
                    tableRow, 1, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget.setItem(
                    tableRow, 2, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget.setItem(
                    tableRow, 3, QtWidgets.QTableWidgetItem('NULL'))
                tableRow += 1

            mycursor.callproc("productcategoryproc", cateogories[1])
            for result in mycursor.stored_results():
                shoes = result.fetchall()
            self.tableWidget_2.setRowCount(50)
            tableRow = 0
            if len(shoes) != 0:
                for row in shoes:
                    self.tableWidget_2.setItem(
                        tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget_2.setItem(
                        tableRow, 1, QtWidgets.QTableWidgetItem(row[2]))
                    self.tableWidget_2.setItem(
                        tableRow, 2, QtWidgets.QTableWidgetItem(row[3]))
                    self.tableWidget_2.setItem(
                        tableRow, 3, QtWidgets.QTableWidgetItem(str(row[4])))
                    tableRow += 1
            else:
                self.tableWidget_2.setItem(
                    tableRow, 0, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_2.setItem(
                    tableRow, 1, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_2.setItem(
                    tableRow, 2, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_2.setItem(
                    tableRow, 3, QtWidgets.QTableWidgetItem('NULL'))
                tableRow += 1

            mycursor.callproc("productcategoryproc", cateogories[2])
            for result in mycursor.stored_results():
                otheraccessories = result.fetchall()
            self.tableWidget_3.setRowCount(50)
            tableRow = 0
            if len(otheraccessories) != 0:
                for row in otheraccessories:
                    self.tableWidget_3.setItem(
                        tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget_3.setItem(
                        tableRow, 1, QtWidgets.QTableWidgetItem(row[2]))
                    self.tableWidget_3.setItem(
                        tableRow, 2, QtWidgets.QTableWidgetItem(row[3]))
                    self.tableWidget_3.setItem(
                        tableRow, 3, QtWidgets.QTableWidgetItem(str(row[4])))
                    tableRow += 1
            else:
                self.tableWidget_3.setItem(
                    tableRow, 0, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_3.setItem(
                    tableRow, 1, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_3.setItem(
                    tableRow, 2, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_3.setItem(
                    tableRow, 3, QtWidgets.QTableWidgetItem('NULL'))
                tableRow += 1

        except:
            print("Error")

    def show_Notifications_tab(self):
        self.tabWidget.setCurrentIndex(3)

    def open_notification(self):
        self.tabWidget.setCurrentIndex(3)

    def open_Jerseys_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_Shoes_Tab(self):
        self.tabWidget.setCurrentIndex(1)

    def open_Others_Tab(self):
        self.tabWidget.setCurrentIndex(2)


# Class for UserDetails UI Interface

class knockOutForm(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "KnockOutForm.ui", self)
        self.HandleButtonsKOForm()
        self.HandleUIChangesKOForm()

    def HandleButtonsKOForm(self):
        pass

    def HandleUIChangesKOFomr(self):
        pass


class UserDetails(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "userDetail.ui", self)
        self.HandleButtonUserDetails()
        self.HandleUIChangesUserDetails()

    def showUserDetail_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def editUser_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def HandleButtonUserDetails(self):
        self.pushButton_6.clicked.connect(self.editUser_tab)
        self.pushButton_5.clicked.connect(self.showUserDetail_tab)
        self.pushButton_7.clicked.connect(self.click_back)
        self.pushButton_8.clicked.connect(self.editDetails)

    def HandleUIChangesUserDetails(self):
        self.tabWidget.tabBar().setVisible(False)
        self.showUserDetails()

    def showUserDetails(self):
        details = []

        emailAddress = [email]
        mycursor.callproc("userDetailsproc", emailAddress)
        # query = f"SELECT * FROM football_fan WHERE Email_Address = '{email}'"
        # mycursor.execute(query)
        for result in mycursor.stored_results():
            details = result.fetchall()
        # except:
            # print("Error")
        self.tableWidget.setRowCount(1)
        print(details)
        self.tableWidget.setItem(
            0, 0, QtWidgets.QTableWidgetItem(str(details[0][1])))
        self.tableWidget.setItem(
            0, 1, QtWidgets.QTableWidgetItem(str(details[0][2])))
        self.tableWidget.setItem(
            0, 2, QtWidgets.QTableWidgetItem(str(details[0][4])))
        self.tableWidget.setItem(
            0, 3, QtWidgets.QTableWidgetItem(str(details[0][0])))
        self.tableWidget.setItem(
            0, 4, QtWidgets.QTableWidgetItem(str(details[0][7])))

    def click_back(self):
        self.new = FanDashboard(self)
        self.new.show()
        self.close()

    def editDetails(self):
        newPass = self.lineEdit_2.text()
        newFName = self.lineEdit_4.text()
        newLName = self.lineEdit_5.text()
        CNIC = LoginWindow.getCNIC(self)
        print(CNIC)
        print(newFName)
        print(newLName)
        print(newPass)
        try:

            if newPass != '':

                mycursor.execute(
                    f'''UPDATE football_fan SET password = '{newPass}' WHERE CNIC = '{CNIC}' ''')
                mydb.commit()

            if newFName != '' and newLName != '':
                mycursor.execute(
                    f'''UPDATE football_fan SET First_Name = '{newFName}', Last_Name = '{newLName}'WHERE CNIC = '{CNIC}' ''')
                mydb.commit()
            QMessageBox.about(self, "Done", "Details Updated")
            self.showUserDetails()
        except:
            print("Error")


# Class for Match Schedules UI Interface


class MatchSchedules(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "SNF.ui", self)
        self.HandleButtonsSNF()
        self.HandleUIChangesSNF()

    def HandleButtonsSNF(self):
        self.pushButton.clicked.connect(self.openFixtures)
        self.pushButton_2.clicked.connect(self.openGroups)
        self.pushButton_4.clicked.connect(self.openTeamStats)
        self.pushButton_3.clicked.connect(self.openPlayerStats)
        self.pushButton_37.clicked.connect(self.openFanDashboard)

    def HandleUIChangesSNF(self):
        pass

    def openFanDashboard(self):
        self.new = FanDashboard(self)
        self.new.show()
        self.close()

    def openFixtures(self):
        self.new = Fixtures(self)
        self.new.show()
        self.close()


class PlayerStats(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "PlayerStats.ui", self)


class TeamStats(QtWidgets.QWidget):
    pass


class MatchSchedules(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "Schedule.ui", self)


class Fixtures(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "matchFictures.ui", self)
# Class for Fifa Tickets UI Interface


class FifaTickets(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "form.ui", self)


# Class for Flight Apply UI Interface


class FlightsApply(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "Flight.ui", self)
        self.HandleButtonsFlightsApply()
        self.HandleUIChangesFlightsApply()

    def HandleButtonsFlightsApply(self):
        self.pushButton.clicked.connect(self.on_search_button)
        self.pushButton_2.clicked.connect(self.reserveFlight)
        self.pushButton_7.clicked.connect(self.click_back)

    def HandleUIChangesFlightsApply(self):
        airlines = []
        arrival = []
        depart = []
        arrivalCities = []
        departCities = []
        try:
            query = "SELECT airline_name FROM Airlines"
            mycursor.execute(query)
            airlines2 = mycursor.fetchall()
        except:
            print("Error")

        try:
            query = "SELECT DISTINCT arrivalCity FROM Flights"
            mycursor.execute(query)
            arrival = mycursor.fetchall()
        except:
            print("Error")

        try:
            query = "SELECT DISTINCT departCity FROM Flights"
            mycursor.execute(query)
            depart = mycursor.fetchall()
        except:
            print("Error")

        for airline in airlines2:
            airlines.append(airline[0])

        for i in range(len(arrival)):
            arrivalCities.append(arrival[i][0])
            departCities.append(depart[i][0])

        self.comboBox_4.addItems(airlines)
        self.comboBox_2.addItems(arrivalCities)
        self.comboBox.addItems(departCities)

    def click_back(self):
        self.new = FanDashboard(self)
        self.new.show()
        self.close()

    def reserveFlight(self):
        reserveID = self.lineEdit.text()
        seatClass = self.comboBox_3.currentText()
        status = 'not confirmed'
        CNIC = LoginWindow.getCNIC(self)
        try:
            mycursor.execute('''INSERT INTO flightreservation (Flight_No, CNIC, SeatClass, status)
            VALUES(%s, %s, %s, %s)''', (reserveID, CNIC, seatClass, status))
            mydb.commit()
            QMessageBox.about(self, "Done", "Flight Reserved Successfully")
        except:
            print("Error")

    def get_ReserveID(self):
        reserve_ID = 0
        CNIC = LoginWindow.getCNIC(self)
        try:
            query = f"SELECT MAX(flight_reserve_id) FROM flightreservation WHERE CNIC = '{CNIC}'"
            mycursor.execute(query)
            reserve = mycursor.fetchall()
        except:
            print("Error")

    def on_search_button(self):
        flights = []
        departDate = (self.dateEdit.date()).toString(Qt.ISODate)
        departCity = self.comboBox.currentText()
        arrivalCity = self.comboBox_2.currentText()
        airline = self.comboBox_4.currentText()
        try:

            query = f"SELECT * FROM Flights NATURAL JOIN seatclasses WHERE arrivalCity = '{arrivalCity}' AND departCity = '{departCity}' AND SUBSTRING(departTime,1,10) = '{departDate}' AND airline_code = (SELECT airline_code FROM airlines WHERE airline_name= '{airline}')"

            mycursor.execute(query)
            flights = mycursor.fetchall()
            print(flights)
            self.tableWidget_2.setRowCount(10)
            tableRow = 0
            for row in flights:
                self.tableWidget_2.setItem(
                    tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                self.tableWidget_2.setItem(
                    tableRow, 1, QtWidgets.QTableWidgetItem(row[1]))
                self.tableWidget_2.setItem(
                    tableRow, 2, QtWidgets.QTableWidgetItem(row[6]))
                self.tableWidget_2.setItem(
                    tableRow, 3, QtWidgets.QTableWidgetItem(row[5]))
                self.tableWidget_2.setItem(
                    tableRow, 4, QtWidgets.QTableWidgetItem(str(row[2])))
                self.tableWidget_2.setItem(
                    tableRow, 5, QtWidgets.QTableWidgetItem(str(row[7])))
                self.tableWidget_2.setItem(
                    tableRow, 6, QtWidgets.QTableWidgetItem(str(row[8])))
                tableRow += 1

        except:
            print("Error")


# Class for FIfaStoreManager UI Interface

class FifaStoreManager(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "StoreManager.ui", self)
        self.HandleButtonsStoreManager()
        self.HandleUIChagesStoreManager()

    def HandleButtonsStoreManager(self):
        self.pushButton_8.clicked.connect(self.openAddItemBar)
        self.pushButton_11.clicked.connect(self.deleteItemBar)
        self.pushButton_12.clicked.connect(self.updateItemBar)
        self.pushButton_13.clicked.connect(self.AddProducts)
        self.pushButton_14.clicked.connect(self.DeleteProducts)
        self.pushButton_15.clicked.connect(self.UpdateProducts)
        self.pushButton_16.clicked.connect(self.click_back)
        self.pushButton_9.clicked.connect(self.ConfirmOrder)
        self.pushButton_10.clicked.connect(self.DiscardOrder)

    def HandleUIChagesStoreManager(self):
        self.tabWidget.tabBar().setVisible(False)
        self.showProducts()
        self.showNewOrders()

    def click_back(self):
        self.new = LoginWindow()
        self.new.show()
        self.close()

    def openAddItemBar(self):
        self.tabWidget.setCurrentIndex(0)

    def deleteItemBar(self):
        self.tabWidget.setCurrentIndex(1)

    def updateItemBar(self):
        self.tabWidget.setCurrentIndex(2)

    def DeleteProducts(self):
        product_id = self.lineEdit_11.text()

        if product_id != '':
            try:
                mycursor.execute(
                    f'''DELETE FROM fifaproducts WHERE product_id = {product_id}''')
                mydb.commit()
                QMessageBox.about(self, "Done", "Product Deleted Successfully")
                self.showProducts()
            except:
                print("Error")

        else:
            QMessageBox.about(self, "Error", "Enter Product ID")

    def ConfirmOrder(self):
        order_id = self.lineEdit_5.text()
        try:
            mycursor.execute(
                f'''UPDATE football_worldcup_management.order SET order_status = 'confirmed' WHERE order_No = '{order_id}' ''')
            mydb.commit()
            QMessageBox.about(self, "Done", "Order Successfully Confirmed")
            self.showNewOrders()
        except:
            print("Error")

    def DiscardOrder(self):
        order_id = self.lineEdit_6.text()
        try:
            mycursor.execute(
                f'''UPDATE football_worldcup_management.order SET order_status = 'discarded' WHERE order_No = '{order_id}' ''')
            mydb.commit()
            QMessageBox.about(self, "Done", "Order Successfully Discarded")
            self.showNewOrders()
        except:
            print("Error")

    def UpdateProducts(self):
        productID = self.lineEdit_15.text()
        productName = self.lineEdit_16.text()
        productDesc = self.lineEdit_12.text()
        productPrice = self.lineEdit_13.text()
        if productID != '':
            try:
                if productName != '' and productName != 'New Product Name':
                    mycursor.execute(
                        f'''UPDATE fifaproducts SET product_name = '{productName}' WHERE product_id = '{productID}' ''')
                    mydb.commit()
                if productDesc != '' and productDesc != 'New Product Description':
                    mycursor.execute(
                        f'''UPDATE fifaproducts SET product_description = '{productDesc}' WHERE product_id = '{productID}' ''')
                    mydb.commit()
                if productPrice != 0 and productPrice != 'New Product Price':
                    mycursor.execute(
                        f'''UPDATE fifaproducts SET price = '{productPrice}' WHERE product_id = '{productID}' ''')
                    mydb.commit()
                QMessageBox.about(
                    self, "Done", "Changes Successfully Updated")
            except:
                print("Error")

        else:
            QMessageBox.about(self, "Error", "Accommodation Name not entered")

    def AddProducts(self):
        category = self.comboBox_2.currentText()
        productName = self.lineEdit_3.text()
        productDescription = self.lineEdit_10.text()
        productPrice = self.lineEdit_4.text()

        if productName != '' and productName != 'Product Name':
            try:
                mycursor.execute('''INSERT INTO fifaproducts (product_category, product_name, product_description, price)
                VALUES(%s, %s, %s, %s)''', (category, productName, productDescription, productPrice))
                mydb.commit()
                QMessageBox.about(self, "Done", "Product Added Successfully")
                self.showProducts()
            except:
                print("Error")

        else:
            QMessageBox.about(self, "Error", "Enter Product Name")

    def showNewOrders(self):
        try:
            # using View
            query = f"SELECT order_No, GROUP_CONCAT(product_id)AS Products, CNIC, order_datetime, delivery_address, city_of_delivery, totalPrice FROM productsfororder GROUP BY order_No"
            mycursor.execute(query)
            orders = mycursor.fetchall()
            print(orders)
            self.tableWidget_2.setRowCount(50)
            tableRow = 0
            if len(orders) != 0:
                for row in orders:
                    self.tableWidget_2.setItem(
                        tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget_2.setItem(
                        tableRow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    self.tableWidget_2.setItem(
                        tableRow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                    self.tableWidget_2.setItem(
                        tableRow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                    self.tableWidget_2.setItem(
                        tableRow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.tableWidget_2.setItem(
                        tableRow, 5, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.tableWidget_2.setItem(
                        tableRow, 6, QtWidgets.QTableWidgetItem(str(row[4])))
                    tableRow += 1
            else:
                self.tableWidget_2.setItem(
                    tableRow, 0, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_2.setItem(
                    tableRow, 1, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_2.setItem(
                    tableRow, 2, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_2.setItem(
                    tableRow, 3, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_2.setItem(
                    tableRow, 4, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_2.setItem(
                    tableRow, 5, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_2.setItem(
                    tableRow, 6, QtWidgets.QTableWidgetItem('NULL'))
                tableRow += 1
        except:
            print("Error")

    def showProducts(self):
        try:
            query = f"SELECT * FROM fifaproducts"
            mycursor.execute(query)
            products = mycursor.fetchall()

            self.tableWidget.setRowCount(50)
            tableRow = 0
            if len(products) != 0:
                for row in products:
                    self.tableWidget.setItem(
                        tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(
                        tableRow, 1, QtWidgets.QTableWidgetItem(row[1]))
                    self.tableWidget.setItem(
                        tableRow, 2, QtWidgets.QTableWidgetItem(row[2]))
                    self.tableWidget.setItem(
                        tableRow, 3, QtWidgets.QTableWidgetItem(row[3]))
                    self.tableWidget.setItem(
                        tableRow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    tableRow += 1
            else:
                self.tableWidget.setItem(
                    tableRow, 0, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget.setItem(
                    tableRow, 1, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget.setItem(
                    tableRow, 2, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget.setItem(
                    tableRow, 3, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget.setItem(
                    tableRow, 4, QtWidgets.QTableWidgetItem('NULL'))
                tableRow += 1
        except:
            print("Error")


class FlightManager(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "FlightManager.ui", self)
        self.HandleButtonsFlightManager()
        self.HandleUIChangesFlightManager()

    def HandleButtonsFlightManager(self):
        self.pushButton_11.clicked.connect(self.AddAirlines)
        self.pushButton_17.clicked.connect(self.AddFlights)
        self.pushButton_18.clicked.connect(self.flightManagement_tab)
        self.pushButton_19.clicked.connect(self.reservations_tab)
        self.pushButton_22.clicked.connect(self.logout)
        self.pushButton_20.clicked.connect(self.confirmReservation)
        self.pushButton_21.clicked.connect(self.discardReservation)

    def HandleUIChangesFlightManager(self):
        self.tabWidget.tabBar().setVisible(False)
        self.showReservations()

    def flightManagement_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def reservations_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def logout(self):
        self.new = LoginWindow()
        self.new.show()
        self.close()

    def showReservations(self):
        try:
            query = "SELECT * FROM flightreservation WHERE status = 'not confirmed'"
            mycursor.execute(query)
            reservations = mycursor.fetchall()
            self.tableWidget_5.setRowCount(50)
            tableRow = 0
            if len(reservations) != 0:
                for row in reservations:
                    self.tableWidget_5.setItem(
                        tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget_5.setItem(
                        tableRow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    self.tableWidget_5.setItem(
                        tableRow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                    self.tableWidget_5.setItem(
                        tableRow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                    self.tableWidget_5.setItem(
                        tableRow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    tableRow += 1
            else:
                self.tableWidget_5.setItem(
                    tableRow, 0, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_5.setItem(
                    tableRow, 1, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_5.setItem(
                    tableRow, 2, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_5.setItem(
                    tableRow, 3, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_5.setItem(
                    tableRow, 4, QtWidgets.QTableWidgetItem('NULL'))
                tableRow += 1

        except:
            print("Error")

    def confirmReservation(self):
        reserveID = self.lineEdit_2.text()
        try:
            mycursor.execute(
                f'''UPDATE flightreservation SET status = 'confirmed' WHERE flight_reserve_id = {reserveID} ''')
            mydb.commit()
            QMessageBox.about(
                self, "Done", "Reservation Confirmed Successfully")
            self.showReservations()
        except:
            print("Error")

    def discardReservation(self):
        reserveID = self.lineEdit_2.text()
        try:
            mycursor.execute(
                f'''UPDATE flightreservation SET status = 'Discarded' WHERE flight_reserve_id = {reserveID} ''')
            mydb.commit()
            QMessageBox.about(
                self, "Done", "Reservation Discarded Successfully")
            self.showReservations()
        except:
            print("Error")

    def AddFlights(self):
        arrivalcity = self.lineEdit_10.text()
        departCity = self.lineEdit_18.text()
        departTime = (self.dateTimeEdit.dateTime()).toString(Qt.ISODate)
        arrivalTime = (self.dateTimeEdit_2.dateTime()).toString(Qt.ISODate)
        price = self.lineEdit_16.text()
        airlineCode = self.lineEdit_17.text()
        capacity = self.lineEdit_13.text()

        try:
            mycursor.execute('''INSERT INTO flights (airline_code, capacity, arrivalCity, departCity, arrivalTime, departTime)
            VALUES(%s, %s, %s, %s, %s, %s)''', (airlineCode, capacity, arrivalcity, departCity, arrivalTime, departTime))
            mydb.commit()

            query = "SELECT MAX(Flight_No) FROM flights"
            mycursor.execute(query)
            maxFlightID = mycursor.fetchall()

            mycursor.execute('''INSERT INTO seatclasses (seatClass, startingPrice, Flight_No) 
            VALUES(%s, %s, %s)''', ('Business', int(price)*2, maxFlightID[0][0]))
            mydb.commit()
            mycursor.execute('''INSERT INTO seatclasses (seatClass, startingPrice, Flight_No) 
            VALUES(%s, %s, %s)''', ('Economy', int(price), maxFlightID[0][0]))
            mydb.commit()
            mycursor.execute('''INSERT INTO seatclasses (seatClass, startingPrice, Flight_No) 
            VALUES(%s, %s, %s)''', ('First Class', int(price)*3, maxFlightID[0][0]))
            mydb.commit()
            mycursor.execute('''INSERT INTO seatclasses (seatClass, startingPrice, Flight_No) 
            VALUES(%s, %s, %s)''', ('Suite', int(price)*4, maxFlightID[0][0]))
            mydb.commit()

            QMessageBox.about(self, "Done", "Flight Added Successfully")

        except:
            print("Error")

    def AddAirlines(self):
        airlineName = self.lineEdit_14.text()
        airlineCode = self.lineEdit_15.text()
        country = "Pakistan"
        telephone = "+92-21-111-786-786"
        try:
            mycursor.execute('''INSERT INTO airlines (airline_code, airline_name, country, telNo_help) 
            VALUES(%s, %s, %s, %s)''', (airlineCode, airlineName, country, telephone))
            mydb.commit()
            QMessageBox.about(self, "Done", "Airline Added Successfully")
        except:
            print("Error")


# Class for HotelsManager UI Interface


class HotelsManager(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "HotelManager.ui", self)
        self.HandleButtonsHotelsManager()
        self.HandleUIChangesHotelsManager()

    def HandleButtonsHotelsManager(self):
        self.pushButton.clicked.connect(self.AddAccommodation)
        self.pushButton_2.clicked.connect(self.DeleteAccommodation)
        self.pushButton_3.clicked.connect(self.UpdateAccommodation)
        self.pushButton_4.clicked.connect(self.ApproveHotelRequest)
        self.pushButton_9.clicked.connect(self.DiscardHotelRequest)
        self.pushButton_6.clicked.connect(self.ApproveApartRequest)
        self.pushButton_8.clicked.connect(self.DiscardApartRequest)
        self.pushButton_11.clicked.connect(self.click_Logout_Button)
        self.pushButton_5.clicked.connect(self.openManagement_tab)
        self.pushButton_10.clicked.connect(self.openHotelRequest_tab)
        self.pushButton_7.clicked.connect(self.openApartRequest_tab)

    def HandleUIChangesHotelsManager(self):
        self.UpdateHotelReserveTable()
        self.UpdateApartmentReserveTable()
        self.tabWidget.tabBar().setVisible(False)

    def openManagement_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def openHotelRequest_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def openApartRequest_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def UpdateHotelReserveTable(self):
        try:
            query = f"SELECT * FROM hotelreservations WHERE status = 'unapproved'"
            mycursor.execute(query)
            hotelreservations = mycursor.fetchall()

            self.tableWidget.setRowCount(50)
            tableRow = 0
            if len(hotelreservations) != 0:
                for row in hotelreservations:
                    self.tableWidget.setItem(
                        tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(
                        tableRow, 1, QtWidgets.QTableWidgetItem(row[1]))
                    self.tableWidget.setItem(
                        tableRow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                    self.tableWidget.setItem(
                        tableRow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                    self.tableWidget.setItem(
                        tableRow, 4, QtWidgets.QTableWidgetItem(row[4]))
                    self.tableWidget.setItem(
                        tableRow, 5, QtWidgets.QTableWidgetItem(row[5]))
                    self.tableWidget.setItem(
                        tableRow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                    tableRow += 1
            else:
                self.tableWidget.setItem(
                    tableRow, 0, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget.setItem(
                    tableRow, 1, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget.setItem(
                    tableRow, 2, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget.setItem(
                    tableRow, 3, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget.setItem(
                    tableRow, 4, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget.setItem(
                    tableRow, 5, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget.setItem(
                    tableRow, 6, QtWidgets.QTableWidgetItem('NULL'))
                tableRow += 1
        except:
            print("Error")

    def click_Logout_Button(self):
        self.new = LoginWindow()
        self.new.show()
        self.close()

    def UpdateApartmentReserveTable(self):
        try:
            query = f"SELECT * FROM appartmentsreservations WHERE status = 'unapproved'"
            mycursor.execute(query)
            apartreservations = mycursor.fetchall()
            self.tableWidget_2.setRowCount(50)
            tableRow = 0
            print(apartreservations)
            if len(apartreservations) != 0:
                for row in apartreservations:
                    self.tableWidget_2.setItem(
                        tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget_2.setItem(
                        tableRow, 1, QtWidgets.QTableWidgetItem(row[1]))
                    self.tableWidget_2.setItem(
                        tableRow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                    self.tableWidget_2.setItem(
                        tableRow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                    self.tableWidget_2.setItem(
                        tableRow, 4, QtWidgets.QTableWidgetItem(row[4]))
                    self.tableWidget_2.setItem(
                        tableRow, 5, QtWidgets.QTableWidgetItem(row[5]))
                    self.tableWidget_2.setItem(
                        tableRow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                    tableRow += 1
            else:
                self.tableWidget_2.setItem(
                    tableRow, 0, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_2.setItem(
                    tableRow, 1, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_2.setItem(
                    tableRow, 2, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_2.setItem(
                    tableRow, 3, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_2.setItem(
                    tableRow, 4, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_2.setItem(
                    tableRow, 5, QtWidgets.QTableWidgetItem('NULL'))
                self.tableWidget_2.setItem(
                    tableRow, 6, QtWidgets.QTableWidgetItem('NULL'))
                tableRow += 1

        except:
            print("Error")

    def ApproveHotelRequest(self):
        reserve_id = self.lineEdit.text()
        try:
            mycursor.execute(
                f'''UPDATE hotelreservations SET status = 'approved' WHERE hotel_reserve_id = '{reserve_id}' ''')
            mydb.commit()
            QMessageBox.about(self, "Done", "Hotel Successfully Approved")
            self.UpdateHotelReserveTable()
        except:
            print("Error")

    def DiscardHotelRequest(self):
        reserve_id = self.lineEdit.text()
        try:
            mycursor.execute(
                f'''UPDATE hotelreservations SET status = 'Discarded' WHERE hotel_reserve_id = {reserve_id} ''')
            mydb.commit()
            QMessageBox.about(self, "Done", "Hotel Successfully Discarded")
            self.UpdateHotelReserveTable()
        except:
            print("Error")

    def ApproveApartRequest(self):
        reserve_id = self.lineEdit_11.text()
        try:
            mycursor.execute(
                f'''UPDATE appartmentsreservations SET status = 'approved' WHERE apart_reserve_id = {reserve_id} ''')
            mydb.commit()
            QMessageBox.about(self, "Done", "Apartment Successfully Approved")
            self.UpdateApartmentReserveTable()
        except:
            print("Error")

    def DiscardApartRequest(self):
        reserve_id = self.lineEdit_11.text()
        try:
            mycursor.execute(
                f'''UPDATE appartmentsreservations SET status = 'approved' WHERE apart_reserve_id = '{reserve_id}' ''')
            mydb.commit()
            QMessageBox.about(self, "Done", "Apartment Successfully Discarded")
            self.UpdateApartmentReserveTable()

        except:
            print("Error")

    def AddAccommodation(self):
        accType = self.comboBox.currentText()
        accName = self.lineEdit_4.text()
        city = self.lineEdit_5.text()
        address = self.lineEdit_3.text()
        price = self.spinBox.value()

        if accName != '':
            if accType == 'Hotel':

                try:
                    mycursor.execute('''INSERT INTO hotels (Hotel_Name, singleBedPrice, doubleBedPrice, tripleBedPrice, city, address)
                    VALUES(%s, %s, %s, %s, %s, %s)''', (accName, price, 1.5*price, 2*price, city, address))
                    mydb.commit()
                    QMessageBox.about(self, "Done", "Hotel Added Successfully")
                except:
                    print("Error")

            elif accType == 'Apartment':
                try:
                    mycursor.execute('''INSERT INTO apartments (Apartment_Name, pricePerUnit, city, address)
                    VALUES(%s, %s, %s, %s)''', (accName, price, city, address))
                    mydb.commit()
                    QMessageBox.about(
                        self, "Done", "Apartment Added Successfully")
                except:
                    print("Error")
        else:
            QMessageBox.about(self, "Error", "Enter Apartment Name")

    def DeleteAccommodation(self):
        accType = self.comboBox.currentText()
        accName = self.lineEdit_4.text()
        city = self.lineEdit_5.text()
        address = self.lineEdit_3.text()

        if accName != '':
            if accType == 'Hotel':
                # try:
                mycursor.execute(
                    f'''DELETE FROM hotels WHERE Hotel_Name = '{accName}' ''')
                mydb.commit()
                QMessageBox.about(self, "Done", "Hotel Deleted Successfully")
                # except:
                # print("Error")

            elif accType == 'Apartment':
                try:
                    mycursor.execute(
                        f'''DELETE FROM apartments WHERE Apartment_Name = '{accName}' ''')
                    mydb.commit()
                    QMessageBox.about(
                        self, "Done", "Apartment Deleted Successfully")
                except:
                    print("Error")
        else:
            QMessageBox.about(
                self, "Error", "Apartment Name not Entered")

    def UpdateAccommodation(self):
        accType = self.comboBox.currentText()
        accName = self.lineEdit_4.text()
        city = self.lineEdit_5.text()
        address = self.lineEdit_3.text()
        price = self.spinBox.value()

        if accName != '':
            if accType == 'Hotel':
                try:
                    if city != '':
                        mycursor.execute(
                            f'''UPDATE hotels SET city = '{city}' WHERE Hotel_Name = '{accName}' ''')
                        mydb.commit()
                    if address != '':
                        mycursor.execute(
                            f'''UPDATE hotels SET address = '{address}' WHERE Hotel_Name = '{accName}' ''')
                        mydb.commit()
                    if price != 0:
                        mycursor.execute(
                            f'''UPDATE hotels SET singleBedPrice = '{price}', doubleBedPrice = '{1.5*price}', tripleBedPrice = '{2*price}' WHERE Hotel_Name = '{accName}' ''')
                        mydb.commit()
                    QMessageBox.about(
                        self, "Done", "Changes Successfully Updated")
                except:
                    print("Error")
            elif accType == 'Apartment':
                try:
                    if city != '':
                        mycursor.execute(
                            f'''UPDATE apartments SET city = '{city}' WHERE Apartment_Name = '{accName}' ''')
                        mydb.commit()
                    if address != '':
                        mycursor.execute(
                            f'''UPDATE apartments SET address = '{address}' WHERE Apartment_Name = '{accName}' ''')
                        mydb.commit()
                    if price != '':
                        mycursor.execute(
                            f'''UPDATE apartments SET pricePerUnit = '{price}' WHERE Apartment_Name = '{accName}' ''')
                        mydb.commit()
                    QMessageBox.about(
                        self, "Done", "Changes Successfully Updated")
                except:
                    print("Error")
        else:
            QMessageBox.about(self, "Error", "Accommodation Name not entered")


class Payment(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "payment.ui", self)

    def HandleButtonsPayment(self):
        pass

    def HandleUIChangesPayment(self):
        pass

# Class for TeamDataManager UI Interface


class TeamDataManager(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "teamDataManager.ui", self)

# Class for EditDetails UI Interface


class TicketManager(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "TicketManager.ui", self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
   # app.setStyleSheet(stylesheet)
    window = LoginWindow()
    window.show()
    app.exec_()
