**Percobaan 4A: Subscribe dan Deserialisasi Data JSON untuk Kendali Aktuator
**
```
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// =====================================================
// KONFIGURASI WIFI
// =====================================================
const char* ssid = "poco";
const char* password = "9876543210";

// =====================================================
// KONFIGURASI MQTT
// =====================================================
const char* mqttServer = "broker.hivemq.com";
const int mqttPort = 1883;

// Topic untuk menerima perintah
const char* topicPerintah = "makan";

// =====================================================
// KONFIGURASI LED
// ESP8266 NodeMCU:
// D1 = GPIO 5
// =====================================================
const int ledPin = 5;

// =====================================================
// OBJEK WIFI DAN MQTT
// =====================================================
WiFiClient espClient;
PubSubClient client(espClient);


// =====================================================
// CALLBACK MQTT
// Fungsi ini dipanggil ketika pesan MQTT diterima
// =====================================================
void callback(char* topic, byte* payload, unsigned int length) {

  // Membuat String untuk menyimpan pesan
  String pesan = "";

  // Membaca payload byte per byte
  for (unsigned int i = 0; i < length; i++) {
    pesan += (char)payload[i];
  }

  // Menampilkan pesan ke Serial Monitor
  Serial.println();
  Serial.println("================================");
  Serial.println("PESAN MQTT DITERIMA");
  Serial.println("================================");

  Serial.print("Topic   : ");
  Serial.println(topic);

  Serial.print("Payload : ");
  Serial.println(pesan);

  // ===================================================
  // PARSING JSON
  // ===================================================

  JsonDocument doc;

  DeserializationError error = deserializeJson(doc, pesan);

  // Jika JSON gagal dibaca
  if (error) {

    Serial.print("Gagal parsing JSON: ");
    Serial.println(error.c_str());

    return;
  }

  // ===================================================
  // MENGAMBIL DATA "perintah"
  // ===================================================

  const char* perintah = doc["perintah"];

  // Cek apakah field perintah ada
  if (perintah == nullptr) {

    Serial.println("ERROR: Field 'perintah' tidak ditemukan!");

    return;
  }

  Serial.print("Perintah: ");
  Serial.println(perintah);

  // ===================================================
  // PERINTAH ON
  // ===================================================

  if (String(perintah) == "ON") {

    digitalWrite(ledPin, HIGH);

    Serial.println(">>> LED MENYALA");
    Serial.println("================================");
  }

  // ===================================================
  // PERINTAH OFF
  // ===================================================

  else if (String(perintah) == "OFF") {

    digitalWrite(ledPin, LOW);

    Serial.println(">>> LED MATI");
    Serial.println("================================");
  }

  // ===================================================
  // PERINTAH TIDAK DIKENAL
  // ===================================================

  else {

    Serial.print("Perintah tidak dikenali: ");
    Serial.println(perintah);

    Serial.println("Gunakan:");
    Serial.println("{\"perintah\":\"ON\"}");
    Serial.println("{\"perintah\":\"OFF\"}");
  }
}


// =====================================================
// FUNGSI MENGHUBUNGKAN ESP8266 KE WIFI
// =====================================================
void hubungkanWiFi() {

  Serial.println();
  Serial.println("================================");
  Serial.println("MENGHUBUNGKAN KE WIFI");
  Serial.println("================================");

  Serial.print("SSID: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  // Tunggu sampai WiFi terhubung
  while (WiFi.status() != WL_CONNECTED) {

    delay(500);

    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi berhasil terhubung!");

  // Menampilkan IP ESP8266
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  Serial.println("================================");
}


// =====================================================
// FUNGSI MENGHUBUNGKAN ESP8266 KE MQTT
// =====================================================
void hubungkanMQTT() {

  while (!client.connected()) {

    Serial.println();
    Serial.println("Menghubungkan ke broker MQTT...");

    // Membuat Client ID random
    String clientId = "ESP8266Client-";

    clientId += String(random(0xffff), HEX);

    Serial.print("Client ID: ");
    Serial.println(clientId);

    // Mencoba koneksi MQTT
    if (client.connect(clientId.c_str())) {

      Serial.println("MQTT berhasil terhubung!");

      // Subscribe ke topic
      if (client.subscribe(topicPerintah)) {

        Serial.print("Berhasil subscribe ke topic: ");
        Serial.println(topicPerintah);

      } else {

        Serial.println("Gagal subscribe topic!");
      }

    } else {

      // Jika gagal koneksi
      Serial.print("MQTT gagal, rc=");
      Serial.println(client.state());

      Serial.println("Mencoba kembali dalam 2 detik...");

      delay(2000);
    }
  }
}


// =====================================================
// SETUP
// =====================================================
void setup() {

  // Memulai Serial Monitor
  Serial.begin(115200);

  delay(1000);

  Serial.println();
  Serial.println();
  Serial.println("================================");
  Serial.println("     ESP8266 MQTT CONTROLLER");
  Serial.println("================================");

  // ===================================================
  // KONFIGURASI LED
  // ===================================================

  pinMode(ledPin, OUTPUT);

  // Kondisi awal LED mati
  digitalWrite(ledPin, LOW);

  Serial.println("LED GPIO 5 / D1 siap.");

  // ===================================================
  // HUBUNGKAN WIFI
  // ===================================================

  hubungkanWiFi();

  // ===================================================
  // KONFIGURASI MQTT
  // ===================================================

  client.setServer(mqttServer, mqttPort);

  // Mendaftarkan fungsi callback
  client.setCallback(callback);

  Serial.println();
  Serial.println("Konfigurasi MQTT selesai.");

  // ===================================================
  // HUBUNGKAN MQTT
  // ===================================================

  hubungkanMQTT();
}


// =====================================================
// LOOP
// =====================================================
void loop() {

  // Jika koneksi MQTT terputus
  if (!client.connected()) {

    Serial.println();
    Serial.println("Koneksi MQTT terputus!");

    hubungkanMQTT();
  }

  // Wajib dipanggil terus-menerus
  // agar ESP8266 dapat menerima pesan MQTT
  client.loop();
}
```

**Percobaan 4B: Pertukaran Data Dua Arah (Publish dan
Subscribe Secara Bersamaan)**
```
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

const char* ssid = "poco";
const char* password = "9876543210";
const char* mqttServer = "broker.hivemq.com";
const int mqttPort = 1883;
const char* topicData = "makan";
const char* topicPerintah = "makan";

const int ledPin = 26;

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long waktuTerakhirPublish = 0;
const long intervalPublish = 5000; // publish data setiap 5 detik (non-blocking)

void callback(char* topic, byte* payload, unsigned int length) {
  String pesan;
  for (unsigned int i = 0; i < length; i++) {
    pesan += (char)payload[i];
  }

  JsonDocument doc;
  if (deserializeJson(doc, pesan)) {
    return; // abaikan jika parsing gagal
  }

  const char* perintah = doc["perintah"];
  digitalWrite(ledPin, String(perintah) == "ON" ? HIGH : LOW);
  
  Serial.print("Perintah diterima -> Aktuator: ");
  Serial.println(perintah);
}

void hubungkanWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.println("WiFi berhasil terhubung!");
}

void hubungkanMQTT() {
  while (!client.connected()) {
    String clientId = "ESP8266Client-" + String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      client.subscribe(topicPerintah);
      Serial.println("Terhubung dan subscribe topic perintah");
    } else {
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  
  hubungkanWiFi();
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    hubungkanMQTT();
  }
  client.loop(); // memproses pesan masuk secara terus-menerus

  // Publish data dummy berkala tanpa sensor DHT
  if (millis() - waktuTerakhirPublish > intervalPublish) {
    waktuTerakhirPublish = millis();

    // Generasi nilai suhu dummy (misal 25.0°C - 35.0°C)
    float suhuDummy = random(250, 350) / 10.0;

    JsonDocument doc;
    doc["suhu"] = suhuDummy;
    
    char buffer[128];
    serializeJson(doc, buffer);
    
    client.publish(topicData, buffer);
    Serial.print("Data terkirim: ");
    Serial.println(buffer);
  }
}
