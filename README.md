# Flight Anomaly Detection Map

Bu proje, **OpenSky Network API**'sinden uçuş verilerini alarak uçuşların konumlarını harita üzerinde gösterir. Ayrıca, **Isolation Forest** algoritması kullanarak uçuş verilerindeki anomaliyi tespit eder ve bu uçuşları harita üzerinde kırmızı işaretçilerle belirtir.

## Özellikler

- **Veri Çekme**: OpenSky Network API'sinden uçuş verileri alınır.
- **Veri Temizleme**: Eksik veriler temizlenir ve sadece geçerli uçuşlar gösterilir.
- **Harita Görselleştirmesi**: Uçuşlar harita üzerinde gösterilir ve anormal uçuşlar kırmızı renkte işaretlenir.
- **Anomali Tespiti**: Uçuş verilerindeki anormallikler (yüksek hız, anormal irtifa, vb.) **Isolation Forest** algoritması ile tespit edilir.
- **Popup Bilgisi**: Uçuşa tıklanarak detaylı bilgiler (callsign, origin_country, altitude, velocity) görüntülenebilir.

---

## Gereksinimler

Bu projeyi çalıştırabilmek için aşağıdaki araçları ve kütüphaneleri kurmanız gerekecek:

- **Python 3.x**: Python programlama dili (Proje Python 3.x sürümü ile çalışmaktadır).
- **Python Paketleri**: Aşağıdaki Python kütüphanelerini yüklemeniz gerekecek:
  - `requests`: OpenSky API'den veri çekmek için
  - `pandas`: Veriyi işlemek ve analiz etmek için
  - `folium`: Harita görselleştirmeleri için
  - `scikit-learn`: Anomali tespiti yapmak için **Isolation Forest** algoritması

---

## Kurulum Adımları

### Adım 1: Python Yükleyin

İlk olarak, [Python 3.x](https://www.python.org/downloads/) sürümünü bilgisayarınıza indirip yükleyin.

### Adım 2: Sanal Ortam Oluşturun (Opsiyonel)

Bir sanal ortam oluşturmak, proje bağımlılıklarını izole ederek sisteminize karışmasını engeller. Bu adım isteğe bağlıdır ancak önerilir.

1. Sanal ortam oluşturmak için terminal veya komut satırını açın ve şu komutu çalıştırın:

   ```bash
   python -m venv myenv
   ```

2. Sanal ortamı aktif hale getirin:
   - **Windows**:
     ```bash
     myenv\Scripts\activate
     ```
   - **MacOS/Linux**:
     ```bash
     source myenv/bin/activate
     ```

### Adım 3: Gerekli Python Paketlerini Yükleyin

Aşağıdaki komutları kullanarak gerekli Python kütüphanelerini yükleyin:

```bash
pip install requests pandas folium scikit-learn
```

### Adım 4: Projeyi İndirin veya Klonlayın

Projeyi GitHub üzerinden indirebilir veya klonlayabilirsiniz.

- GitHub'dan projenin ZIP dosyasını indirip çıkarın.
- Alternatif olarak, git kullanarak projenizi klonlayabilirsiniz:

```bash
git clone https://github.com/<your-username>/flight-anomaly-detection.git
cd flight-anomaly-detection
```

### Adım 5: Uygulamayı Çalıştırın

Projeyi çalıştırmak için terminal veya komut satırında aşağıdaki komutu kullanarak Python dosyasını çalıştırın:

```bash
python app.py
```

Uygulamanız, uçuş verilerini OpenSky API'den çekip harita üzerinde gösterecektir. Anormal uçuşlar kırmızı işaretçilerle belirtilir.

---

## Katkıda Bulunma

Eğer bu projeye katkıda bulunmak isterseniz, **Pull Request** gönderebilirsiniz. Projenin geliştirilmesine yardımcı olmak için öneri veya hata raporları gönderebilirsiniz.

---

**Bu proje, uçuş verilerini görselleştirerek anomali tespiti yapmanıza olanak sağlar. Yüksek hız, anormal irtifa gibi veriler üzerinde çalışarak uçuşlardaki olası sorunları tespit edebilirsiniz.**
