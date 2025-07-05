# [Proje İsmi]

## Takım üyeleri

| ![Photo](https://avatars.githubusercontent.com/u/0000000?v=4) | **Name**          | **Title**         | **Socials**                                                                                                                                         |
|:-------------------------------------------------------------:|-------------------|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| ![Photo](https://avatars.githubusercontent.com/gulistankumas) | Gülistan Kumaş    | Scrum Master      | [![GitHub](https://img.shields.io/badge/GitHub-000?logo=github&logoColor=white)](https://github.com/kullanici)|
| ![Photo](https://avatars.githubusercontent.com/yusufkaan03)   | Yusuf Kaan Çelebi | Developer         | [![GitHub](https://img.shields.io/badge/GitHub-000?logo=github&logoColor=white)](https://github.com/kullanici)|
| ![Photo](https://avatars.githubusercontent.com/Haticeozken)   | Hatice Özken      | Developer         | [![GitHub](https://img.shields.io/badge/GitHub-000?logo=github&logoColor=white)](https://github.com/kullanici)|
| ![Photo](https://avatars.githubusercontent.com/YunusEmreCakar)| Yunus Emre Çakar  | Developer         | [![GitHub](https://img.shields.io/badge/GitHub-000?logo=github&logoColor=white)](https://github.com/kullanici)|


## Proje Açıklaması

Bu proje, hastanelerde yapılan kan tahlili sonuçlarının hızlı ve doğru biçimde değerlendirilmesini sağlayan yapay zekâ destekli bir karar destek sistemidir. Sistem, laboratuvardan gelen tahlil verilerini otomatik olarak alır, hastanın önceki sonuçlarıyla kıyaslar, anormal değerleri vurgular ve olası sağlık riskleri hakkında açıklayıcı bir rapor üretir. Doktorlar, hasta muayenesinden önce bu raporu görüntüleyerek hızlıca bilgi edinir ve daha etkili kararlar verebilir. Ayrıca hasta, doktor ziyaretinin ardından sistemle etkileşim kurarak tanısı, ilaçları ve yaşam tarzı önerileri hakkında kişiselleştirilmiş bilgilere ulaşabilir.

---

## Projenin Amacı

- Tahlil sonuçlarının otomatik ve karşılaştırmalı analizini sağlamak
- Doktorların karar verme sürecini hızlandırmak
- Olası riskleri klinik muayeneden önce görünür hale getirmek
- Hastalara tanı ve tedavi süreci hakkında yapay zekâ destekli danışmanlık sunmak

---

## Kullanıcı Senaryosu

1. Tahlil sonuçları laboratuvar sisteminden otomatik olarak alınır.
2. Yapay zekâ motoru:
   - Mevcut sonuçları geçmiş tahlillerle kıyaslar
   - Anormal yüksek/düşük değerleri tespit eder
   - Olası risk faktörlerini belirler
   - Klinik rapor oluşturur
3. Doktor muayene sırasında bu raporu görüntüler ve tanıyı koyar.
4. Doktor sistem üzerinden hastaya özel uyarı ve notları ekler.
5. Hasta muayene sonrası sistemden:
   - Doktorun tanısını
   - İlaç ve doz bilgilerini
   - Yaşam tarzı önerilerini
   - Yapay zekâ destekli bilgilendirmeleri alır.

---

## Desteklenen Tahlil Türleri

- Kan tahlili (ilk aşamada)
> İlerleyen sürümlerde biyokimya, hormon testleri gibi ek modüller planlanmaktadır.

---

## Yapay Zekâ Yetenekleri

- Anormal değerleri otomatik tespit etme
- Geçmiş verilerle istatistiksel karşılaştırma
- Olası risk ve hastalık önerileri
- Hastaya yönelik bilgilendirme ve tavsiye oluşturma
- Doktorun manuel notlarını bağlama dayalı tavsiyelerle ilişkilendirme

---

## Kullanıcı Arayüzü

- Doktorlar için masaüstü/web tabanlı panel
- Hastalar için mobil uygulama veya web arayüzü
- Hastane bilgi sistemi entegrasyonu (otomatik veri aktarımı)

---

## Kullanılan Teknolojiler

- Python
- Pandas, NumPy (veri işleme)
- scikit-learn veya TensorFlow (makine öğrenmesi)
- Flask veya FastAPI (API servisi)
- PostgreSQL veya MongoDB (veritabanı)
- React veya Streamlit (web arayüzü)
- Docker (deployment)

---

## Hedef Kullanıcılar

- Özellikle acil servis doktorları
- Klinik laboratuvar uzmanları
- Hastane bilgi işlem birimleri
- Hastalar ve hasta yakınları

---

## Projenin Farklılaştırıcı Özellikleri

Bu sistem, doktorun ilk bakışta göremeyeceği kadar detaylı analiz ve karşılaştırmayı otomatik olarak hazırlayarak, muayene öncesi tanı sürecini hızlandırır ve karar kalitesini artırır. Anlamlı bağlantılar kurar, geçmiş verileri bağlamsal olarak yorumlar ve hem doktora hem hastaya kişiselleştirilmiş bilgi sağlar.

---

## Proje Durumu

- Fikir aşamasında
- Analiz ve tasarım süreci planlanmaktadır


---

## Notlar

Bu sistem, doktor kararlarının yerini almaz. Nihai tanı ve tedavi planı yalnızca sağlık profesyonelleri tarafından belirlenir.
