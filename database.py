import pymssql
import time 

class dataBase():
    """2 tane tablodan olusan database class'i. Database'e veri ekleme, veri cikarma gibi islemleri yapabileceginiz class.
    """    
    def __init__(self):
        #try:
        self.conn = pymssql.connect(server='localhost', user='sa', password='MyPass@word', database='master')
        self.cursor = self.conn.cursor()
        #self.createTrigger()
        self.createTable()
        self.createProcedure()
        self.isConnected = True
        print("Baglanti basarili.")
        # except Exception:
        #     print("Database'e Baglanilamadi!")
        #     self.isConnected = False
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
            Dogum_tarihi Date
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
            if exists (select * from sysobjects where name='Istatistik' and xtype='U')
            DROP TABLE Istatistik
            if not exists (select * from sysobjects where name='Istatistik' and xtype='U')
            CREATE TABLE Istatistik
            (
            Istatistik_ID int IDENTITY(1,1),
            Ad nvarchar(50),
            Soyad nvarchar(50),
            Tarih varchar(50),
            Saat varchar(50),
            Dogum_tarihi Date,
            Cinsiyet nvarchar(50),
            Doktor nvarchar(50)
            )
            INSERT INTO Istatistik (Ad, Soyad, Tarih, Saat,Dogum_tarihi, Cinsiyet, Doktor)
            VALUES
            ('Yusuf','Yalcin','24.05.2021','09.00','01.04.2000','Erkek','Mehmet Uzun'),
            ('Busranur','Atilgan','24.05.2021','09.15','11.07.2000','Kadin','Hasan Ustundag'),
            ('Cengiz','Altay','24.05.2021','09.30','01.03.1981','Erkek','Hamza Boynukalin'),
            ('Filiz','Hantal','24.05.2021','10.00','10.10.2007','Kadin','Mehmet Uzun'),
            ('Rumeysa','Kaya','24.05.2021','10.15','11.29.1997','Kadin','Mehmet Uzun'), 
            ('Bahadir','Hacioglu','24.05.2021','10.30','12.17.1980','Erkek','Halil Sezai'),
            ('Mucahit','Dogan','24.05.2021','10.45','09.22.1972','Erkek','Hamza Boynukalin'), 
            ('Olcay','El','24.05.2021','11.00','10.06.1991','Erkek','Mehmet Uzun'),
            ('Elif','Salihoglu','24.05.2021','11.30','08.27.1998','Kadin','Mehmet Uzun'), 
            ('Melisa','Isik','24.05.2021','11.45','12.13.1980','Kadin','Halil Sezai'),
            ('Yasin','Kuru','24.05.2021','13.00','03.19.1982','Erkek','Hamza Boynukalin'), 
            ('Huseyin','Kuzu','24.05.2021','13.15','12.19.2020','Erkek','Mehmet Uzun'), 
            ('Burhan','Ucar','24.05.2021','13.30','08.10.1989','Erkek','Hasan Ustundag'), 
            ('Seyyit Muhammed','Mengec','24.05.2021','13.45','10.04.1996','Erkek','Mehmet Uzun'),
            ('Adem','Bayak','24.05.2021','14.00','07.16.1964','Erkek','Hamza Boynukalin'), 
            ('Halil','Kucuk','24.05.2021','14.15','02.02.1992','Erkek','Mehmet Uzun'), 
            ('Hakan','Acik','24.05.2021','14.30','05.01.2021','Erkek','Hasan Ustundag'), 
            ('Yagmur','Ruzgar','24.05.2021','14.45','01.21.2005','Kadin','Mehmet Uzun'),
            ('Serif','Kara','24.05.2021','15.00','06.02.1997','Erkek','Hamza Boynukalin'), 
            ('Kubra','Ozer','24.05.2021','15.15','06.18.1991','Kadin','Hasan Ustundag'), 
            ('Omer','Kara','24.05.2021','15.30','10.04.1966','Erkek','Hasan Ustundag'),
            ('Fuat','Duran','24.05.2021','16.00','01.12.1990','Erkek','Halil Sezai'), 
            ('Ibrahim','Tufek','25.05.2021','09.30','03.07.2000','Erkek','Hasan Ustundag'), 
            ('Yasin','Guler','25.05.2021','09.45','02.28.1985','Erkek','Hamza Boynukalin'), 
            ('Burak','Ak','25.05.2021','10.00','08.16.1955','Erkek','Mehmet Uzun'), 
            ('Betul','Sevinc','25.05.2021','10.15','05.23.1997','Kadin','Hasan Ustundag'), 
            ('Tugce','Coban','25.05.2021','11.00','01.01.1989','Kadin','Hasan Ustundag'), 
            ('Ali','Divlim','25.05.2021','11.30','11.10.2002','Erkek','Hasan Ustundag'), 
            ('Seyma','Tak','25.05.2021','13.00','08.22.1991','Kadin','Halil Sezai'),
            ('Busra','Cevik','25.05.2021','13.30','06.12.1998','Kadin','Hamza Boynukalin'), 
            ('Sinem','Yilmaz','25.05.2021','14.00','03.31.1977','Kadin','Hasan Ustundag'), 
            ('Samet','Turan','25.05.2021','14.15','11.22.1993','Erkek','Mehmet Uzun'), 
            ('Mustafa','Bahar','25.05.2021','15.00','10.09.1960','Erkek','Hasan Ustundag'),
            ('Hulya','Asici','25.05.2021','15.30','01.19.1950','Kadin','Halil Sezai'), 
            ('Habil','Duzgun','25.05.2021','16.00','09.28.1988','Erkek','Hasan Ustundag'),
            ('Busra','Kara','25.05.2021','16.30','05.31.1998','Kadin','Hasan Ustundag'),
            ('Arif','Dagistan','26.05.2021','09.00','09.10.1977','Erkek','Hamza Boynukalin'), 
            ('Erhan','Hacioglu','26.05.2021','09.15','11.22.1955','Erkek','Hasan Ustundag'),
            ('Rahmi','Dogru','26.05.2021','09.30','12.17.1988','Erkek','Mehmet Uzun'), 
            ('Huseyin','Gurel','26.05.2021','09.45','01.01.1980','Erkek','Halil Sezai'),
            ('Ahmet','Manav','26.05.2021','10.00','10.30.1971','Erkek','Halil Sezai'), 
            ('Berfin','Sevgi','26.05.2021','10.15','12.19.1999','Kadin','Halil Sezai'),
            ('Ahmet','Kadayif','26.05.2021','10.30','03.27.1986','Erkek','Hasan Ustundag'),
            ('Mehmet','Guz','26.05.2021','10.45','10.03.1998','Erkek','Hamza Boynukalin'),
            ('Deniz','Bitir','26.05.2021','11.00','02.28.1995','Erkek','Halil Sezai'),
            ('Hakime','Yol','26.05.2021','11.15','12.10.2001','Kadin','Halil Sezai'),
            ('Nazli','Getir','26.05.2021','11.30','09.15.2003','Kadin','Hamza Boynukalin'),
            ('Amine','Sakir','26.05.2021','11.45','02.04.1990','Kadin','Halil Sezai'),
            ('Huseyin','Biter','26.05.2021','13.00','12.19.2004','Erkek','Hasan Ustundag'),
            ('Galip','Bulbul','26.05.2021','13.15','11.11.2002','Erkek','Halil Sezai'),
            ('Ali','Saray','26.05.2021','13.30','10.07.1994','Erkek','Mehmet Uzun'),
            ('Feyyaz','Tiken','26.05.2021','13.45','01.02.1996','Erkek','Hasan Ustundag'),
            ('Ebru','Baris','26.05.2021','14.00','05.06.1990','Kadin','Hasan Ustundag'),
            ('Halime','Gunoya','26.05.2021','14.15','12.23.1988','Kadin','Hamza Boynukalin'),
            ('Cihat','Genc','26.05.2021','14.30','11.18.2011','Erkek','Hasan Ustundag'),
            ('Ahmet','Kinali','26.05.2021','15.00','10.26.2009','Erkek','Hamza Boynukalin'), 
            ('Mucahit','Seyrek','26.05.2021','15.15','01.22.1994','Erkek','Mehmet Uzun'), 
            ('Kader','Uyar','26.05.2021','16.00','03.27.1965','Kadin','Hamza Boynukalin'), 
            ('Merve','Akbaba','27.05.2021','09.15','04.20.1997','Kadin','Hamza Boynukalin'), 
            ('Yilmaz','Sonmez','27.05.2021','09.30','11.17.1990','Erkek','Hamza Boynukalin'), 
            ('Recep','Yalcin','27.05.2021','09.45','01.02.1952','Erkek','Hasan Ustundag'), 
            ('Guven','Elmas','27.05.2021','10.00','05.18.1997','Erkek','Hamza Boynukalin'), 
            ('Mahir','Akyol','27.05.2021','10.30','09.05.1974','Erkek','Hamza Boynukalin'), 
            ('Onur Can','Sen','27.05.2021','10.45','01.27.1999','Erkek','Mehmet Uzun'), 
            ('Osman','Koca','27.05.2021','11.00','02.22.1973','Erkek','Hamza Boynukalin'), 
            ('Fatih','Bayram','27.05.2021','11.15','12.30.1999','Erkek','Hasan Ustundag'),
            ('Hakan','Demir','27.05.2021','11.30','01.06.1980','Erkek','Halil Sezai'),
            ('Esra','Arslan','27.05.2021','11.45','04.15.1986','Kadin','Hamza Boynukalin'),
            ('Muslum','Topal','27.05.2021','13.30','12.31.1995','Erkek','Mehmet Uzun'),
            ('Serdar','Cetinkaya','27.05.2021','13.45','10.18.1973','Erkek','Hamza Boynukalin'),
            ('Gulay','Boyraz','27.05.2021','14.00','08.25.1970','Kadin','Hamza Boynukalin'),
            ('Mehmet','Koc','27.05.2021','14.30','07.07.2006','Erkek','Hamza Boynukalin'),
            ('Osman Nuri','Bildirici','27.05.2021','14.45','11.16.2000','Erkek','Halil Sezai'), 
            ('Metin','Ahu','27.05.2021','15.00','01.26.1977','Erkek','Hasan Ustundag'), 
            ('Ayse','Temiz','27.05.2021','15.15','01.01.1991','Kadin','Mehmet Uzun'), 
            ('Omer','Kilic','27.05.2021','15.30','08.08.1984','Erkek','Hamza Boynukalin'), 
            ('Berat','Olmez','27.05.2021','16.00','11.06.1990','Erkek','Hamza Boynukalin'), 
            ('Ufuk','Sakar','27.05.2021','16.15','03.18.1995','Erkek','Hasan Ustundag'), 
            ('Ugur','Aydi','27.05.2021','16.30','06.18.1996','Erkek','Hamza Boynukalin'), 
            ('Ensar','Saracoglu','28.05.2021','10.00','10.10.1992','Erkek','Hamza Boynukalin'), 
            ('Haci','Kavraz','28.05.2021','10.15','05.17.1995','Erkek','Halil Sezai'), 
            ('Ihsan','Yuce','28.05.2021','10.30','04.17.1986','Erkek','Hasan Ustundag'), 
            ('Ulas','Kirgin','28.05.2021','10.45','10.24.2001','Erkek','Hamza Boynukalin'),
            ('Habibe','Kirman','28.05.2021','11.00','07.19.1997','Kadin','Hamza Boynukalin'),
            ('Eda','Tankas','28.05.2021','11.15','03.19.1980','Kadin','Hamza Boynukalin'), 
            ('Begum','Mersin','28.05.2021','11.30','02.28.1998','Kadin','Hasan Ustundag'), 
            ('Recep','Ozcan','28.05.2021','11.45','07.01.1943','Erkek','Hamza Boynukalin'), 
            ('Murat','Battal','28.05.2021','13.00','05.04.1999','Erkek','Mehmet Uzun'), 
            ('Serkan','Polat','28.05.2021','13.45','09.01.1988','Erkek','Hamza Boynukalin'),
            ('Feyza','Akkaya','28.05.2021','14.00','08.11.1977','Kadin','Hasan Ustundag'), 
            ('Mustafa Kemal','Gokce','28.05.2021','14.15','04.29.1955','Erkek','Mehmet Uzun'),
            ('Hasan','Yurt','28.05.2021','14.30','10.20.1988','Erkek','Mehmet Uzun'), 
            ('Fatih','Ar','28.05.2021','14.45','04.17.1977','Erkek','Halil Sezai'), 
            ('Burak','Dal','28.05.2021','15.00','06.19.1995','Erkek','Hasan Ustundag'), 
            ('Ergin','Dost','28.05.2021','15.15','12.29.2009','Erkek','Mehmet Uzun'), 
            ('Guray','Kalbur','28.05.2021','15.30','11.11.1999','Erkek','Hamza Boynukalin'), 
            ('Ali','Akbas','28.05.2021','16.00','01.12.2000','Erkek','Halil Sezai'), 
            ('Goksel','Kaya','28.05.2021','16.30','03.19.1988','Kadin','Hasan Ustundag'), 
            ('Elif','Yilmaz','28.05.2021','16.45','02.05.2021','Kadin','Mehmet Uzun')
            
        ''')
        self.conn.commit()
    def createTrigger(self)->None:
        '''
            Bu fonksyion sql triggerlerini olusturur.
        '''
        self.cursor.execute('''
            IF EXISTS (select * from sysobjects where name like '%Hasta_INSERT_Notification%')
            DROP TRIGGER Hasta_INSERT_Notification                        
        ''')
        self.cursor.execute('''            
            CREATE TRIGGER Hasta_INSERT_Notification
                    ON Hasta
            AFTER INSERT
            AS
            BEGIN
                SET NOCOUNT ON;

                DECLARE @ID INT

                SELECT @ID = inserted.ID 
                FROM inserted
                declare @body varchar(500) = 'Hasta with ID: ' + CAST(@ID AS VARCHAR(5)) + ' inserted.'
                EXEC msdb.dbo.sp_send_dbmail
                        @profile_name = 'hastaneRandevu'
                        ,@recipients = 'yalcinyusufyy@gmail.com'
                        ,@subject = 'Yeni Hasta Kaydi'
                        ,@body = 'Hastane randevunuz alinmistir.'
            END
            
        ''')
        self.conn.commit()
    def createProcedure(self)->None:
        '''
            Bu fonksyion sql procedurlerini olusturur.
        '''
        self.cursor.execute('''
            IF EXISTS (
                    SELECT type_desc, type
                    FROM sys.procedures WITH(NOLOCK)
                    WHERE NAME = 'createTable'
                        AND type = 'P'
                    )
                    DROP PROCEDURE dbo.createTable    
            IF EXISTS (
                    SELECT type_desc, type
                    FROM sys.procedures WITH(NOLOCK)
                    WHERE NAME = 'hastaGencler'
                    AND type = 'P'
                    )
                    DROP PROCEDURE dbo.hastaGencler      
            IF EXISTS (
                    SELECT type_desc, type
                    FROM sys.procedures WITH(NOLOCK)
                    WHERE NAME = 'enYogunGun'
                    AND type = 'P'
                    )
                    DROP PROCEDURE dbo.enYogunGun   
            IF EXISTS (
                    SELECT type_desc, type
                    FROM sys.procedures WITH(NOLOCK)
                    WHERE NAME = 'hastaBul'
                    AND type = 'P'
                    )
                    DROP PROCEDURE dbo.hastaBul   
                    
            IF EXISTS (
                    SELECT type_desc, type
                    FROM sys.procedures WITH(NOLOCK)
                    WHERE NAME = 'hastaSil'
                    AND type = 'P'
                    )
                    DROP PROCEDURE dbo.hastaSil           
                                   
        ''')
        self.cursor.execute('''
            CREATE PROCEDURE createTable
            AS
            Select Hasta.ID,Hasta.TC,Hasta.Ad+' '+Hasta.Soyad as ad_soyad,Poliklinikler.Doktor,Poliklinikler.Poliklinik, Randevu.Tarih, Randevu.Saat FROM Hasta
            FULL OUTER join Poliklinikler on Hasta.ID = Poliklinikler.ID
            FULL OUTER join Randevu on Randevu.ID = Hasta.ID
            
        ''')

        self.cursor.execute('''
            CREATE PROC hastaGencler
            AS
            SELECT AVG(DATEDIFF(YY,Dogum_tarihi,GETDATE()) ) from Istatistik
            where Cinsiyet = 'Erkek' AND DATEDIFF(YY,Dogum_tarihi,GETDATE()) BETWEEN 18 AND 35
    
        ''')

        self.cursor.execute('''
            CREATE PROC enYogunGun
            AS
            SELECT Tarih FROM (SELECT TOP(1) Tarih, COUNT(*) ID
            FROM Istatistik
            GROUP BY Tarih
            ORDER BY ID desc) as sub_select

            
        ''')

        self.cursor.execute('''
            CREATE PROC hastaBul
            @TC_no nvarchar(11)
            AS 
            Select Hasta.ID,Hasta.TC,Hasta.Ad+' '+Hasta.Soyad as ad_soyad,Poliklinikler.Doktor,Poliklinikler.Poliklinik, Randevu.Tarih, Randevu.Saat FROM Hasta
            FULL OUTER join Poliklinikler on Hasta.ID = Poliklinikler.ID
            FULL OUTER join Randevu on Randevu.ID = Hasta.ID
            WHERE Hasta.TC = @TC_no
            
        ''')
        self.cursor.execute('''
            CREATE PROCEDURE hastaSil
            @TC NVARCHAR(11),
            @Tarih VARCHAR(50),
            @Saat VARCHAR(50)
            AS
            Select Hasta.ID FROM Hasta
            FULL OUTER join Poliklinikler on Hasta.ID = Poliklinikler.ID
            FULL OUTER join Randevu on Randevu.ID = Hasta.ID
            WHERE TC = @TC and Tarih = @Tarih and Saat = @Saat                
        ''')
        self.conn.commit()
    
    def randevuEkle(self,tc=str,ad=str,soyad=str,tarih=str,saat=str,poliklinik=str,doktor=str,mail=str,cinsiyet=str,dogum_tarihi=str)->bool: 
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
    def randevuSil(self,tc=str,tarih=str,saat=str)->bool:
        '''
            Bu fonksiyon verilen tc numarasina hasta tablosundan veri siler.
        '''
        
        strCommand = 'EXEC hastaSil ' + "'"+ str(tc)+ "'," +"'" +str(tarih)+"',"+"'"+str(saat)+"'"
        print(strCommand)
        # Hata varsa return False, yoksa return True.
        try:
            
            self.cursor.execute(strCommand)
            id = self.cursor.fetchall()[0]
            self.cursor.execute('DELETE From Poliklinikler WHERE ID = %s',id)
            self.conn.commit()
            self.cursor.execute('DELETE From Randevu WHERE ID = %s',id)
            self.conn.commit()
            self.cursor.execute('DELETE From Hasta WHERE ID = %s',id)
            self.conn.commit()
            return True
        except Exception:
            return False
            
    
    def getAllPatients(self)->list:
        '''
            Database'e kayitli tum hastalari dondurur.
        '''
        self.cursor.execute('EXEC createTable')
        return self.cursor.fetchall()
    
    
    def getUniqueDoctors(self,date,saat)->list:
        '''
            Verilen tarih ve saat degerlerindeki doktorlari ve calistiklari poliklinikleri dondurur.
        '''
        self.cursor.execute('''      
            SELECT Poliklinikler.Doktor,Poliklinikler.Poliklinik FROM Poliklinikler
            FULL OUTER join Randevu on Randevu.ID = Poliklinikler.ID
            Where Saat = %s and Tarih = %s
        ''',(saat,date))
        return self.cursor.fetchall()
    
        
    def getUniqueTC(self,tc=str)->list:
        self.cursor.execute('SELECT DISTINCT TC,AD,SOYAD FROM HASTA WHERE TC = %s',tc)
        tc = self.cursor.fetchall()
        return tc
    def getIstatistik(self,switch=str):
        '''
            Istatistik fonksiyonu, belirli istatistik degelerini return eder.
        '''
        if(switch=='doktor_siralama'):
            self.cursor.execute(''' 
                        SELECT TOP(1)Poliklinikler.Doktor, Count(*) as muayene_sayisi FROM Poliklinikler, Hasta
                        where Poliklinikler.ID = Hasta.ID
                        Group by Doktor
                        order by  muayene_sayisi  desc
            ''')
            return self.cursor.fethall()
        elif switch=='max_doktor':
            self.cursor.execute(''' 
                    SELECT TOP(1)Istatistik.Doktor, Count(*) as muayene_sayisi FROM Istatistik
                    Group by Doktor
                    order by  muayene_sayisi  desc            
                                
            ''')
            return self.cursor.fetchall()
        elif switch=='toplam_hasta_sayisi':
            self.cursor.execute('SELECT  Count(*) as toplam_hasta_sayisi FROM Istatistik')
            return self.cursor.fetchall()
        
        elif switch == 'toplam_erkek_sayisi':
            self.cursor.execute("SELECT  Count(*) as Erkek FROM Istatistik WHERE Cinsiyet= 'Erkek' ")
            return self.cursor.fetchall()
        elif switch == 'toplam_kadin_sayisi':
            self.cursor.execute("SELECT  Count(*) as Erkek FROM Istatistik WHERE Cinsiyet= 'Kadin' ")
            return self.cursor.fetchall()
            
        elif switch =='erkek_yas':
            self.cursor.execute("SELECT  AVG(DATEDIFF(YY,Dogum_tarihi,GETDATE())) as Erkek_yas_ortalamalari FROM Istatistik WHERE Cinsiyet= 'Erkek'")
            return self.cursor.fetchall()
        elif switch =='kadin_yas':
            self.cursor.execute("SELECT  AVG(DATEDIFF(YY,Dogum_tarihi,GETDATE())) as Erkek_yas_ortalamalari FROM Istatistik WHERE Cinsiyet= 'Kadin'")
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

    def getIstatistikValues(self):
        self.cursor.execute('SELECT * FROM Istatistik')
        return (self.cursor.fetchall())
