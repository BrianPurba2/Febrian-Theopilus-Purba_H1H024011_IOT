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
