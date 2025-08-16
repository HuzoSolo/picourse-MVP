# Picourse API - Öğrenci ve Öğretmen Özel Ders Platformu

## 🎯 Proje Açıklaması

Picourse API, öğrenci ve öğretmenlerin buluşabileceği bir özel ders platformunun backend API'sidir. Platform, öğrencilerin ihtiyaç duydukları konularda uzman öğretmenleri bulabilmesini ve ders talepleri oluşturabilmesini sağlar. Öğretmenler de gelen talepleri onaylayabilir veya reddedebilir.

### Temel İş Akışı
1. **Kullanıcı Kaydı**: Kullanıcılar öğrenci veya öğretmen olarak kayıt olur
2. **Öğretmen Keşfi**: Öğrenciler, konu bazında öğretmenleri arayabilir ve filtreler
3. **Ders Talebi**: Öğrenciler seçtikleri öğretmenlere ders talebi gönderir
4. **Talep Yönetimi**: Öğretmenler gelen talepleri onaylar veya reddeder
5. **Profil Yönetimi**: Kullanıcılar profillerini güncelleyebilir

## 🛠 Teknoloji Seçimleri ve Gerekçeleri

### Authentication: JWT (JSON Web Tokens)
**Neden JWT?**
- **Stateless**: Server-side session yönetimi gerektirmez
- **Scalable**: Mikroservis mimarisine uygun
- **Mobile-Friendly**: Mobil uygulamalar için ideal
- **Secure**: Dijital imza ile güvenli
- **Standard**: OAuth 2.0 ve OpenID Connect ile uyumlu

**djangorestframework-simplejwt seçimi:**
- DRF ile mükemmel entegrasyon
- Token rotation desteği
- Customizable token claims
- Refresh token mekanizması

### API Dokümantasyonu: drf-spectacular
**Neden drf-spectacular?**
- **OpenAPI 3.0**: Modern API standardı
- **Auto-generation**: Koddan otomatik dokümantasyon
- **Interactive UI**: Swagger UI ile test edilebilir dokümantasyon
- **Type Safety**: Python type hints desteği

### Veritabanı: SQLite (Development) / PostgreSQL (Production Ready)
**Neden SQLite (development)?**
- **Zero Configuration**: Kolay setup
- **Portable**: Tek dosya
- **Testing**: Hızlı test execution

**Production için PostgreSQL önerisi:**
- **ACID Compliance**: Tam ACID destegi
- **Concurrency**: Çoklu kullanıcı desteği
- **JSON Support**: Modern veri tipleri
- **Scaling**: Horizontal ve vertical scaling

## 🏗 Mimari ve Tasarım Kararları

### Model-View-Serializer (MVS) Pattern
DRF'nin önerdiği MVS pattern'ini benimsedim:

```
Models (Data Layer) → Serializers (Business Logic) → Views (Presentation Layer)
```

### Separation of Concerns
- **Models**: Sadece veri yapısı ve business rules
- **Serializers**: Veri validation ve transformation
- **Views**: HTTP request/response handling
- **Permissions**: Authorization logic
- **Services**: Karmaşık business logic (future expansion)

### Role-Based Access Control (RBAC)
```python
User Roles:
├── Student (öğrenci)
│   ├── Can create lesson requests
│   ├── Can view own requests
│   └── Can update own profile
└── Tutor (öğretmen)
    ├── Can view incoming requests
    ├── Can approve/reject requests
    ├── Can update own profile
    └── Can manage subject expertise
```

### RESTful API Design
HTTP metodlarını semantic anlamlarına uygun kullandım:
- **GET**: Veri okuma
- **POST**: Yeni kaynak oluşturma
- **PATCH**: Kısmi güncelleme (partial update)


## 💾 Veri Modeli

### Model Tasarım Kararları

#### Custom User Model
```python
class User(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    # ... diğer alanlar
```
**Neden Custom User?**
- Future-proof: Gelecekte ek alanlar kolayca eklenebilir
- Role-based: Tek model ile farklı kullanıcı tipleri
- Django Best Practice: Django dokümantasyonunda önerilen yaklaşım

#### Many-to-Many with Through Model
```python
class TutorSubject(models.Model):
    tutor = models.ForeignKey(User, ...)
    subject = models.ForeignKey(Subject, ...)
    experience_years = models.IntegerField(...)
```
**Neden Through Model?**
- **Extra Fields**: Experience years gibi ek bilgiler
- **Flexibility**: Gelecekte rating, certification vb. eklenebilir
- **Query Optimization**: Daha verimli sorgular


## 🔌 API Endpoint'leri

### Authentication Endpoints
```
POST /api/auth/register/     # Kullanıcı kaydı
POST /api/auth/login/        # JWT token alma
POST /api/auth/token/        # JWT token alma (Django SimpleJWT)
POST /api/auth/token/refresh/ # Token yenileme
POST /api/auth/token/verify/  # Token doğrulama
```

### User Management
```
GET  /api/me/               # Profil görüntüleme
PATCH /api/me/              # Profil güncelleme
```

### Subject Management
```
GET /api/subjects/          # Ders konuları listesi (public)
```

### Tutor Discovery
```
GET /api/tutors/            # Öğretmen listesi (filtering, search, ordering)
GET /api/tutors/{id}/       # Öğretmen detayları
```

### Lesson Request Management
```
POST /api/lesson-requests/create/    # Ders talebi oluşturma (student only)
GET  /api/lesson-requests/           # Talep listesi (role-based filtering)
PATCH /api/lesson-requests/{id}/     # Talep durum güncelleme (tutor only)
```

### Documentation
```
GET /api/docs/              # Swagger UI
GET /api/schema/            # OpenAPI schema
```

## 🔒 Güvenlik ve İzinler

### Authentication Strategy
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### Custom Permission Classes
```python
# permissions.py
class IsStudentOrReadOnly(BasePermission):
    """Sadece öğrenciler yazabilir, herkes okuyabilir"""
    
class IsOwnerOrTutorForLessonRequest(BasePermission):
    """Sadece ilgili öğrenci/öğretmen erişebilir"""
```

### Input Validation
- **Serializer Level**: DRF serializers ile veri validasyonu
- **Model Level**: Model constraints ve validators
- **Database Level**: Unique constraints, foreign keys

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.8+
- Virtual Environment (önerilir)

### Kurulum Adımları

1. **Repository'yi klonlayın**
```bash
git clone <repository-url>
cd picourse-MVP/api-service
```

2. **Virtual environment oluşturun ve aktive edin**
```bash
python -m venv env
source env/bin/activate  # macOS/Linux
# veya
env\Scripts\activate  # Windows
```

3. **Gerekli paketleri yükleyin**
```bash
pip install -r requirements.txt
```

4. **Veritabanı migration'larını çalıştırın**
```bash
cd picourseAPI
python manage.py makemigrations
python manage.py migrate
```

5. **Test verilerini yükleyin**
```bash
python manage.py seed_data
```

6. **Development server'ı başlatın**
```bash
python manage.py runserver
```

### Test Kullanıcıları
Seed data ile oluşturulan test kullanıcıları (şifre: `password123`):

**Öğrenciler:**
- `can_ogrenci` - 11. sınıf
- `elif_ogrenci` - 12. sınıf  
- `berk_ogrenci` - 10. sınıf

**Öğretmenler:**
- `ahmet_ogretmen` - Matematik, Fizik (4.8★)
- `fatma_ogretmen` - İngilizce (4.9★)
- `mehmet_ogretmen` - Kimya, Fizik (4.6★)
- `ayse_ogretmen` - Tarih (4.7★)
- `ali_ogretmen` - Matematik, Fizik (4.5★)

## 📚 API Kullanım Örnekleri

### 1. Kullanıcı Kaydı

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "yeni_ogrenci",
    "email": "ogrenci@example.com",
    "password": "guvenli_sifre123",
    "password_confirm": "guvenli_sifre123",
    "first_name": "Ahmet",
    "last_name": "Yılmaz",
    "role": "student",
    "grade_level": 11
  }'
```

**Response:**
```json
{
  "message": "Kullanıcı başarıyla oluşturuldu.",
  "user": {
    "id": 9,
    "username": "yeni_ogrenci",
    "email": "ogrenci@example.com",
    "first_name": "Ahmet",
    "last_name": "Yılmaz",
    "role": "student",
    "role_display": "Öğrenci",
    "bio": null,
    "grade_level": 11,
    "grade_level_display": "11. Sınıf",
    "rating": 0.0,
    "total_lessons": 0,
    "date_joined": "2025-08-16T08:46:00.123456Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

### 2. Kullanıcı Girişi

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "can_ogrenci",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "message": "Giriş başarılı.",
  "user": {
    "id": 6,
    "username": "can_ogrenci",
    "email": "can@example.com",
    "first_name": "Can",
    "last_name": "Yıldız",
    "role": "student",
    "role_display": "Öğrenci",
    "bio": "11. sınıf öğrencisiyim. Üniversite sınavına hazırlanıyorum.",
    "grade_level": 11,
    "grade_level_display": "11. Sınıf",
    "rating": 0.0,
    "total_lessons": 0,
    "date_joined": "2025-08-16T08:44:05.453226Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

### 3. Ders Konuları Listesi

**Request:**
```bash
curl -X GET http://localhost:8000/api/subjects/
```

**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 4,
      "name": "İngilizce",
      "description": "İngilizce dil bilgisi, konuşma ve yazma becerileri",
      "created_at": "2025-08-16T08:44:05.439945Z"
    },
    {
      "id": 2,
      "name": "Fizik",
      "description": "Klasik fizik, modern fizik ve uygulamalı fizik",
      "created_at": "2025-08-16T08:44:05.438647Z"
    },
    {
      "id": 3,
      "name": "Kimya",
      "description": "Genel kimya, organik ve inorganik kimya",
      "created_at": "2025-08-16T08:44:05.439361Z"
    },
    {
      "id": 1,
      "name": "Matematik",
      "description": "Temel matematik, cebir, geometri ve analiz konuları",
      "created_at": "2025-08-16T08:44:05.437644Z"
    },
    {
      "id": 5,
      "name": "Tarih",
      "description": "Türk tarihi, dünya tarihi ve tarih metodolojisi",
      "created_at": "2025-08-16T08:44:05.441142Z"
    }
  ]
}
```

### 4. Öğretmen Arama ve Filtreleme

**Request:**
```bash
curl -X GET "http://localhost:8000/api/tutors/?search=matematik&ordering=-rating&limit=2"
```

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "ahmet_ogretmen",
      "first_name": "Ahmet",
      "last_name": "Yılmaz",
      "role": "tutor",
      "role_display": "Öğretmen",
      "bio": "Matematik alanında 10 yıllık deneyime sahip. Üniversite hazırlık kurslarında ders vermekteyim.",
      "rating": 4.8,
      "total_lessons": 150,
      "subjects": [
        {
          "subject": {
            "id": 1,
            "name": "Matematik",
            "description": "Temel matematik, cebir, geometri ve analiz konuları",
            "created_at": "2025-08-16T08:44:05.437644Z"
          },
          "experience_years": 12
        },
        {
          "subject": {
            "id": 2,
            "name": "Fizik",
            "description": "Klasik fizik, modern fizik ve uygulamalı fizik",
            "created_at": "2025-08-16T08:44:05.438647Z"
          },
          "experience_years": 8
        }
      ]
    },
    {
      "id": 5,
      "username": "ali_ogretmen",
      "first_name": "Ali",
      "last_name": "Çelik",
      "role": "tutor",
      "role_display": "Öğretmen",
      "bio": "Matematik ve Fizik dersleri veriyorum. Özellikle sayısal konularda uzmanım.",
      "rating": 4.5,
      "total_lessons": 95,
      "subjects": [
        {
          "subject": {
            "id": 1,
            "name": "Matematik",
            "description": "Temel matematik, cebir, geometri ve analiz konuları",
            "created_at": "2025-08-16T08:44:05.437644Z"
          },
          "experience_years": 3
        },
        {
          "subject": {
            "id": 2,
            "name": "Fizik",
            "description": "Klasik fizik, modern fizik ve uygulamalı fizik",
            "created_at": "2025-08-16T08:44:05.438647Z"
          },
          "experience_years": 14
        }
      ]
    }
  ]
}
```

### 5. Ders Talebi Oluşturma (Authentication Required)

**Request:**
```bash
curl -X POST http://localhost:8000/api/lesson-requests/create/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "tutor": 1,
    "subject": 1,
    "message": "Matematik dersinde limit ve türev konularında yardıma ihtiyacım var. Hafta sonu uygun olur mu?",
    "preferred_date": "2025-08-20T14:00:00",
    "duration_hours": 2
  }'
```

**Response:**
```json
{
  "id": 5,
  "student": 6,
  "student_name": "Can Yıldız",
  "student_username": "can_ogrenci",
  "tutor": 1,
  "tutor_name": "Ahmet Yılmaz",
  "tutor_username": "ahmet_ogretmen",
  "subject": 1,
  "subject_name": "Matematik",
  "status": "pending",
  "status_display": "Beklemede",
  "message": "Matematik dersinde limit ve türev konularında yardıma ihtiyacım var. Hafta sonu uygun olur mu?",
  "preferred_date": "2025-08-20T14:00:00Z",
  "duration_hours": 2,
  "created_at": "2025-08-16T08:50:00.123456Z",
  "updated_at": "2025-08-16T08:50:00.123456Z"
}
```

### 6. Ders Taleplerini Görüntüleme (Öğrenci Perspektifi)

**Request:**
```bash
curl -X GET "http://localhost:8000/api/lesson-requests/?role=student" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 5,
      "student": 6,
      "student_name": "Can Yıldız",
      "student_username": "can_ogrenci",
      "tutor": 1,
      "tutor_name": "Ahmet Yılmaz",
      "tutor_username": "ahmet_ogretmen",
      "subject": 1,
      "subject_name": "Matematik",
      "status": "pending",
      "status_display": "Beklemede",
      "message": "Matematik dersinde limit ve türev konularında yardıma ihtiyacım var.",
      "preferred_date": "2025-08-20T14:00:00Z",
      "duration_hours": 2,
      "created_at": "2025-08-16T08:50:00.123456Z",
      "updated_at": "2025-08-16T08:50:00.123456Z"
    },
    {
      "id": 1,
      "student": 6,
      "student_name": "Can Yıldız",
      "student_username": "can_ogrenci",
      "tutor": 1,
      "tutor_name": "Ahmet Yılmaz",
      "tutor_username": "ahmet_ogretmen",
      "subject": 1,
      "subject_name": "Matematik",
      "status": "pending",
      "status_display": "Beklemede",
      "message": "Matematik dersinde limit ve türev konularında yardıma ihtiyacım var.",
      "preferred_date": "2025-08-17T08:44:05.466783Z",
      "duration_hours": 2,
      "created_at": "2025-08-16T08:44:05.467208Z",
      "updated_at": "2025-08-16T08:44:05.467215Z"
    }
  ]
}
```

### 7. Ders Talebini Onaylama (Öğretmen Perspektifi)

**Request:**
```bash
curl -X PATCH http://localhost:8000/api/lesson-requests/5/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "status": "approved"
  }'
```

**Response:**
```json
{
  "id": 5,
  "student": 6,
  "student_name": "Can Yıldız",
  "student_username": "can_ogrenci",
  "tutor": 1,
  "tutor_name": "Ahmet Yılmaz",
  "tutor_username": "ahmet_ogretmen",
  "subject": 1,
  "subject_name": "Matematik",
  "status": "approved",
  "status_display": "Onaylandı",
  "message": "Matematik dersinde limit ve türev konularında yardıma ihtiyacım var.",
  "preferred_date": "2025-08-20T14:00:00Z",
  "duration_hours": 2,
  "created_at": "2025-08-16T08:50:00.123456Z",
  "updated_at": "2025-08-16T08:52:30.789012Z"
}
```

### 8. Hata Durumları

**Authentication Hatası:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Permission Hatası:**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**Validation Hatası:**
```json
{
  "password": ["Bu alan boş bırakılamaz."],
  "email": ["Geçerli bir e-posta adresi girin."]
}
```

## 🧪 Test Stratejisi

### Test Kategorileri

1. **Authentication Tests**
   - Kullanıcı kaydı (happy path)
   - Giriş başarılı/başarısız senaryoları
   - Token validation

2. **Permission Tests**
   - Rol bazlı erişim kontrolü
   - Object-level permissions
   - Anonymous user restrictions

3. **Business Logic Tests**
   - Lesson request workflow
   - Student-tutor interactions
   - Status transitions

4. **Integration Tests**
   - Complete user journey
   - API endpoint interactions
   - Data consistency

### Test Çalıştırma
```bash
# Tüm testleri çalıştır
python manage.py test


# Verbose output ile
python manage.py test --verbosity=2


### Test Verileri
Test ortamında kullanılacak veriler için seed data:
```bash
python manage.py seed_data --clear
```

### Dosya Açıklamaları

#### Core Django Files
- **settings.py**: Django konfigürasyonu, DRF ayarları, JWT ayarları
- **urls.py**: URL routing, API endpoint tanımları
- **models.py**: Veri modelleri (User, Subject, LessonRequest, TutorSubject)

#### DRF Specific Files
- **serializers.py**: API serialization, validation logic
- **views.py**: API endpoints, business logic
- **permissions.py**: Custom permission classes

#### Supporting Files
- **admin.py**: Django admin panel konfigürasyonu
- **tests.py**: Test suite
- **seed_data.py**: Test data generation command


#### Neden Custom Permissions?
DRF'nin built-in permissions yeterli değildi çünkü:
- Role-based access control gerekiyordu
- Object-level permissions gerekiyordu
- Business logic specific rules vardı

#### Neden Through Model?
Standard many-to-many yeterli değildi çünkü:
- Experience years gibi ek bilgiler gerekiyordu
- Query optimization imkanı

#### Neden Separate Serializers?
- **Create vs Read**: Farklı field requirements
- **Security**: Sensitive fields hiding
- **Performance**: Optimized queries
- **Validation**: Context-specific rules


### API Dokümantasyonu
- **Swagger UI**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Development Server
```bash
python manage.py runserver
# API: http://localhost:8000/api/
# Admin: http://localhost:8000/admin/
```
### Troubleshooting
- **Migration Issues**: `python manage.py migrate --run-syncdb`
- **Permission Errors**: Check role assignments
- **Token Expiry**: Use refresh endpoint
- **CORS Issues**: Add django-cors-headers for frontend
