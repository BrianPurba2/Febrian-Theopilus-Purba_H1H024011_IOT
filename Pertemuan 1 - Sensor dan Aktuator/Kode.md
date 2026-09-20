Percobaan 1A
```
#include <DHT.h>

#define DHTPIN 4        // pin data DHT22 terhubung ke GPIO 4
#define DHTTYPE DHT22   // tipe sensor yang digunakan

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin(); // inisialisasi sensor DHT22
  Serial.println("Memulai akuisisi data sensor DHT22...");
}

void loop() {
  // Membaca data kelembaban dan suhu
  float kelembaban = dht.readHumidity();
  float suhu = dht.readTemperature();

  // Periksa apakah pembacaan berhasil
  if (isnan(kelembaban) || isnan(suhu)) {
    Serial.println("Gagal membaca data dari sensor DHT22!");
  } else {
    Serial.print("Suhu: ");
    Serial.print(suhu);
    Serial.print(" °C, Kelembaban: ");
    Serial.print(kelembaban);
    Serial.println(" %");
  }
```
Percobaan 1B
```
#include <DHT.h>

#define DHTPIN 4          // DATA DHT22 → GPIO 2
#define DHTTYPE DHT22
#define RELAYPIN 5        // Relay → GPIO 5

DHT dht(DHTPIN, DHTTYPE);

const float suhuThreshold = 30.0;

void setup() {
  Serial.begin(115200);
  pinMode(DHTPIN, INPUT_PULLUP); // pull-up internal, tanpa resistor
  dht.begin();
  pinMode(RELAYPIN, OUTPUT);
  digitalWrite(RELAYPIN, LOW);
}

void loop() {
  delay(2000); // DHT22 butuh 2 detik antar pembacaan

  float suhu = dht.readTemperature();

  if (isnan(suhu)) {
    Serial.println("Gagal membaca data sensor!");
    delay(1000);
  } else {
    Serial.print("Suhu: ");
    Serial.print(suhu);
    Serial.print(" °C -> ");

    if (suhu > suhuThreshold) {
      digitalWrite(RELAYPIN, HIGH);
      Serial.println("Aktuator: ON");
    } else {
      digitalWrite(RELAYPIN, LOW);
      Serial.println("Aktuator: OFF");
    }
  }


  delay(2000); // jeda pembacaan setiap 2 detik
}
