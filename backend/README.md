# 🏥 Sağlık Analiz Merkezi - Backend API

Yapay zeka destekli tahlil sonuçları analiz platformu backend servisi.

## 🚀 Özellikler

### 🤖 LLM Entegrasyonu
- **OpenAI GPT-4** ve **Anthropic Claude** desteği
- Tıbbi analiz için özelleştirilmiş prompt'lar
- JSON formatında yapılandırılmış yanıtlar
- Hata durumunda fallback mekanizmaları

### 📊 Analiz Türleri
1. **Kan Tahlili Analizi** - Anormal değer tespiti ve risk değerlendirmesi
2. **Risk Değerlendirmesi** - 30 günlük sağlık riski tahmini
3. **Doktor Insights** - Klinik değerlendirme desteği
4. **Hasta Eğitimi** - Kişiselleştirilmiş eğitim materyalleri

### 🔒 Güvenlik
- JWT tabanlı kimlik doğrulama
- Role-based access control (RBAC)
- HIPAA uyumlu audit logging
- Veri şifreleme

### 📈 Veritabanı
- PostgreSQL ile ilişkisel veri modeli
- SQLAlchemy ORM
- Alembic migration yönetimi

## 🏗️ Mimari

```
backend/
├── app/
│   ├── api/v1/           # API endpoint'leri
│   ├── core/             # Konfigürasyon ve güvenlik
│   ├── models/           # Veritabanı modelleri
│   ├── services/         # İş mantığı servisleri
│   └── utils/            # Yardımcı fonksiyonlar
├── tests/                # Test dosyaları
├── alembic/              # Database migration'ları
├── logs/                 # Log dosyaları
└── requirements.txt      # Python bağımlılıkları
```

## 🚀 Kurulum

### 1. Gereksinimler
- Python 3.9+
- PostgreSQL 13+
- Redis (opsiyonel, cache için)

### 2. Sanal Ortam Oluşturma
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows
```

### 3. Bağımlılıkları Yükleme
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
`.env` dosyası oluşturun:
```env
# Veritabanı
DATABASE_URL=postgresql://user:password@localhost/health_analysis

# LLM API Keys
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# Güvenlik
SECRET_KEY=your-secret-key-here
MEDICAL_DATA_ENCRYPTION_KEY=your-encryption-key

# Uygulama
DEBUG=True
LOG_LEVEL=INFO
```

### 5. Veritabanı Kurulumu
```bash
# PostgreSQL'de veritabanı oluştur
createdb health_analysis

# Migration'ları çalıştır
alembic upgrade head
```

### 6. Uygulamayı Başlatma
```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 API Dokümantasyonu

Uygulama başlatıldıktan sonra:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 LLM Kullanım Örnekleri

### 1. Kan Tahlili Analizi
```python
# API çağrısı
POST /api/v1/analyze/blood-test
{
    "test_results": [
        {
            "test_name": "Total Kolesterol",
            "value": 280,
            "unit": "mg/dL",
            "reference_range": "125-200",
            "status": "high"
        }
    ],
    "patient_info": {
        "age": 45,
        "gender": "male",
        "medical_history": ["hipertansiyon"]
    }
}
```

### 2. Risk Değerlendirmesi
```python
POST /api/v1/analyze/risk-assessment
{
    "test_results": [...],
    "patient_info": {...}
}
```

### 3. Doktor Insights
```python
POST /api/v1/analyze/doctor-insights
{
    "test_results": [...],
    "patient_info": {...},
    "symptoms": ["göğüs ağrısı", "nefes darlığı"]
}
```

## 🧪 Test

```bash
# Tüm testleri çalıştır
pytest

# Coverage ile test
pytest --cov=app

# Belirli test dosyası
pytest tests/test_llm_service.py
```

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Logs
```bash
# Uygulama logları
tail -f logs/app.log

# Error logları
tail -f logs/error.log
```

## 🔒 Güvenlik Özellikleri

### 1. Veri Şifreleme
- Hassas hasta verileri AES-256 ile şifrelenir
- API anahtarları güvenli şekilde saklanır

### 2. Audit Logging
- Tüm veri erişimleri loglanır
- HIPAA uyumlu audit trail
- IP adresi ve kullanıcı bilgileri kaydedilir

### 3. Rate Limiting
- API rate limiting
- LLM çağrıları için özel limitler

## 🚀 Deployment

### Docker ile
```bash
# Docker image oluştur
docker build -t health-analysis-api .

# Container çalıştır
docker run -p 8000:8000 health-analysis-api
```

### Docker Compose ile
```bash
docker-compose up -d
```

## 📈 Performans

### Caching
- Redis ile analiz sonuçları cache'lenir
- TTL: 1 saat (yapılandırılabilir)

### Async Processing
- Background task'lar ile uzun süren işlemler
- Celery entegrasyonu (opsiyonel)

### Database Optimization
- İndeksler optimize edilmiş
- Connection pooling
- Query optimization

## 🔧 Geliştirme

### Code Style
```bash
# Black ile format
black app/

# Flake8 ile lint
flake8 app/

# MyPy ile type checking
mypy app/
```

### Pre-commit Hooks
```bash
pre-commit install
```

## 📞 Destek

- **GitHub Issues**: Bug raporları ve özellik istekleri
- **Email**: Teknik destek için
- **Dokümantasyon**: `/docs` endpoint'i

## 📄 Lisans

MIT License - Detaylar için LICENSE dosyasına bakın.

---

**Not**: Bu sistem eğitim amaçlıdır. Gerçek tıbbi kullanım için ek güvenlik ve doğrulama önlemleri gerekir. 