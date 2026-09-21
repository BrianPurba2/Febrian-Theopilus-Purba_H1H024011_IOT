Pertanyaan Analisis<p>
1.Uraikan hasil tugas pada praktikum yang telah dilakukan pada setiap percobaan!
Percobaan 3A — HTTP<p>
Pada percobaan HTTP, perangkat berhasil mengirimkan data dalam format JSON menuju endpoint httpbin.org/post menggunakan metode POST. Berdasarkan data pengamatan, pengiriman dilakukan pada interval 10 detik mulai dari waktu 0 sampai 90 detik.

Seluruh 10 kali pengiriman memperoleh HTTP Response Code 200 dan status pengiriman tercatat Berhasil. Response body juga menunjukkan kembali data JSON yang dikirimkan, sehingga data dapat diverifikasi telah diterima oleh server.

Percobaan 3B — MQTT
Pada percobaan MQTT, perangkat berhasil terhubung ke broker dan mempublikasikan data JSON ke topic unsoed/tk245004/nim10/sensor. Data tersebut kemudian diterima oleh subscriber dengan isi JSON yang sama.

Berdasarkan tabel pengamatan, seluruh 10 kali pengiriman pada rentang 0 hingga 90 detik berstatus Terhubung dan Berhasil, serta data yang diterima subscriber sesuai dengan data yang dipublikasikan.

2.Bandingkan besar overhead data dan pola komunikasi antara protokol HTTP dan MQTT berdasarkan hasil percobaan yang telah dilakukan!
Perbedaan utama keduanya terletak pada mekanisme komunikasi yang digunakan.<p>
Aspek	HTTP	MQTT
Pola komunikasi	Request-response	Publish-subscribe
Perantara	Client berkomunikasi langsung dengan server/endpoint	Menggunakan broker MQTT
Pengiriman data	Client membuat request setiap kali data dikirim	Publisher mengirim pesan ke topic
Koneksi	Tidak harus dipertahankan secara terus-menerus	Dirancang untuk koneksi yang tetap terjaga
Overhead	Relatif lebih besar karena terdapat HTTP request/response dan header	Relatif kecil sehingga lebih efisien untuk komunikasi IoT
Cocok untuk	Pengiriman data periodik atau komunikasi berbasis web	Pertukaran data sensor secara kontinu
Pada percobaan, HTTP melakukan pengiriman menuju endpoint menggunakan request POST dan menerima response dari server. Sementara itu, MQTT mengirim data ke broker melalui topic dan data tersebut diterima oleh subscriber.

3.Untuk skenario pengiriman data sensor secara terus-menerus setiap beberapa detik dalam jangka waktu lama, protokol manakah (HTTP atau MQTT) yang lebih sesuai digunakan? Jelaskan alasannya!

Untuk pola pengiriman data sensor secara terus-menerus setiap beberapa detik dalam waktu yang panjang, MQTT lebih sesuai berdasarkan karakteristik yang dijelaskan pada modul.<p>

MQTT menggunakan pola publish-subscribe dan dirancang sebagai protokol komunikasi ringan dengan overhead yang relatif kecil. Selain itu, MQTT mendukung koneksi yang tetap terjaga sehingga sesuai untuk pertukaran data secara kontinu.

Sebaliknya, HTTP menggunakan pola request-response dan memiliki overhead header yang relatif lebih besar. HTTP lebih sesuai ketika perangkat perlu melakukan komunikasi periodik tanpa harus mempertahankan koneksi secara terus-menerus.

4.Bagaimana peran format JSON dalam mendukung interoperabilitas data antara perangkat IoT dan berbagai platform/aplikasi yang berbeda?

JSON berperan sebagai format pertukaran data yang sederhana, ringan, dan mudah dibaca oleh manusia maupun mesin. Struktur data JSON menggunakan pasangan key-value, sehingga informasi dapat disusun secara jelas.<p>

Dalam praktikum ini, data seperti suhu dan kelembaban dikemas dalam JSON sebelum dikirim menggunakan HTTP maupun MQTT. Karena JSON merupakan format berbasis teks yang umum digunakan, data yang berasal dari ESP8266 dapat lebih mudah diproses oleh server, broker, aplikasi MQTT client, maupun platform IoT lain yang mendukung format tersebut.

Contoh data:
```
{"suhu":28.5,"kelembaban":65}
Penggunaan format yang sama pada berbagai sisi komunikasi membantu perangkat pengirim dan penerima memahami struktur data yang dipertukarkan.


