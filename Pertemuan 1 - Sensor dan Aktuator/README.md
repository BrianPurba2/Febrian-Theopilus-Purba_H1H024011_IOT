Pertanyaan Analisis
```
1) Uraian Hasil Tugas Praktikum pada Setiap Percobaan
Percobaan 1A (Akuisisi Data Sensor DHT22):Hasil dari percobaan ini adalah keberhasilan ESP32 dalam membaca data fisik lingkungan berupa suhu (dalam °C) dan kelembaban relatif (dalam %) menggunakan sensor digital DHT22. Data tersebut berhasil dikirimkan dan ditampilkan pada Serial Monitor Arduino IDE dengan interval pembaruan setiap 2 detik. Program juga dilengkapi dengan fungsi validasi isnan() untuk mengantisipasi kegagalan pembacaan (error handling) agar sistem tidak mengolah data kosong (NaN).
Percobaan 2A (Kendali Aktuator Relay Berdasarkan Data Sensor):Hasil dari percobaan ini adalah terwujudnya sistem kendali otomatis berbasis ambang batas (threshold). Ketika sensor DHT22 mendeteksi nilai suhu di atas nilai acuan (\[30.0^{\circ }\text{C}\]), ESP32 mengirim sinyal HIGH ke GPIO 26 sehingga relay (atau LED simulasi) menyala (ON). Sebaliknya, ketika suhu berada di bawah threshold, pin kendali diatur ke LOW dan aktuator otomatis mati (OFF). Status kestabilan ini tercatat secara real-time pada Serial Monitor.

2) Pengaruh Akurasi dan Waktu Tanggap (Response Time) Sensor Terhadap Kecepatan Reaksi Aktuator
Pengaruh Akurasi: Akurasi sensor menentukan ketepatan pengambilan keputusan oleh mikrokontroler. Jika akurasi sensor rendah (margin error besar), aktuator dapat terpicu pada waktu yang salah—misalnya menyala terlalu cepat atau justru terlambat dari kondisi nyata di lapangan.
Pengaruh Waktu Tanggap (Response Time): Waktu tanggap menentukan seberapa cepat perubahan fisik lingkungan dapat dideteksi. Sensor DHT22 memiliki jeda waktu tanggap inheren sekitar 2 detik untuk memperbarui datanya. Semakin lambat waktu tanggap suatu sensor, maka akan semakin lama pula akumulasi penundaan (delay) bagi aktuator untuk bereaksi terhadap perubahan darurat di lingkungan sekitar.

3) Cara Kerja Sistem dalam Mengubah Data Sensor Menjadi Keputusan Kendali Aktuator
Proses perubahan dari data mentah menjadi aksi fisik (akuisisi hingga aktuasi) mengikuti siklus berikut:
-Akuisisi Data: Sensor DHT22 mendeteksi parameter fisik lingkungan (suhu dan kelembaban), mengonversinya menjadi sinyal digital biner melalui protokol komunikasi internalnya, lalu mengirimkannya ke pin GPIO 4 ESP32.
-Pemrosesan Data: Protokol data tersebut dibaca oleh ESP32 menggunakan pustaka DHT.h dan diterjemahkan ke dalam variabel bilangan desimal (float kelembaban dan float suhu).
-Pengambilan Keputusan (Logika): Mikrokontroler mengevaluasi nilai variabel tersebut menggunakan fungsi logika pengondisian (if-else) dengan membandingkan nilai suhu aktual terhadap nilai konstanta suhuThreshold (\[30.0^{\circ }\text{C}\]).
-Aktuasi: Berdasarkan hasil evaluasi logika, ESP32 mengubah status tegangan keluaran (digitalWrite) pada pin GPIO 26. Tegangan ini memicu koil elektromagnetik pada modul relay untuk mengubah posisi sakelar fisik (menghubungkan atau memutus aliran listrik pada beban aktuator).

4) Implementasi Kombinasi Sensor-Aktuator pada Sistem Smart Farming dan Smart Home
-Sistem Smart Home (Rumah Pintar):
Kombinasi ini dapat diaplikasikan pada sistem pengondisian udara otomatis (Automated HVAC). Ketika sensor suhu mendeteksi ruangan melebihi batas kenyamanan (misalnya \[>27^{\circ }\text{C}\]), mikrokontroler akan memicu relay untuk menyalakan pendingin ruangan (AC) atau kipas angin. Begitu suhu ruangan kembali sejuk di bawah batas bawah, AC akan dimatikan secara otomatis untuk menghemat konsumsi energi listrik.
-Sistem Smart Farming (Pertanian Cerdas):
Kombinasi ini dapat digunakan pada sistem otomatisasi Greenhouse atau penyiraman tanaman. Sensor kelembaban tanah dan suhu udara memantau kondisi media tanam secara berkala. Jika kelembaban terdeteksi drop di bawah batas minimum (tanah kering) atau suhu udara terlalu ekstrem, sistem akan langsung mengaktifkan modul relay untuk menghidupkan pompa air/nozzle misting untuk menyiram tanaman hingga parameter lingkungan kembali optimal bagi pertumbuhan tanaman.
```
Penjelasan Kode
```
1. Percobaan 1A: Akuisisi Data Sensor DHT22 (Suhu dan Kelembaban)
Kode ini bertujuan untuk membaca data suhu dan kelembaban secara berkala, lalu menampilkan hasilnya ke Serial Monitor.

Inisialisasi & Konfigurasi
#include <DHT.h>: Memanggil pustaka (library) utama untuk mengontrol sensor DHT.

#define DHTPIN 4: Menentukan pin GPIO 4 pada mikrokontroler (seperti ESP32/ESP8266) sebagai pin komunikasi data.

#define DHTTYPE DHT11: Menentukan jenis sensor yang dipakai.

Catatan Kesalahan di Komentar Kode:
Penulisan kode menggunakan DHTTYPE DHT11, tetapi komentar di baris kode menyebutkan DHT22. Pustaka akan memproses data menggunakan algoritma DHT11.

Fungsi setup()
Serial.begin(115200);: Membuka jalur komunikasi serial dengan kecepatan baud rate 115200 bps untuk mengirim teks ke monitor komputer.

dht.begin();: Mengaktifkan sensor DHT agar siap membaca data.

Fungsi loop()
dht.readHumidity() & dht.readTemperature(): Mengambil nilai kelembaban (persen) dan suhu (Celsius) lalu menyimpannya ke variabel berjenis float.

isnan(...): Fungsi Is Not a Number untuk mengecek apakah pembacaan sensor gagal/terputus. Jika gagal, pesan peringatan akan dikirim ke Serial Monitor.

Serial.print(...): Jika berhasil, nilai suhu dan kelembaban ditampilkan ke Serial Monitor.

2. Percobaan 1B: Kendali Aktuator Relay Berdasarkan Data Sensor
Kode ini merupakan pengembangan dari Percobaan 1A. Selain membaca suhu, sistem ini menambahkan logika kontrol untuk menyalakan atau mematikan Relay berdasarkan suhu lingkungan.

Tambahan Inisialisasi
#define RELAYPIN 5: Menentukan pin GPIO 5 terhubung ke modul Relay.

const float suhuThreshold = 30.0;: Menentukan batas suhu pemicu sebesar 30,0 °C.

Fungsi setup()
pinMode(DHTPIN, INPUT_PULLUP);: Mengaktifkan resistor pull-up internal mikrokontroler pada pin data sensor.

pinMode(RELAYPIN, OUTPUT);: Mengatur pin relay sebagai output.

digitalWrite(RELAYPIN, LOW);: Memastikan relay berada dalam kondisi mati (OFF) saat sistem pertama kali menyala.

Fungsi loop()
delay(2000);: Memberikan jeda 2 detik sebelum membaca sensor, karena keluarga sensor DHT membutuhkan jeda minimal 1–2 detik agar hasilnya stabil.

Logika Kontrol Keputusan:

Jika Suhu > 30,0 °C: digitalWrite(RELAYPIN, HIGH); → Relay aktif (ON). Aktuator (seperti kipas angin atau pendingin) menyala.

Jika Suhu ≤ 30,0 °C: digitalWrite(RELAYPIN, LOW); → Relay nonaktif (OFF).
```
Dokumentasi Praktikum
<img width="1280" height="576" alt="IMG-20260901-WA0017" src="https://github.com/user-attachments/assets/0e41f7a5-afee-47e2-8151-0aea1a4f8e9c" />
Gambar yang menampilkan Serial Monitor
<img width="1280" height="576" alt="IMG-20260901-WA0022" src="https://github.com/user-attachments/assets/5cecb722-71fb-4622-a868-11bc4a161f6a" />
Peralatan yang digunakan seperti aktuator dan sensor
<img width="1280" height="576" alt="IMG-20260901-WA0020" src="https://github.com/user-attachments/assets/f97a136d-1a39-4d5b-817a-46d5e1b9815a" />
Gambar Aktuator

Rangkaian Skematik
Percobaan 1A<p>
<img width="503" height="456" alt="image" src="https://github.com/user-attachments/assets/669fe3ff-5b45-4d56-a941-7914f7d03f50" />

Percobaan 1B<p>
<img width="626" height="429" alt="image" src="https://github.com/user-attachments/assets/7971d851-4ad9-4068-a763-454236a85604" />


