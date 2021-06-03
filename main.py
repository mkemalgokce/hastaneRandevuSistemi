import sys 
from PyQt5.QtWidgets import QApplication,QWidget,QMessageBox,QMainWindow,QDateEdit,QComboBox,QDialog,QTableWidget,QTableWidgetItem,QAbstractItemView
from PyQt5 import uic
from PyQt5.QtCore import QRegExp,QEvent,Qt
from PyQt5.QtGui import QRegExpValidator,QPixmap
from database import dataBase
import matplotlib.pyplot as plt
from functools import partial
import re
import smtplib
from fpdf import FPDF
import subprocess

def createPDF(msg=str)->None:
    '''
        Bu fonksiyon verilen string degerini pdf'e ekler.
    '''
    pdf = FPDF()
  
    # Yeni sayfa olusturuyor.
    pdf.add_page()
    
    # Pdf'in fontunu ve buyuklugunu belirledik.
    pdf.set_font("Arial", size = 20)
    
    # create a cell
    pdf.cell(150, 10, txt = 'Hastane Randevu Sistemi\n', 
            ln = 1, align = 'C')
    # 
    pdf.set_font("Arial", size = 8)
    msg = msg.split('\n')
    lenMsg = len(msg)
    for i in range(0,lenMsg):
        pdf.cell(150, 20+2*i, txt = msg[i], 
            ln = 1, align = 'L')
    
    
    # PDF' i saveledik.
    pdf.output("hastanerandevu.pdf")  
    
    # PDF'i actik.
    subprocess.Popen('open %s' % 'hastanerandevu.pdf', shell=True)

    
def checkMail(email=str)->bool:
    '''Kullanicinin girdigi email formatinin dogru olup olmadigini kontrol eden fonksiyon.'''
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if(re.search(regex, email)):
        return True
 
    else:
        return False
        
def mesaiSaatleri(saat=list)->list:
    '''Mesai saatlerini saat degiskenine atar.'''
    saat = ['Saat Seciniz.']
    
    for i in range(9):
            for j in range(4):
                if(i==3):
                    continue
                if(i==0):
                    saatStr = '0'+str(i+9)+'.'+str(j*15)+'0'
                    saat.append(saatStr[:5])
                else:
                    saatStr = str(i+9)+'.'+str(j*15)+'0'
                    saat.append(saatStr[:5])
    return saat    

def sendMail(target=str,mailMessage=str)->None:
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('hastanerandevusistemi10@gmail.com','hastanerandevU3')
    server.sendmail('hastanerandevu10@gmail.com',target,mailMessage)
    server.quit()
    
class hastaEkle(QWidget):
    '''
        Hasta bilgilerinin database'e eklendigi pencere.
    '''
    def __init__(self,parent):     
        self.saat = mesaiSaatleri([])    
        self.doktorlar = ['Doktor Seciniz.','Mehmet Uzun','Hasan Ustundag','Halil Sezai','Hamza Boynukalin']
        self.poliklinikler = ['Poliklinik Seciniz.','Dahiliye','Ortopedi']                 
        super().__init__()
        self.init_Ui()
        self.parent = parent
        self.update()  
    def init_Ui(self)->None:
        '''
            Ui initializer
        '''
        uic.loadUi('Uis/hasta.ui',self)
        #Validator atayarak lineEditlere rakam/harf girislerini engelledik.
        
        numberValidator = QRegExpValidator(QRegExp('[0-9]+'))
        letterValidator = QRegExpValidator(QRegExp('[a-zA-Z üÜöÖğĞçÇİşŞ]+'))   
        
        #lineEditlerin max uzakliklarini belirledik.
        self.tc_Line.setMaxLength(11)
        self.tc_Line.setValidator(numberValidator)
        
        self.ad_Line.setMaxLength(30)
        self.ad_Line.setValidator(letterValidator)
        
        self.soyad_Line.setMaxLength(30)
        self.soyad_Line.setValidator(letterValidator) 
        
        
        # Saatleri guncellemek icin event takibi yaptim, kullanici comboboxa tiklarsa saatler otomatik olarak guncellenecek.
        self.comboBox_AddItems('saat',self.saat)
        self.comboBox_AddItems('doktor',self.doktorlar)
        self.comboBox_AddItems('poliklinik',self.poliklinikler)

        # Comboboxlardaki tiklama eventlerini takip etmek icin bu fonksiyonlari calistirdik.
        self.comboBox_Saat.installEventFilter(self)
        self.comboBox_Doktor.installEventFilter(self) 
        self.comboBox_Poliklinik.installEventFilter(self) 
        
        
        self.hastaEkle_Btn.clicked.connect(self.add_Database)
        
        
    def eventFilter(self,target,event)->bool:
        #Eventleri duzenleyen fonksiyon, Comboboxlardaki verileri otomatik olarak duzenlemek icin kullandik.
        
        if target == self.comboBox_Saat and event.type() == QEvent.MouseButtonPress:
            #Kullanici Saat comboBox'una tiklarsa bu event calisiyor.
            self.update()
        if target == self.comboBox_Poliklinik and event.type() == QEvent.MouseButtonPress:
            #Kullanici Poliklinik comboBox'una tiklarsa bu event calisiyor.
            saat = self.comboBox_Saat.currentText()
            tarih = self.rt_dateEdit.date().toString("dd.MM.yyyy")
            
            if(saat != 'Saat Seciniz.'):
                datas = self.parent.database.getUniqueDoctors(tarih,saat)
                
                if len(datas) ==2 : # Veriler
                    if(datas[0][1] == datas[1][1]):
                        pol = self.poliklinikler.copy()
                        pol.remove(datas[0][1])
                        self.comboBox_AddItems('poliklinik',pol)
                        
                elif len(datas) ==3 :
                    if(datas[0][1] == datas[1][1] or datas[1][1] == datas[2][1]):
                        pol = self.poliklinikler.copy()
                        pol.remove(datas[1][1])
                        self.comboBox_AddItems('poliklinik',pol)
                    
        if target == self.comboBox_Doktor and event.type() == QEvent.MouseButtonPress:
            #Kullanici Doktor comboBox'una tiklarsa bu event calisiyor.
            saat = self.comboBox_Saat.currentText()
            tarih = self.rt_dateEdit.date().toString("dd.MM.yyyy")
            if(saat != 'Saat Seciniz.'):
                datas = self.parent.database.getUniqueDoctors(tarih,saat)
                if(self.comboBox_Poliklinik.currentText()==self.poliklinikler[1]):
                    dok = self.doktorlar.copy()[:3]
                    for i in range(len(datas)):
                        if(self.doktorlar[1] == datas[i][0]):
                            dok.remove(datas[i][0])
                        elif(self.doktorlar[2] == datas[i][0]):
                            dok.remove(datas[i][0])
                    self.comboBox_AddItems('doktor',dok)
                
                elif(self.comboBox_Poliklinik.currentText()==self.poliklinikler[2]):
                    dok = [self.doktorlar[0]]+self.doktorlar.copy()[3:] 
                    for i in range(len(datas)):
                        if(self.doktorlar[3] == datas[i][0]):
                            dok.remove(datas[i][0])
                        elif(self.doktorlar[4] == datas[i][0]):
                            dok.remove(datas[i][0])
                    self.comboBox_AddItems('doktor',dok)
        return False   
      
    def comboBox_AddItems(self,switch=str,data=list)->None:
        '''
            Comboboxlara degerler eklememizi/ degerleri guncellememizi saglayan fonksiyon.
        '''
        if switch == 'saat' :
            self.comboBox_Saat.clear()
            for i in range(len(data)):
                self.comboBox_Saat.addItem(data[i])
            self.comboBox_Saat.setCurrentIndex(0)
            self.comboBox_Saat.model().item(0).setEnabled(False)
        elif switch == 'doktor':
            self.comboBox_Doktor.clear()
            for i in range(len(data)):
                self.comboBox_Doktor.addItem(data[i])
            self.comboBox_Doktor.setCurrentIndex(0)
            self.comboBox_Doktor.model().item(0).setEnabled(False)
        elif switch == 'poliklinik':
            self.comboBox_Poliklinik.clear()
            for i in range(len(data)):
                self.comboBox_Poliklinik.addItem(data[i])
            self.comboBox_Poliklinik.setCurrentIndex(0)
            self.comboBox_Poliklinik.model().item(0).setEnabled(False)
            
    def update(self)->None:
        '''
            Bu fonksiyon database'deki degerlere gore hasta ekleme pencerisini gunceller.
        '''
        tarih = self.rt_dateEdit.date().toString("dd.MM.yyyy")
        doluSaatler = []
        self.saat = mesaiSaatleri(self.saat)
        for i in range(0,len(self.saat)):    
            if(len(self.parent.database.getUniqueDoctors(tarih,self.saat[i])) == 4):
                doluSaatler.append(self.saat[i])
        
        if len(doluSaatler)!= 0 :
            for x in doluSaatler:
                self.saat.remove(x)
        self.comboBox_AddItems('saat',self.saat)
        self.comboBox_AddItems('doktor',self.doktorlar)
        self.comboBox_AddItems('poliklinik',self.poliklinikler)
        
    def add_Database(self)->None:
        '''
            Bu fonksiyon pencerede girilen degerleri database'e ekler.
        '''
        ad = self.ad_Line.text()
        soyad = self.soyad_Line.text()
        tc = self.tc_Line.text()
        doktor = self.comboBox_Doktor.currentText()
        poliklinik = self.comboBox_Poliklinik.currentText()
        saat = self.comboBox_Saat.currentText()
        tarih =  self.rt_dateEdit.date().toString("dd.MM.yyyy")
        cinsiyet = self.comboBox_Cinsiyet.currentText()
        dogum_tarihi = self.dt_dateEdit.date().toString("MM.dd.yyyy")
        mail = self.mail_Line.text()
        uniquePatiens = self.parent.database.getUniqueTC(tc)
        print(uniquePatiens)
        if(mail=='' or ad == '' or soyad == '' or tc == '' or doktor == 'Doktor Seciniz.' or poliklinik == 'Poliklinik Seciniz.' or saat == 'Saat Seciniz.'):
            print('a')
            self.errorBox('Lutfen tum alanlari eksiksiz doldurunuz!')

        elif(len(tc)<11):
            self.errorBox("Lutfen TC'nizi dogru giriniz!")
        
        elif len(uniquePatiens) != 0 and uniquePatiens[0][1] != ad and uniquePatiens[0][1] != soyad :
            self.errorBox('Sistemde bu TC ile kaydedilmis baska bir kayit var !')
        elif not checkMail(mail):
            self.errorBox('Hatali mail adresi!')
        else:
            if(not self.parent.database.randevuEkle(tc,ad,soyad,tarih,saat,poliklinik,doktor,mail,cinsiyet,dogum_tarihi)):
                self.errorBox('Hasta eklenemedi!')
            else:
                self.errorBox('Islem tamamlandi.')
                sendMail(target=mail,mailMessage ='''Subject: Hastane Randevu\n\n
                Randevunuz basariyla olusturuldu.
                -----------------------------------------------------------------
                
                    Randevu Bilgileri
                    -------------------------
                    
                         Ad-soyad : {ad} {soyad}

                         Randevu tarihi : {tarih}

                         Randevu saati : {saat}

                         Poliklinik : {poliklinik}

                         Doktor : {doktor}
                    
                '''.format(ad=ad,soyad=soyad,tarih=tarih,saat=saat,poliklinik=poliklinik,doktor=doktor))
                
                self.parent.updateTable()
                
        self.update()
        
    def errorBox(self,hataMesaji=str)->None:
        """[Ekrana hata mesaji yansitir.]s

        Args:
            hataMesaji ([string], optional): [Ekranda gosterilecek hata mesaji]. Defaults to str.
        """        
        errorBox= QMessageBox(self)
        errorBox.setStyleSheet('background-color: rgb(255, 255, 255);color:(100,100,100);')
        errorBox.setText(hataMesaji)
        errorBox.show()     
        
        
    
class mainApp(QMainWindow):
    '''
        Ana uygulamanin classi. Tablo, randevu ekleme, randevu silme ve istatistik gibi alanlara sahip.
    '''
    def __init__(self):             
        super().__init__()
        self.database = dataBase()
        if(self.database.isConnected == True):
            self.show()
            uic.loadUi('Uis/main.ui',self)
            self.updateTable()
            self.add_Btn.clicked.connect(self.addFunc)
            self.del_Btn.clicked.connect(self.delFunc)
            self.stat_Btn.clicked.connect(self.istatistikFunc)
            self.yazdir_Btn.clicked.connect(self.yazdirFunc)
            
        else:
            self.database_ErrorBox = self.errorBox("Database'e baglanilamadi.")
            self.database_ErrorBox.show()
            
        
    def addFunc(self)->None:
        '''
            Hasta ekleme pencerisini acar.
        '''
        self.hastaEkle = hastaEkle(self)
        self.hastaEkle.show()
       
    def delFunc(self)->None:
        '''
            Hasta silme penceresini acar.
        '''
        saatList = []
        saatList = mesaiSaatleri(saatList)
        self.delW= QWidget()
        uic.loadUi('Uis/hastaSil.ui',self.delW)
        numberValidator = QRegExpValidator(QRegExp('[0-9]+'))
        self.delW.tc_lineEdit.setMaxLength(11)
        self.delW.tc_lineEdit.setValidator(numberValidator)
        self.delW.saat_comboBox.addItems(saatList)
        self.delW.show()
        self.delW.onayla_Btn.clicked.connect(self.del_Btn_Func)
        
    def istatistikFunc(self)->None:
        '''
            Istatistik pencereini acar, oradaki degerleri database'den ceker.
        '''
        
        self.istatistikW = QWidget()
        uic.loadUi('Uis/istatistik.ui',self.istatistikW)
        
        
        #Databaseden verileri cekerek, onlari degiskenlere atayan kisim.
        toplamHasta = self.database.getIstatistik('toplam_hasta_sayisi')[0][0]
        toplamErkek = self.database.getIstatistik('toplam_erkek_sayisi')[0][0]
        toplamKadin = self.database.getIstatistik('toplam_kadin_sayisi')[0][0]
        erkekYas = self.database.getIstatistik('erkek_yas')[0][0]
        kadinYas = self.database.getIstatistik('kadin_yas')[0][0]
        pol_dahiliye_Hastalar = self.database.getIstatistik('dahiliye_gelen_hasta')
        pol_ortopedi_Hastalar = self.database.getIstatistik('ortopedi_gelen_hasta')
        # kadinYas = self.database.getIstatistik('kadin_yas')[0][0]
        en_yogun_gun = self.database.getIstatistik('en_yogun_gun')[0][0]
        hasta_gencler = self.database.getIstatistik('hasta_gencler')[0][0]
        maxDoktor = self.database.getIstatistik('max_doktor')[0][0]
        
        # #Degiskenleri arayuzdeki labellara atayan kisim.
        self.istatistikW.toplamHasta_label.setText(str(toplamHasta))
        self.istatistikW.toplamErkek_label.setText(str(toplamErkek))
        self.istatistikW.toplamKadin_label.setText(str(toplamKadin))
        self.istatistikW.avgErkek_label.setText(str(erkekYas))
        self.istatistikW.avgKadin_label.setText(str(kadinYas))
        self.istatistikW.maxPol1_label.setText(str(pol_dahiliye_Hastalar[0]))
        self.istatistikW.maxPol2_label.setText(str(pol_ortopedi_Hastalar[0]))
        self.istatistikW.eyg_label.setText(str(en_yogun_gun))
        self.istatistikW.hastaGencler_label.setText(str(hasta_gencler))
        self.istatistikW.maxDoktor_label.setText(str(maxDoktor))
        
        #Grafiklerin olusturulmasi
        plt.style.use('ggplot')
        fig = plt.figure(figsize=(2.2,2.2))
        fig.patch.set_facecolor([67/255, 67/255, 152/255])
        plt.pie([toplamErkek,toplamKadin],autopct='%1.1f%%',shadow=True, labels=['Erkek','Kadin'],textprops={'fontsize': 8})
        plt.title('Toplam Hasta Dagilimi',fontsize=8)
        plt.savefig('Grafikler/gr1.png', bbox_inches='tight')
        
        fig = plt.figure(figsize=(2.2,2.2))
        fig.patch.set_facecolor([67/255, 67/255, 152/255])
        plt.pie([pol_dahiliye_Hastalar[0],pol_ortopedi_Hastalar[0]],autopct='%1.1f%%',shadow=True, labels=['Dahiliye','Ortopedi'],textprops={'fontsize': 8})
        plt.title('Polikliniklerin Oranlari',fontsize=8)
        plt.savefig('Grafikler/gr2.png', bbox_inches='tight')
        
        # Grafiklerin pencereye yerlestirilmesi
        pixmap1 = QPixmap('Grafikler/gr1.png')
        self.istatistikW.gr1_label.setPixmap(pixmap1)
        pixmap2 = QPixmap('Grafikler/gr2.png')
        self.istatistikW.gr2_label.setPixmap(pixmap2)
        # Tabloya verilerin yerlestirilmesi
        self.updateIstatistikTable()
        self.istatistikW.show()

        
    def updateIstatistikTable(self)->None:
        '''
            Bu fonksiyon istatistik tablosunu gunceller.
        '''
        istatistikler = self.database.getIstatistikValues()
        print(istatistikler)
        row = 0
        self.istatistikW.istatistik_tableWidget.setRowCount(len(istatistikler)) 
        self.istatistikW.istatistik_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.istatistikW.istatistik_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        for istatistik in istatistikler:
            self.istatistikW.istatistik_tableWidget.setItem(row , 0 , QTableWidgetItem(str(istatistik[1])+' ' +str(istatistik[2])))
            self.istatistikW.istatistik_tableWidget.setItem(row , 1 , QTableWidgetItem(str(istatistik[3])))
            self.istatistikW.istatistik_tableWidget.setItem(row , 2 , QTableWidgetItem(str(istatistik[4])))
            self.istatistikW.istatistik_tableWidget.setItem(row , 3 , QTableWidgetItem(str(istatistik[5])))
            self.istatistikW.istatistik_tableWidget.setItem(row , 4 , QTableWidgetItem(str(istatistik[6])))
            for i in range(4):
                item = self.istatistikW.istatistik_tableWidget.item(row, i)
                item.setTextAlignment(Qt.AlignCenter)
            row+=1
            
    def del_Btn_Func(self)->None:
        '''
            Hasta silme butonunun fonksiyonu
        '''
        tc = self.delW.tc_lineEdit.text()
        tarih = self.delW.tarih_dateEdit.date().toString("dd.MM.yyyy")
        saat = self.delW.saat_comboBox.currentText()
        if(len(tc)<11):
            self.errorBox('Hatali TC girdiniz !').show()
            
        else:
            if(self.database.randevuSil(tc,tarih,saat)):
                self.errorBox('Kayit Silindi .').show()
                self.updateTable()
            else:
                self.errorBox('Hata Olustu!').show()
            
            


    def updateTable(self)->None:
        '''
            Ana penceredeki tabloyu guncelleyen fonksiyon.
        '''
        hastalar = self.database.getAllPatients()   
        row = 0
        self.hastaTable.setRowCount(len(hastalar)) 
        self.hastaTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.hastaTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        for hasta in hastalar:
            self.hastaTable.setItem(row , 0 , QTableWidgetItem(str(hasta[1])))
            self.hastaTable.setItem(row , 1 , QTableWidgetItem(hasta[2]))
            self.hastaTable.setItem(row , 2 , QTableWidgetItem(hasta[5]))
            self.hastaTable.setItem(row , 3 , QTableWidgetItem(hasta[6]))
            self.hastaTable.setItem(row , 4 , QTableWidgetItem(str(hasta[4])))
            self.hastaTable.setItem(row , 5 , QTableWidgetItem(str(hasta[3])))
            for i in range(6):
                item = self.hastaTable.item(row, i)
                item.setTextAlignment(Qt.AlignCenter)
            row+=1

    def errorBox(self,hataMesaji=str)->QMessageBox:
        """[Ekrana hata mesaji yansitir.]

        Args:
            hataMesaji ([string], optional): [Ekranda gosterilecek hata mesaji]. Defaults to str.
        """        
        errorBox= QMessageBox(self)
        errorBox.setStyleSheet('background-color: rgb(255, 255, 255);')
        errorBox.setText(hataMesaji)
        return errorBox

    def yazdirFunc(self):
        '''
            Bu fonksiyon verileri bir stringe ekler ve onlari createPdf fonksiyonuna yollar.
        '''
        msg = ''
        for i in range(0,len(self.database.getAllPatients())):
            msg += 'TC: '+str(self.database.getAllPatients()[i][1])+' | '
            msg += 'AD-Soyad: '+str(self.database.getAllPatients()[i][2])+' | '
            msg +='Tarih: '+str(self.database.getAllPatients()[i][5])+' | '
            msg += 'Saat: '+str(self.database.getAllPatients()[i][6])+' | '
            msg += 'Poliklinik: '+str(self.database.getAllPatients()[i][4])+' | '
            msg += 'Doktor: '+str(self.database.getAllPatients()[i][3])+'\n'
        print(msg)   
        createPDF(msg)
app = QApplication(sys.argv)
demo = mainApp()
demo.show()
try:
    sys.exit(app.exec_())
except SystemExit:
    print('Closing Window')