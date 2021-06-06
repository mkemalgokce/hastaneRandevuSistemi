# Hastane Randevu Otomasyonu

## Installation

* pip install requirements.txt
<hr>

Bu hastanede 2 poliklinik ve 4 doktor vardır. Her poliklinikte 2 doktor şeklinde hasta tedavi etmektedir. 

Projeyi yaparken MSSQL Server veri tabanı ile Python dili kullanıldı.Veri tabanının arayüzünü görselleştirmek için arayüz olarak PyQt5 kütüphanesi kullanıldı.Arayüzleri dizayn etmek için Qt Designer adlı programdan yararlanıldı.

Otomasyon kodu yazılırken hem Windows hem de MacOS işletim sisteminde çalışması sağlanmıştır.Veri tabanı bağlantısı için MacOS için pymssql kullanırken,Windows işletimli bilgisayar için pyodbc kütüphanesi kullanıldı.
# Giriş Ekranı:

![image](https://user-images.githubusercontent.com/61952281/120885823-8db36080-c5f3-11eb-81c9-3895cc00e699.png)

# Ana Sayfa:

![image](https://user-images.githubusercontent.com/61952281/120885920-1cc07880-c5f4-11eb-8938-94064a820e84.png)

# Yazdır:  

SQL’den çekilen verileri FPDF kütüphanesini kullanarak, pdf dosyasına aktarır. Pdf dosyasında yeni randevu almış hastaların bilgileri bulunmaktadır.

![image](https://user-images.githubusercontent.com/61952281/120886269-bfc5c200-c5f5-11eb-8ac6-a07c16843c0e.png)
# Randevu Al: 


Hasta TC numarasını ve poliklinik bilgisini girerek uygun doktorlardan randevu alacaktır. Randevu aralıkları 15 dk şeklindedir. Yani hasta 9:00 , 9:15, 9:30, 9:45 … şeklindeki
slotlardan randevu alabilir. Bir hasta ilgili doktor için belirli bir saatte randevu aldıysa o doktorun o tarih ve saatteki durumu meşgul olduğundan başka bir hasta randevu alamayacaktır.TC kimlik 11 haneden küçük olamaz.İsim ve soyisim sadece harflerden oluşur.

![image](https://user-images.githubusercontent.com/61952281/120885994-614c1400-c5f4-11eb-9c77-32bf9c2bfa5a.png)

Hasta randevu aldığında şu şekilde e-posta adresine mail gelecektir :

![image](https://user-images.githubusercontent.com/46056478/120931760-b292fb00-c6fb-11eb-80c3-1c25b11d9f65.png)

# Randevu İptal Et:

Hasta TC numarası,randevu tarihi ve saatini girerek randevusunu iptal edebilecektir.
![image](https://user-images.githubusercontent.com/61952281/120886080-c56ed800-c5f4-11eb-89ee-833d121a1ae4.png)
# İstatistik Menüsü:
Her bir doktorun muayene ettiği hasta bilgileri, vb istatiksel bilgilere erişilmektedir.Bu verilere ulaşırken diğerlerinde olduğu gibi sql sorgularıyla sağlanmıştır.

![image](https://user-images.githubusercontent.com/61952281/120886161-3615f480-c5f5-11eb-8e00-b3a1053ddc2a.png)
