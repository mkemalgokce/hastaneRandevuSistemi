import pymssql

class dataBase():
    def __init__(self):
        self.conn = pymssql.connect(server='localhost', user='sa', password='MyPass@word', database='master')
        self.cursor = self.conn.cursor()
        self.createTable()
        
    def createTable(self)->None:
        '''
            Bu fonksiyon 2 tane tablo olusturur. Ilki hasta tablosu, ikincisi istatistik tablosu.
        '''
        self.cursor.execute('''
            if not exists (select * from sysobjects where name='Hasta' and xtype='U')
            CREATE TABLE Hasta
            (
            TC int NOT NULL PRIMARY KEY,
            AD nvarchar(50),
            SOYAD nvarchar(50),
            Tarih nvarchar(50),
            Saat nvarchar(50),
            Poliklinik nvarchar(50),
            Doktor nvarchar(50),
            Cinsiyeti nvarchar(50)
            )
        ''')
        self.cursor.execute('''
            if not exists (select * from sysobjects where name='Istatistik' and xtype='U')
            CREATE TABLE Istatistik
            (
            Doktor nvarchar(50),
            Poliklinik nvarchar(50),
            TC int NOT NULL Primary KEY,
            Ad nvarchar(50),
            Soyad nvarchar(50),
            Tarih nvarchar(50),
            Saat nvarchar(50),
            Cinsiyeti nvarchar(50)
            )
        ''')
        self.conn.commit()
    
    def randevuEkle(self,tc=int,ad=str,soyad=str,tarih=str,saat=str,poliklinik=str,doktor=str,cinsiyet=str)->None: 
        '''
            Bu fonksiyon hasta tablosuna satir ekler.
        '''
        self.cursor.execute('INSERT INTO Hasta VALUES(%s, %s,%s, %s,%s, %s,%s, %s)',(tc,ad,soyad,tarih,saat,poliklinik,doktor,cinsiyet))
        self.conn.commit()
        
    def randevuSil(self,tc=int)->None:
        '''
            Bu fonksiyon verilen tc numarasina hasta tablosundan veri siler.
        '''
        self.cursor.execute('DELETE FROM Hasta WHERE TC = %s',tc)
        self.conn.commit()
    
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
    
m = dataBase()
m.randevuEkle(103,'Kemal','s2','sa','asds','sd','sda','asds')



