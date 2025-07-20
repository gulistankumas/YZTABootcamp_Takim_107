# Tahlil Karar Destek Sistemi

## 👥 Takım Üyeleri

| Fotoğraf | İsim | Görev | GitHub |
|:--------:|:-----|:------|:-------|
| <img src="https://avatars.githubusercontent.com/gulistankumas" width="80"/> | Gülistan Kumaş    | Scrum Master/Developer      | [![GitHub](https://img.shields.io/badge/GitHub-000?logo=github&logoColor=white)](https://github.com/gulistankumas) |
| <img src="https://avatars.githubusercontent.com/yusufkaan03" width="80"/>   | Yusuf Kaan Çelebi | Developer         | [![GitHub](https://img.shields.io/badge/GitHub-000?logo=github&logoColor=white)](https://github.com/yusufkaan03) |
| <img src="https://avatars.githubusercontent.com/Haticeozken" width="80"/>   | Hatice Özken      | Developer         | [![GitHub](https://img.shields.io/badge/GitHub-000?logo=github&logoColor=white)](https://github.com/Haticeozken) |
| <img src="https://avatars.githubusercontent.com/YunusEmreCakar" width="80"/>| Yunus Emre Çakar  | Developer         | [![GitHub](https://img.shields.io/badge/GitHub-000?logo=github&logoColor=white)](https://github.com/YunusEmreCakar) |


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

1. **Tahlil Verilerinin Alınması**  
   - Tahlil sonuçları laboratuvar sisteminden otomatik olarak alınır.

2. **Yapay Zeka Analizi**  
   - Mevcut tahlil sonuçları, hastanın geçmiş verileriyle karşılaştırılır.  
   - Anormal yüksek/düşük değerler tespit edilir.  
   - Olası risk faktörleri belirlenir ve klinik bir ön rapor hazırlanır.

3. **Doktor İncelemesi**  
   - Doktor, muayene sırasında sistem üzerinden raporu görüntüler.  
   - Tanıyı koyar, tedavi planını oluşturur ve hastaya özel uyarı/notlar ekler.

4. **Hasta Bilgilendirmesi**  
   - Muayene sonrasında hasta, sistem üzerinden aşağıdaki bilgilere erişir:  
     - Doktorun tanısı  
     - İlaç ve dozaj bilgileri  
     - Yaşam tarzı ve beslenme önerileri  
     - Yapay zekâ destekli bilgilendirmeler

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
- LLM 
- FastAPI (API servisi)
- PostgreSQL  (veritabanı)
- React (web arayüzü)
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

## Notlar

Bu sistem, doktor kararlarının yerini almaz. Nihai tanı ve tedavi planı yalnızca sağlık profesyonelleri tarafından belirlenir.

# SPRINT 1
## Sprint Notları
Sprint 1 sürecinde proje ekibi olarak öncelikli hedefimiz proje fikrinin netleştirilmesi, ekip rollerinin belirlenmesi ve temel planlamaların yapılması olmuştur. Bu aşamada geliştirilecek ürünün temel özellikleri, kullanıcı kitlesi ve teknik gereksinimleri üzerine yoğunlaşılmıştır. Takım içi iletişim ve iş birliği süreçleri için gerekli platformlar belirlenmiş ve görev dağılımları yapılmıştır.

## Sprint İçinde Tamamlanması Tahmin Edilen Puan
Sprint 1 için toplamda tamamlanması planlanan puan miktarı 100 olarak belirlenmiştir. Bu puan, fikir bulma, marka ismi seçimi, takım rollerinin belirlenmesi, proje zaman çizelgesinin çıkarılması ve ilk tasarım kararlarının alınması gibi temel hazırlık görevlerinden oluşmaktadır.

## Puan Tamamlama Mantığı
Proje genelinde toplam backlog puanı 300 olarak belirlenmiştir. Sprint 1'de bu toplam puanın 100 puanlık kısmının tamamlanması hedeflenmiştir. Sprint sonunda belirlenen görevler başarıyla tamamlanarak hedeflenen puana ulaşılmış ve sprint başarıyla tamamlanmıştır.

## Daily Scrum
Sprint süresince ekip içi günlük iletişim ve durum değerlendirmeleri WhatsApp üzerinden gerçekleştirilmiştir. Her ekip üyesi ilerleme durumu hakkında bilgilendirme yapmış, karşılaşılan sorunlar anında paylaşılmış ve çözüm yolları hızlıca bulunmuştur. Bu süreçte ekip, iletişimi güçlü tutarak etkin bir iş birliği sergilemiştir.

<details>
  <summary>Daily Scrum: Ekran Görüntüleri</summary>

  <img src="https://github.com/user-attachments/assets/8bd5db9c-fb3f-4ac1-b14d-66d24e7e4a6b" alt="Daily Scrum Screenshot" width="600"/>

</details>


## Sprint Board Screenshotları
Sprint boyunca yürütülen çalışmalar ve görevlerin durumu Trello üzerinden takip edilmiştir. Backlog, To Do, ve Doing listeleri altında görevler planlanmış ve ilerlemeleri görsel olarak izlenmiştir. Aşağıda Sprint 1'e ait pano görseli yer almaktadır:

![image](https://github.com/user-attachments/assets/e333b4f9-a990-4437-92b9-4d983bdaa394)



## Ürün Durumu: Ekran Görüntüleri
Sprint 1 sonunda ürünün henüz görsel arayüz geliştirmesi başlamamış olmakla birlikte, proje fikri, marka ismi ve takım yapısına ilişkin kararlar alınmıştır. Bu aşamada proje fikrine uygun ilk logo tasarımları, renk seçimleri ve kullanıcı senaryoları belirlenmiştir. Bu hazırlıklar ilerleyen sprintlerde arayüz çalışmalarına temel oluşturacaktır.


## Sprint Review
Sprint Review toplantısında, proje fikrinin netleştirildiği, takım rollerinin başarıyla belirlendiği ve görev dağılımının tamamlandığı teyit edilmiştir. Ürün geliştirme sürecine başlamadan önce gerekli tüm ön hazırlıklar tamamlanmıştır. Ekip üyeleri sürece aktif katılım göstermiş ve hedeflenen tüm görevler başarıyla sonuçlandırılmıştır.

## Sprint Retrospective
Sprint Retrospective sürecinde takım içi iletişimin verimli geçtiği ancak bazı görevlerin daha erken aşamada belirlenmesinin faydalı olacağı not edilmiştir. Takım üyeleri, rollerin netleştirilmesinden ve görev paylaşımının dengeli şekilde yapılmasından memnuniyetlerini ifade etmiştir. Gelecek sprintlerde fiziksel veya çevrim içi kısa toplantıların artırılması kararlaştırılmıştır.


# SPRINT 2

## Sprint Notları

Sprint 2 sürecinde proje ekibi, teknik geliştirmelere odaklanarak sistemin temel bileşenlerini oluşturmuştur. Bu sprintte özellikle veritabanı altyapısının kurulumu, veri işleme modülünün hazırlanması, LLM testlerinin yapılması ve arayüz tasarımına başlanması gibi adımlar başarıyla gerçekleştirilmiştir. Ayrıca RAG sistemi ile anormal değerleri karşılaştırmak üzere kullanılacak veri seti hazırlanmış ve entegrasyon için altyapı kurulmuştur.

## Sprint İçinde Tamamlanması Tahmin Edilen Puan

Sprint 2 için belirlenen hedefler doğrultusunda toplamda 100 puanlık iş planlanmıştır. Bu puan; veritabanı kurulumu, RAG veri setinin hazırlanması, yapay zeka modülünün temel testleri ve frontend başlangıcını kapsamaktadır. Planlanan tüm iş kalemleri başarıyla tamamlanmış ve puan hedefi gerçekleştirilmiştir.

## Puan Tamamlama Mantığı

Sprint 2 için belirlenen işlerin tamamlanmasıyla birlikte 100 puanlık hedefe ulaşılmıştır. Yapılan işler projenin temel yapısının oluşmasını sağlamış ve sonraki sprintler için sağlam bir zemin oluşturmuştur.

## Daily Scrum

Sprint süresince günlük iletişim WhatsApp üzerinden sürdürülmüş ve her ekip üyesi kendi ilerlemesini paylaşmıştır. Teknik engeller, test çıktıları ve arayüzde karşılaşılan sorunlar anlık olarak ekip ile paylaşılmış ve çözüm üretilmiştir.

<details>
  <summary>Ekran Görüntüleri</summary>

  <img src="https://github.com/user-attachments/assets/4563b058-b9d8-41ca-b0e2-e516608b7853" alt="image" width="827" height="817"/>

</details>


## Sprint Board Screenshotları

Sprint 2 süresince görevler Trello panosunda Backlog, To Do, Doing ve Done listeleri altında yönetilmiştir. Sprint boyunca işlerin ilerlemesi görselleştirilmiş ve her görev bir ekip üyesine atanarak takip edilmiştir.

<img width="1708" height="1059" alt="image" src="https://github.com/user-attachments/assets/420c3c54-52d1-4836-8c69-07976394c33c" />


## Ürün Durumu: Ekran Görüntüleri

Sprint sonunda sistemin aşağıdaki bileşenleri oluşturulmuştur:

* Veritabanı kurulumu ve temel veri yapıları
* Anormal değerlerin tespiti için kullanılacak veri setinin hazırlanması (RAG sistemi)
* LLM ile örnek prompt testleri ve doktor notu-öneri bağlantısı
* Frontend tarafında giriş ekranı ve panel iskeleti oluşturuldu.
<details>
  <summary>Ekran Görüntüleri</summary>

  <img src="https://github.com/user-attachments/assets/7b0df87d-8aa4-46d2-8c3c-de0ad5e27292" alt="Ürün Durumu: Ekran Görüntüleri" width="600"/>

</details>

Bu yapılar, sonraki sprintte ürünün işlevsel hale gelmesine temel sağlayacaktır.

## Sprint Review

Sprint Review toplantısında, planlanan tüm işlerin zamanında tamamlandığı görülmüştür. Ekip üyeleri, backend ve frontend tarafında uyumlu çalışarak sistemin temel parçalarını ortaya koymuştur. LLM test sonuçları olumlu değerlendirilmiş ve geliştirilmeye açık noktalar belirlenmiştir. Frontend iskeletinin oluşturulması, görsel testlerin başlamasına olanak sağlamıştır.

## Sprint Retrospective

Sprint sonunda ekip içi iş birliği yüksek bulunmuş, özellikle RAG veri seti hazırlanırken yaşanan zaman yönetimi sorunu ekip içi destekle çözülmüştür. Kod paylaşım süreçlerinin biraz daha sistematik hale getirilmesi ve test senaryolarının yazımına daha erken başlanması gerektiği not edilmiştir. Gelecek sprintte entegrasyon odaklı ilerlenmesi ve UI/UX testlerinin devreye alınması planlanmıştır.

