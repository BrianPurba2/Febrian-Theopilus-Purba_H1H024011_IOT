Pertanyaan Analisis
```
1. Uraian Hasil Tugas Percobaan
-Percobaan 2A (Mode Station - STA): ESP32 berhasil dikonfigurasi sebagai client yang terhubung ke router/hotspot. Hasil pada Serial Monitor menunjukkan keberhasilan proses koneksi dengan menampilkan IP Address dinamik dari router, MAC Address unik ESP32, serta parameter nilai RSSI (kekuatan sinyal). Indikator LED pada GPIO 2 menyala sebagai konfirmasi bahwa status koneksi bernilai WL_CONNECTED.
-Percobaan 2B (Mode Access Point - AP): ESP32 berhasil bertindak sebagai pemancar hotspot mandiri (SSID: ESP32_Access Point). Perangkat client (seperti smartphone/laptop) dapat mendeteksi dan terhubung ke jaringan tersebut. Serial Monitor secara real-time menampilkan IP Address default AP (192.168.4.1) dan memperbarui jumlah client yang terhubung menggunakan fungsi WiFi.softAPgetStationNum() setiap 5 detik.

2. Pengaruh Kekuatan Sinyal (RSSI) Terhadap Kestabilan Koneksi
Received Signal Strength Indication (RSSI) diukur dalam satuan dBm dan bernilai negatif. Kekuatan sinyal berpengaruh langsung terhadap stabilitas data pada perangkat IoT:
-Sinyal Sangat Baik (-30 dBm hingga -67 dBm): Koneksi sangat stabil, transfer data cepat, dan latency/delay transmisi rendah.
-Sinyal Lemah (lebih rendah dari -80 dBm): Menyebabkan packet loss (data hilang), delay pengiriman data sensor, hingga risiko terputus koneksi secara mendadak (disconnection). Hal ini membuat siklus pemantauan IoT menjadi tidak responsif atau gagal mengirim data ke cloud.

3. Cara Kerja ESP32 Membedakan Peran Station (STA) dan Access Point (AP)
ESP32 membedakan kedua fungsi ini pada lapisan stack jaringan (TCP/IP Adapter/Wi-Fi Driver) melalui konfigurasi antarmuka (interface) internalnya:
-Sebagai Station (Klien/STA): Antarmuka WiFi ESP32 bekerja secara pasif mendengarkan beacon frame dari router, lalu melakukan proses jabat tangan (handshake) authentication/association. ESP32 meminta alokasi alamat IP melalui DHCP Server milik router/network eksternal.
-Sebagai Access Point (AP): Antarmuka WiFi ESP32 bertindak secara aktif memancarkan beacon frame (SSID), menjalankan layanan DHCP Server internal untuk membagikan alamat IP (default: 192.168.4.1) kepada perangkat yang terhubung, serta memproses permintaan autentikasi client.
```
Penjelasan Kode
```
1. Percobaan 2A: Konfigurasi Mode Station (STA)
Kod ini mengonfigurasikan ESP32 sebagai Station (STA), iaitu peranti bertindak sebagai client yang menyambung ke rangkaian WiFi yang sedia ada (contohnya hotspot telefon atau router).

>Komponen Utama Kod:
Pengisytiharan Pemboleh Ubah:
-ssid dan password: Menyimpan nama rangkaian WiFi ("poco") dan kata laluan ("9876543210").
-ledPin = 2: Menggunakan pin GPIO 2 (biasanya LED terbina pada ESP32) sebagai penunjuk status sambungan.

>Fungsi setup():
-Serial.begin(115200): Memulakan komunikasi serial pada kelajuan 115200 bps untuk paparan Serial Monitor.
-WiFi.mode(WIFI_STA): Menetapkan mode ESP32 sebagai Station sahaja.
-WiFi.begin(ssid, password): Memulakan proses penyambungan ke rangkaian WiFi.
-while (WiFi.status() != WL_CONNECTED): Gelung menyemak status sehingga sambungan berjaya. Titik . dipaparkan setiap 0.5 saat semasa proses penyambungan.

>Maklumat Rangkaian: Selepas berjaya disambungkan, kod akan memaparkan:
-WiFi.localIP(): Alamat IP yang diberikan oleh router kepada ESP32.
-WiFi.macAddress(): Alamat perkakasan fizikal (MAC) unik bagi modul WiFi ESP32.
-WiFi.RSSI(): Kekuatan isyarat WiFi dalam unit dBm.
-digitalWrite(ledPin, HIGH): Menyalakan LED sebagai tanda status telah menyambung.

>Fungsi loop():
-Setiap 5 saat (delay(5000)), ESP32 menyemak status sambungan WiFi melalui WiFi.status().
-Jika masih terhubung (WL_CONNECTED), mesej "Status: Terhubung" dipaparkan.
-Jika terputus, mesej "Status: Terputus" dipaparkan dan LED dimatikan.
```
Dokumentasi Praktikum<p>
<img width="640" height="480" alt="IMG-20260915-WA0002" src="https://github.com/user-attachments/assets/9e7b7795-8c51-474a-96dd-d4f630ca6494" /><p>
Gambar Output Program<p>
<img width="640" height="480" alt="IMG-20260915-WA0003" src="https://github.com/user-attachments/assets/0ae585ce-3fa4-409f-b375-c63a23ebb886" /><P>
Dokumentasi hasil rangkaian<p>

Rangkaian Skematik<p>
Percobaan 2A<p>
<img width="394" height="392" alt="image" src="https://github.com/user-attachments/assets/81f714d9-2a28-4992-8002-4c7d1a815601" /><p>

Percobaan 2B<p>
<img width="238" height="319" alt="image" src="https://github.com/user-attachments/assets/539c7134-8cd5-48d7-893c-5fbf378b147f" /><p>

