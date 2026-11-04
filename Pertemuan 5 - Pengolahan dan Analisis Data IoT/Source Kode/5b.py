import time
import math
import random
import pandas as pd
import matplotlib.pyplot as plt

JUMLAH_SAMPEL = 30  # jumlah data

data = []

# -- Tahap 1: akuisisi data dummy (pengganti sensor DHT22 via MQTT)
# Mock function pengganti sensor DHT22 (sama seperti versi ESP)
jumlahBaca = 0  # penghitung jumlah pembacaan

def bacaSuhuMock():
    global jumlahBaca
    jumlahBaca += 1

    # Suhu dasar berubah secara bertahap
    suhuDasar = 28.0 + 2.0 * math.sin(jumlahBaca * 0.08)

    # Noise kecil untuk mensimulasikan fluktuasi sensor
    noise = random.randint(-5, 5) * 0.1  # random(-5,6) di C++ (maks eksklusif)

    suhu = suhuDasar + noise

    # Lonjakan suhu setiap 25 pembacaan untuk simulasi anomali
    if jumlahBaca % 25 == 0:
        suhu += 8.0

    return suhu

for i in range(JUMLAH_SAMPEL):
    suhu = bacaSuhuMock()
    data.append({"waktu": time.strftime("%Y-%m-%d %H:%M:%S"), "suhu": suhu})
    print(f"[{len(data)}/{JUMLAH_SAMPEL}] suhu = {suhu:.2f}")
    time.sleep(0.1)  # jeda kecil supaya kolom waktu bervariasi

# -- Tahap 2: simpan ke CSV
df = pd.DataFrame(data)
df.to_csv("data_suhu.csv", index=False)
print("Data tersimpan di data_suhu.csv")

# -- Tahap 3: analisis statistik dan deteksi anomali (z-score)
rata2 = df["suhu"].mean()
std = df["suhu"].std()

if std == 0:
    df["zscore"] = 0.0
else:
    df["zscore"] = (df["suhu"] - rata2) / std

df["anomali"] = df["zscore"].abs() > 2

print(f"Rata-rata   : {rata2:.2f}")
print(f"Std deviasi : {std:.2f}")
print(f"Minimum     : {df['suhu'].min():.2f}")
print(f"Maksimum    : {df['suhu'].max():.2f}")
print(f"Jumlah anomali: {df['anomali'].sum()}")

# -- Tahap 4: visualisasi
plt.figure(figsize=(10, 4))
plt.plot(df.index, df["suhu"], marker="o", label="Suhu")
anom = df[df["anomali"]]
plt.scatter(anom.index, anom["suhu"], color="red", s=100, label="Anomali", zorder=3)
plt.axhline(rata2, color="gray", linestyle="--", label="Rata-rata")
plt.xlabel("Urutan data")
plt.ylabel("Suhu (°C)")
plt.title("Data Suhu dan Deteksi Anomali")
plt.legend()
plt.tight_layout()
plt.savefig("grafik_suhu.png")
plt.show()
