from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """
    Özel kullanıcı modeli - öğrenci ve öğretmen rolleri
    """
    ROLE_CHOICES = [
        ('student', 'Öğrenci'),
        ('tutor', 'Öğretmen'),
    ]
    
    GRADE_LEVEL_CHOICES = [
        (1, '1. Sınıf'),
        (2, '2. Sınıf'),
        (3, '3. Sınıf'),
        (4, '4. Sınıf'),
        (5, '5. Sınıf'),
        (6, '6. Sınıf'),
        (7, '7. Sınıf'),
        (8, '8. Sınıf'),
        (9, '9. Sınıf'),
        (10, '10. Sınıf'),
        (11, '11. Sınıf'),
        (12, '12. Sınıf'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True, null=True, verbose_name="Biyografi")
    grade_level = models.IntegerField(
        choices=GRADE_LEVEL_CHOICES,
        blank=True,
        null=True,
        verbose_name="Sınıf Seviyesi"
    )
    # Öğretmenler için puanlama sistemi
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        verbose_name="Puan"
    )
    total_lessons = models.IntegerField(default=0, verbose_name="Toplam Ders Sayısı")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Subject(models.Model):
    """
    Ders konuları modeli
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Ders Adı")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Ders"
        verbose_name_plural = "Dersler"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class TutorSubject(models.Model):
    """
    Öğretmenlerin hangi dersleri verebileceğini belirten ara tablo
    """
    tutor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'tutor'},
        related_name='tutor_subjects'
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    experience_years = models.IntegerField(default=0, verbose_name="Deneyim Yılı")
    
    class Meta:
        unique_together = ['tutor', 'subject']
        verbose_name = "Öğretmen Dersi"
        verbose_name_plural = "Öğretmen Dersleri"
    
    def __str__(self):
        return f"{self.tutor.username} - {self.subject.name}"


class LessonRequest(models.Model):
    """
    Ders talep modeli
    """
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('approved', 'Onaylandı'),
        ('rejected', 'Reddedildi'),
    ]
    
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='lesson_requests_as_student'
    )
    tutor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'tutor'},
        related_name='lesson_requests_as_tutor'
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Durum"
    )
    message = models.TextField(verbose_name="Mesaj")
    preferred_date = models.DateTimeField(verbose_name="Tercih Edilen Tarih")
    duration_hours = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        verbose_name="Ders Süresi (saat)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Ders Talebi"
        verbose_name_plural = "Ders Talepleri"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.username} -> {self.tutor.username} ({self.subject.name})"
