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
