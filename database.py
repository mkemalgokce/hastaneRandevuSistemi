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
            print("Baglanti basarili.")
        except Exception:
            print("Database'e Baglanilamadi!")
            self.isConnected = False
    def createTable(self)->None:
        '''
            Bu fonksiyon 2 tane tablo olusturur. Ilki hasta tablosu, ikincisi istatistik tablosu.
        '''
        self.cursor.execute('''
            if not exists (select * from sysobjects where name='Hasta' and xtype='U')
            CREATE TABLE Hasta
            (
            ID int IDENTITY(1,1) PRIMARY KEY,
            TC nvarchar(11) ,
            Ad nvarchar(50),
            Soyad nvarchar(50),
            Cinsiyet nvarchar(5),
            Mail nvarchar(50),
            Dogum_tarihi Date,
            )
        ''')
        self.cursor.execute('''
            if not exists (select * from sysobjects where name='Randevu' and xtype='U')
            CREATE TABLE Randevu
            (
            ID int IDENTITY(1,1),
            Tarih varchar(50),
            Saat varchar(50),
            FOREIGN KEY (ID) REFERENCES Hasta(ID)
            )
        ''')
        self.cursor.execute('''
            if not exists (select * from sysobjects where name='Poliklinikler' and xtype='U')
            CREATE TABLE Poliklinikler
            (
            ID int IDENTITY(1,1),
            Doktor nvarchar(50),
            Poliklinik nvarchar(50),
            FOREIGN KEY(ID) REFERENCES Hasta(ID)
            )
        ''')
        self.cursor.execute('''
            if not exists (select * from sysobjects where name='Istatistik' and xtype='U')
            CREATE TABLE Istatistik
            (
            ID int IDENTITY(1,1),
            Ad nvarchar(50),
            Soyad nvarchar(50),
            Cinsiyet nvarchar(50),
            Yas nvarchar(50),
            FOREIGN KEY(ID) REFERENCES Hasta(ID)
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
    
    def randevuEkle(self,tc=str,ad=str,soyad=str,tarih=str,saat=str,poliklinik=str,doktor=str,mail=str,cinsiyet=str,dogum_tarihi=str)->None: 
        '''
            Bu fonksiyon hasta tablosuna satir ekler.
        '''
        try:
            self.cursor.execute('INSERT INTO Hasta VALUES(%s, %s,%s, %s,%s, %s)',(tc,ad,soyad,cinsiyet,mail,dogum_tarihi))
            self.conn.commit()
            self.cursor.execute('INSERT INTO Randevu VALUES(%s,%s)',(tarih,saat))
            self.conn.commit()
            self.cursor.execute('INSERT INTO Poliklinikler VALUES(%s,%s)',(doktor,poliklinik))
            self.conn.commit()
            return True
        except Exception:
            return False
    def randevuSil(self,tc=str)->int:
        '''
            Bu fonksiyon verilen tc numarasina hasta tablosundan veri siler.
        '''
        
        # Kayit yoksa 0 donduruyor. Basarili bir sekilde calisirsa 1 donduruyor. Herhangi bir hata olursa -1 donduruyor.
        self.cursor.execute('SELECT TC FROM Hasta')
        lenTc = len(self.cursor.fetchall())
        if(lenTc == 0 ):
            return 0 #Hasta bulunamadi.
        
        try:
            self.cursor.execute('DELETE FROM Hasta WHERE TC = %s',tc)
            self.conn.commit()
            return 1 #Hasta silindi.
        except Exception:
            return -1 #Hata olustu, hasta silinemedi.
    
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
        self.cursor.execute('EXEC createTable')
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
        self.cursor.execute('SELECT Doktor,Poliklinik FROM Poliklinikler,Randevu Where Tarih = %s and Saat = %s ',(date,saat))
        return self.cursor.fetchall()
    
    def hastaBul(self,tc=str):
        '''
            Verilen TC degerine gore hastalarin randevu bilgilerini bulur.
        '''
        try:
            self.cursor.execute("EXEC hastaBul %s",tc)
            return self.cursor.fetchall()
        except Exception:
            return False
        
    def getUniqueTC(self,tc=str):
        self.cursor.execute('SELECT DISTINCT TC,AD,SOYAD FROM HASTA WHERE TC = %s',tc)
        tc = self.cursor.fetchall()
        return tc
    def getIstatistik(self,switch=str):
        if(switch=='doktor_siralama'):
            self.cursor.execute(''' 
                        SELECT Poliklinikler.Doktor, Count(*) as muayene_sayisi FROM Poliklinikler, Hasta
                        where Poliklinikler.ID = Hasta.ID
                        Group by Doktor
                        order by  muayene_sayisi  desc
            ''')
            return self.cursor.fethall()
        elif switch=='max_doktor':
            self.cursor.execute(''' 
                    SELECT Poliklinikler.Doktor, Count(*) as muayene_sayisi FROM Poliklinikler, Hasta
                    where Poliklinikler.ID = Hasta.ID
                    Group by Doktor
                    order by  muayene_sayisi  desc               
                                
            ''')
            return self.cursor.fetchall()
        elif switch=='toplam_hasta_sayisi':
            self.cursor.execute('SELECT  Count(*) as toplam_hasta_sayisi FROM Hasta')
            return self.cursor.fetchall()
        
        elif switch == 'toplam_erkek_sayisi':
            self.cursor.execute("SELECT  Count(*) as Erkek FROM Hasta WHERE Cinsiyet= 'Erkek' ")
            return self.cursor.fetchall()
        elif switch == 'toplam_kadin_sayisi':
            self.cursor.execute("SELECT  Count(*) as Erkek FROM Hasta WHERE Cinsiyet= 'Kadin' ")
            return self.cursor.fetchall()
            
        elif switch =='erkek_yas':
            self.cursor.execute("SELECT  AVG(DATEDIFF(YY,Dogum_tarihi,GETDATE())) as Erkek_yas_ortalamalari FROM Hasta WHERE Cinsiyet= 'Erkek'")
            return self.cursor.fetchall()
        elif switch =='kadin_yas':
            self.cursor.execute("SELECT  AVG(DATEDIFF(YY,Dogum_tarihi,GETDATE())) as Erkek_yas_ortalamalari FROM Hasta WHERE Cinsiyet= 'Kadin'")
            return self.cursor.fetchall()
        
        elif switch =='pol_gelen_hasta':
            self.cursor.execute(''' 
                        SELECT Poliklinikler.Poliklinik, Count(*) as Poliklinik_GTHS FROM Poliklinikler, Hasta
                        where Poliklinikler.ID = Hasta.id
                        Group by Poliklinik
                        order by  Poliklinik_GTHS  desc
            ''')
            return self.cursor.fetchall()
        elif switch == 'max_Poliklinik':
            self.cursor.execute('''
                Select Poliklinik from Poliklinikler
                WHERE  ID = (SELECT TOP(1) Alt_Sorgu.ID
                from(SELECT Hasta.ID, Count(*) as Poliklinik_GTHS FROM Hasta,Poliklinikler
                where Poliklinikler.ID = Hasta.ID
                Group by Hasta.ID) AS Alt_Sorgu
                order by  Poliklinik_GTHS  desc)
            ''')
            return self.cursor.fetchall()
        elif switch == 'en_yogun_gun':
            self.cursor.execute('EXEC enYogunGun')
            return self.cursor.fetchall()
        elif switch == 'hasta_gencler':
            self.cursor.execute('EXEC hastaGencler')
            return self.cursor.fetchall()
        else:
            print('Hata!')
