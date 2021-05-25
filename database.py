import pymssql
import time 

class dataBase():
    """2 tane tablodan olusan database class'i. Database'e veri ekleme, veri cikarma gibi islemleri yapabileceginiz class.
    """    
    def __init__(self):
        try:
            self.conn = pymssql.connect(server='localhost', user='sa', password='MyPass@word', database='master')
            self.cursor = self.conn.cursor()
            self.createTable()
            self.isConnected = True
        except Exception:
            self.isConnected = False
    def createTable(self)->None:
        '''
            Bu fonksiyon 2 tane tablo olusturur. Ilki hasta tablosu, ikincisi istatistik tablosu.
        '''
        self.cursor.execute('''
            if not exists (select * from sysobjects where name='Hasta' and xtype='U')
            CREATE TABLE Hasta
            (
            TC nvarchar(11) NOT NULL ,
            AD nvarchar(50),
            SOYAD nvarchar(50),
            Tarih nvarchar(50),
            Saat nvarchar(50),
            Poliklinik nvarchar(50),
            Doktor nvarchar(50),
            )
        ''')
        self.cursor.execute('''
            if not exists (select * from sysobjects where name='Istatistik' and xtype='U')
            CREATE TABLE Istatistik
            (
            Doktor nvarchar(50),
            Poliklinik nvarchar(50),
            TC int NOT NULL ,
            Ad nvarchar(50),
            Soyad nvarchar(50),
            Tarih nvarchar(50),
            Saat nvarchar(50),
            Cinsiyeti nvarchar(50)
            )
        ''')
        self.conn.commit()
    
    def getDoktorlar(self)->list:
        '''
            Bu fonksiyon database'deki doktorlari ceker.
        '''
        self.cursor.execute('SELECT DISTINCT Doktor FROM HASTA')
        
        return self.cursor.fetchall()
    
    def getPoliklinikler(self)->list:
        self.cursor.execute('SELECT DISTINCT Poliklinik FROM Hasta')
        return self.cursor.fetchall()
    def randevuEkle(self,tc=str,ad=str,soyad=str,tarih=str,saat=str,poliklinik=str,doktor=str)->None: 
        '''
            Bu fonksiyon hasta tablosuna satir ekler.
        '''
        try:
            self.cursor.execute('INSERT INTO Hasta VALUES(%s, %s,%s, %s,%s, %s,%s)',(tc,ad,soyad,tarih,saat,poliklinik,doktor))
            self.conn.commit()
            return True
        except:
            return False
        
    def randevuSil(self,tc=str)->int:
        '''
            Bu fonksiyon verilen tc numarasina hasta tablosundan veri siler.
        '''
        
        # Kayit yoksa 0 donduruyor. Basarili bir sekilde calisirsa 1 donduruyor. Herhangi bir hata olursa -1 donduruyor.
        self.cursor.execute('SELECT TC FROM Hasta')
        lenTc = len(self.cursor.fetchall())
        if(lenTc == 0 ):
            return 0
        
        try:
            self.cursor.execute('DELETE FROM Hasta WHERE TC = %s',tc)
            self.conn.commit()
            return 1
        except:
            return -1
    
    def alinmisRandevular(self)->None:
        '''
            Bu fonksiyon, istatistik tablosuna veriler ekler.
        '''
        self.cursor.execute('''
        INSERT INTO Istatistik (Doktor, Poliklinik,TC, Ad, Soyad,  Tarih, Saat,  Cinsiyeti)
        VALUES
        ('XZ','Ortopedi',234,'Yusuf','Yalcin','11.05.2021','13.15','Erkek'),
        ('YZ','Dahiliye',434,'Mustafa','Gökçe','03.05.2021','13.45','Erkek')
        ''')
        self.conn.commit()
    
    def getAllPatients(self)->list:
        '''
            Database'e kayitli tum hastalari dondurur.
        '''
        self.cursor.execute('SELECT * FROM Hasta')
        return self.cursor.fetchall()
    
    def getHasta(self,date=str)->list:
        '''
            Verilen tarih degerindeki randevu saatlerini dondurur.
        '''
        self.cursor.execute('SELECT Saat FROM Hasta WHERE Tarih = %s ',date)
        return self.cursor.fetchall()
    
    def getUniqueDoctors(self,date,saat)->list:
        '''
            Verilen tarih ve saat degerlerindeki doktorlari ve calistiklari poliklinikleri dondurur.
        '''
        self.cursor.execute('SELECT Doktor,Poliklinik FROM Hasta Where Tarih = %s and Saat = %s ',(date,saat))
        return self.cursor.fetchall()
    
        

