import sys 
from PyQt5.QtWidgets import QApplication,QWidget,QMessageBox,QMainWindow,QDateEdit,QComboBox,QDialog,QTableWidget,QTableWidgetItem,QAbstractItemView
from PyQt5 import uic
from PyQt5.QtCore import QRegExp,QEvent,Qt
from PyQt5.QtGui import QRegExpValidator
from database import dataBase

        
def mesaiSaatleri(saat=tuple)->tuple:
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

class hastaEkle(QWidget):
    '''
        Hasta bilgilerinin database'e eklendigi pencere.
    '''
    def __init__(self,parent):     
        self.saat = mesaiSaatleri([])    
        self.doktorlar = ['Doktor Seciniz.','Mehmet Uzun','Hasan Ustundag','Halil Sezai','Hamza Boynukalin']
        self.poliklinikler = ['Poliklinik Seciniz.','Dahiliye','Hariciye']                 
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
        letterValidator = QRegExpValidator(QRegExp('[a-zA-Z ]+'))   
        
        #lineEditlerin max uzakliklarini belirledik.
        self.tc_Line.setMaxLength(11)
        self.tc_Line.setValidator(numberValidator)
        
        self.ad_Line.setMaxLength(30)
        self.ad_Line.setValidator(letterValidator)
        
        self.soyad_Line.setMaxLength(30)
        self.soyad_Line.setValidator(letterValidator) 
        
        self.dateEdit.setDisplayFormat("dd.MM.yyyy")
        
        # Saatleri guncellemek icin event takibi yaptim, kullanici comboboxa tiklarsa saatler otomatik olarak guncellenecek.
        self.comboBox_AddItems('saat',self.saat)
        self.comboBox_AddItems('doktor',self.doktorlar)
        self.comboBox_AddItems('poliklinik',self.poliklinikler)

        # Comboboxlardaki tiklama eventlerini takip etmek icin bu fonksiyonlari calistirdik.
        self.comboBox_Saat.installEventFilter(self)
        self.comboBox_Doktor.installEventFilter(self) 
        self.comboBox_Poliklinik.installEventFilter(self) 
        
        
        self.hastaEkle_Btn.clicked.connect(self.add_Database)
        
        
    def eventFilter(self,target,event):
        #Eventleri duzenleyen fonksiyon, Comboboxlardaki verileri otomatik olarak duzenlemek icin kullandik.
        
        if target == self.comboBox_Saat and event.type() == QEvent.MouseButtonPress:
            #Kullanici Saat comboBox'una tiklarsa bu event calisiyor.
            self.update()
        if target == self.comboBox_Poliklinik and event.type() == QEvent.MouseButtonPress:
            #Kullanici Poliklinik comboBox'una tiklarsa bu event calisiyor.
            saat = self.comboBox_Saat.currentText()
            tarih = self.dateEdit.date().toString("dd.MM.yyyy")
            
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
            tarih = self.dateEdit.date().toString("dd.MM.yyyy")
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
        tarih = self.dateEdit.date().toString("dd.MM.yyyy")
        doluSaatler = []
        self.saat = mesaiSaatleri(self.saat)
        for i in range(0,len(self.saat)):
            if(len(self.parent.database.getUniqueDoctors(tarih,self.saat[i])) == 4):
                doluSaatler.append(self.saat[i])
        print('Dolu Saatler : ' , doluSaatler)        
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
        tarih =  self.dateEdit.date().toString("dd.MM.yyyy")
        
        if(ad == '' or soyad == '' or tc == '' or doktor == 'Doktor Seciniz.' or poliklinik == 'Poliklinik Seciniz.' or saat == 'Saat Seciniz.'):
            self.errorBox('Lutfen tum alanlari eksiksiz doldurunuz!')

        elif(len(tc)<11):
            self.errorBox("Lutfen TC'nizi dogru giriniz!")
        
        else:
            if(not self.parent.database.randevuEkle(tc,ad,soyad,tarih,saat,poliklinik,doktor)):
                self.errorBox('Hasta eklenemedi!')
            else:
                self.errorBox('Islem tamamlandi.')
                self.parent.updateTable()
                
        self.update()
    def errorBox(self,hataMesaji=str)->None:
        """[Ekrana hata mesaji yansitir.]

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
        self.delDialog= QDialog()
        uic.loadUi('Uis/hastaSil.ui',self.delDialog)
        numberValidator = QRegExpValidator(QRegExp('[0-9]+'))
        self.delDialog.tc_lineEdit.setMaxLength(11)
        self.delDialog.tc_lineEdit.setValidator(numberValidator)
        self.delDialog.show()
        self.delDialog.onayla_Btn.clicked.connect(self.del_Btn_Func)
        
    def del_Btn_Func(self)->None:
        '''
            Hasta silme butonunun fonksiyonu
        '''
        tc = self.delDialog.tc_lineEdit.text()
        if(len(tc)<11):
            self.errorBox('Hatali TC girdiniz !').show()
            
        else:
            if(self.database.randevuSil(tc= tc) == 1):
                self.errorBox('Kayit Silindi .').show()
                self.updateTable()
            
            elif(self.database.randevuSil(tc= tc) == -1):
                self.errorBox('Hata Olustu !').show()
            else:
                self.errorBox('Kayit Bulunamadi !').show()

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
            self.hastaTable.setItem(row , 0 , QTableWidgetItem(str(hasta[0])))
            self.hastaTable.setItem(row , 1 , QTableWidgetItem(hasta[1]+' ' + hasta[2]))
            self.hastaTable.setItem(row , 2 , QTableWidgetItem(hasta[3]))
            self.hastaTable.setItem(row , 3 , QTableWidgetItem(hasta[4]))
            self.hastaTable.setItem(row , 4 , QTableWidgetItem(str(hasta[5])))
            self.hastaTable.setItem(row , 5 , QTableWidgetItem(str(hasta[6])))
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



             