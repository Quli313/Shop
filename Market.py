from PyQt5 import QtWidgets
from Quliyev import Ui_MainWindow
import sys
import mysql.connector
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from math import *
import random
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from openpyxl import *
import xlsxwriter
import datetime
from fpdf import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from tkinter import *
from PyQt5.QtWidgets import QFileDialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages



class mywindow(QtWidgets.QMainWindow): 

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # self.mydb = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="12348765",
        #     database="datamiz"
        # )

        # self.cursor = self.mydb.cursor()

        self.ui.calendarWidget.setVisible(False)
        self.ui.TB.clicked.connect(self.Tarix)
        self.ui.calendarWidget.clicked[QDate].connect(self.Secmek)
        self.ui.PB1.clicked.connect(self.Add)
        self.ui.PB3.clicked.connect(self.Delete)
        self.ui.PB4.clicked.connect(self.Excel)
        self.ui.PB5.clicked.connect(self.PDF)
        self.ui.PB6.clicked.connect(self.Yekun)
        self.column_headers = ["ID", "Kod", "Malın adı", "Qiymət", "Miqdar", "Məbləğ", "EDV", "Ümumi dəyər", "Tarix"]


#-------------------------------------ADD-------------------------------------------

    def Add(self):
        Malinadi = self.ui.lineEdit.text()
        Qiymet = self.ui.lineEdit_2.text()
        Miqdar = self.ui.lineEdit_3.text()
        Mebleg = float(Qiymet) * int(Miqdar)
        EDV = float(Mebleg) * 0.018
        Umumideyer = float(EDV) + float(Mebleg)

        # Miqdar boş olsa error verir
        if not Miqdar or not Miqdar.isdigit():
            QMessageBox.warning(self, 'Error', 'Miqdar integer olmalıdır!')
            return

        # Qiymət boş olsa error verir 
        if not Qiymet:
            QMessageBox.warning(self, 'Error', 'Qiymət boş ola bilməz!')
            return
        try:
            Qiymet = float(Qiymet)
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Qiymət float olmalıdır!')
            return
        

        
        # Kod sütunu üçün random 4 rəqəmli ədəd
        Kod = str(random.randint(1000,9999))
        
        # Bu günün tarixini yeni yaranan sətirə əlavə etmə
        tarix = QDate.currentDate().toString('yyyy-MM-dd')
    

        # Nəticə
        query = "INSERT INTO mallar (Kod, Malinadi, Qiymet, Miqdar, Mebleg, EDV, Umumideyer, tarix) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (Kod, Malinadi, Qiymet, Miqdar, Mebleg, EDV, Umumideyer, tarix)
        self.cursor.execute(query, values)
        self.mydb.commit()
        QMessageBox.information(self, 'Success', 'Cədvələ əlavə olundu!')



#--------------------------------YEKUN-----------------------------------------

    def Yekun(self):
        # Calendardan tarixi alır
        secilmis_tarih = self.ui.calendarWidget.selectedDate().toPyDate()

        # Seçili tarixi, sorguda istifadə edilə bilən bir string formatına çevir
        secilmis_tarih_str = secilmis_tarih.strftime('%Y-%m-%d')

        # Seçili tarix üçün Mebleg cəmini əldə etmək üçün verilənlər bazasını sorğula
        query = "SELECT SUM(Mebleg) FROM mallar WHERE tarix = %s"
        values = (secilmis_tarih_str,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()

        # Sətir düzəlişində toplamı göstər
        self.ui.lineEdit_4.setText(str(int(result[0])))
#----------------------------------------------------------------------------------------------------       
       
       
        secilmis_tarih = self.ui.calendarWidget.selectedDate().toPyDate()

       
        secilmis_tarih_str = secilmis_tarih.strftime('%Y-%m-%d')

        query = "SELECT SUM(EDV) FROM mallar WHERE tarix = %s"
        values = (secilmis_tarih_str,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()

        self.ui.lineEdit_5.setText(str(int(result[0])))


#------------------------------------------------------------------------------------------------------
       
       
        secilmis_tarih = self.ui.calendarWidget.selectedDate().toPyDate()

        secilmis_tarih_str = secilmis_tarih.strftime('%Y-%m-%d')

        query = "SELECT SUM(Umumideyer) FROM mallar WHERE tarix = %s"
        values = (secilmis_tarih_str,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()

        self.ui.lineEdit_6.setText((str(result[0])))

       

#----------------------------------------DELETE-----------------------------------------------------       

    
    def Delete(self):
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'Error', 'Silmək üçün cədvəldən bir sətri seçin!')
            return
        kod = self.ui.tableWidget.item(selected_row, 0).text()
        query = f"DELETE FROM mallar WHERE Kod = '{kod}'"
        self.cursor.execute(query)
        self.mydb.commit()
        self.ui.tableWidget.removeRow(selected_row)
        QMessageBox.information(self, 'Success', 'Sətir silindi!')


#--------------------------------------SECMEK---------------------------------------------------

    def Tarix(self):
        self.ui.calendarWidget.setVisible(True)

    def Secmek(self, date):
        gun = date.day()
        ay = date.month()
        il = date.year()
        self.ui.LCD1.display(gun)
        self.ui.LCD2.display(ay)
        self.ui.LCD3.display(il)
        self.ui.calendarWidget.setVisible(False)

        query = f"SELECT * FROM mallar WHERE tarix = '{il}-{ay}-{gun}'"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.mydb.commit()
        print(data)

        for d in data:
            row_count = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row_count)

            for i in range(len(d)-1):
                if i != 0:
                    self.ui.tableWidget.setItem(row_count, i-1, QTableWidgetItem(str(d[i])))

#---------------------------------------EXPORT EXCEL-------------------------------------------------------------

      # Excele cevir
    def Excel(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export to Excel", "", "Excel Files (*.xlsx)")

        if filename:
            query = "SELECT * FROM mallar"
            self.cursor.execute(query)
            data = self.cursor.fetchall()
        
            workbook = xlsxwriter.Workbook(filename)
            worksheet = workbook.add_worksheet()
        
        row = 0
        col = 0
        
        # Write column headers
        for column_header in self.column_headers:
            worksheet.write(row, col, column_header)
            col += 1
        
        # Write data rows
        for d in data:
            row += 1
            col = 0
            for item in d:
                if isinstance(item, datetime.date):
                    item = item.strftime("%Y-%m-%d")
                worksheet.write(row, col, item)
                col += 1
        
        workbook.close()
        QMessageBox.information(self, 'Success', 'Excel faylı yaradıldı.')


#-------------------------------EXPORT PDF-------------------------------

    def PDF(self):
            query = "SELECT * FROM mallar"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows, columns=self.column_headers)

            fig, ax = plt.subplots(figsize=(12, 4))
            ax.axis('tight')
            ax.axis('off')
            the_table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')

            filename, _ = QFileDialog.getSaveFileName(self, "Export to PDF", "", "PDF Files (*.pdf)")
            if filename:
                pp = PdfPages(filename)
                pp.savefig(fig, bbox_inches='tight')
            pp.close()
            QMessageBox.information(self, 'Success', 'PDF faylı yaradıldı.')

    
#---------------------------SON--------------------------

app = QtWidgets.QApplication([])
applications = mywindow()
applications.show()
sys.exit(app.exec())
