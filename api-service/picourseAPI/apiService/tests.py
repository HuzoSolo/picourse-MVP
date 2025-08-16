from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Subject, TutorSubject, LessonRequest
from datetime import datetime, timedelta

User = get_user_model()


class AuthenticationTestCase(APITestCase):
    """
    Kimlik doğrulama testleri
    """
    
    def setUp(self):
        self.register_url = reverse('user-register')
        self.login_url = reverse('user-login')
        
    def test_user_registration_student(self):
        """Öğrenci kayıt testi"""
        data = {
            'username': 'test_student',
            'email': 'student@test.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'Student',
            'role': 'student',
            'grade_level': 11
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertEqual(User.objects.count(), 1)
        
    def test_user_registration_tutor(self):
        """Öğretmen kayıt testi"""
        data = {
            'username': 'test_tutor',
            'email': 'tutor@test.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'Tutor',
            'role': 'tutor',
            'bio': 'Matematik öğretmeniyim'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        
    def test_user_login(self):
        """Kullanıcı giriş testi"""
        # Önce kullanıcı oluştur
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role='student'
        )
        
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        
    def test_invalid_login(self):
        """Geçersiz giriş testi"""
        data = {
            'username': 'nonexistent',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PermissionTestCase(APITestCase):
    """
    Rol bazlı izin testleri
    """
    
    def setUp(self):
        # Test kullanıcıları oluştur
        self.student = User.objects.create_user(
            username='student',
            email='student@test.com',
            password='pass123',
            role='student'
        )
        
        self.tutor = User.objects.create_user(
            username='tutor',
            email='tutor@test.com',
            password='pass123',
            role='tutor'
        )
        
        # Test ders konusu
        self.subject = Subject.objects.create(
            name='Test Subject',
            description='Test description'
        )
        
        # Öğretmen-ders ilişkisi
        TutorSubject.objects.create(
            tutor=self.tutor,
            subject=self.subject
        )
        
    def test_student_can_create_lesson_request(self):
        """Öğrenci ders talebi oluşturabilir"""
        self.client.force_authenticate(user=self.student)
        
        data = {
            'tutor': self.tutor.id,
            'subject': self.subject.id,
            'message': 'Test message',
            'preferred_date': (datetime.now() + timedelta(days=1)).isoformat(),
            'duration_hours': 2
        }
        
        url = reverse('lesson-request-create')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_tutor_cannot_create_lesson_request(self):
        """Öğretmen ders talebi oluşturamaz"""
        self.client.force_authenticate(user=self.tutor)
        
        data = {
            'tutor': self.tutor.id,
            'subject': self.subject.id,
            'message': 'Test message',
            'preferred_date': (datetime.now() + timedelta(days=1)).isoformat(),
            'duration_hours': 2
        }
        
        url = reverse('lesson-request-create')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_tutor_can_update_lesson_request_status(self):
        """Öğretmen ders talebi durumunu güncelleyebilir"""
        # Ders talebi oluştur
        lesson_request = LessonRequest.objects.create(
            student=self.student,
            tutor=self.tutor,
            subject=self.subject,
            message='Test message',
            preferred_date=datetime.now() + timedelta(days=1),
            duration_hours=2
        )
        
        self.client.force_authenticate(user=self.tutor)
        
        url = reverse('lesson-request-update', kwargs={'pk': lesson_request.pk})
        data = {'status': 'approved'}
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson_request.refresh_from_db()
        self.assertEqual(lesson_request.status, 'approved')
        
    def test_student_cannot_update_lesson_request_status(self):
        """Öğrenci ders talebi durumunu güncelleyemez"""
        lesson_request = LessonRequest.objects.create(
            student=self.student,
            tutor=self.tutor,
            subject=self.subject,
            message='Test message',
            preferred_date=datetime.now() + timedelta(days=1),
            duration_hours=2
        )
        
        self.client.force_authenticate(user=self.student)
        
        url = reverse('lesson-request-update', kwargs={'pk': lesson_request.pk})
        data = {'status': 'approved'}
        response = self.client.patch(url, data)
        
        # Öğrenci kendi talebini bulamaz çünkü queryset sadece öğretmene göre filtreleniyor
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LessonRequestFlowTestCase(APITestCase):
    """
    Ders talebi akış testleri
    """
    
    def setUp(self):
        # Test kullanıcıları ve verileri oluştur
        self.student = User.objects.create_user(
            username='student',
            email='student@test.com',
            password='pass123',
            role='student'
        )
        
        self.tutor = User.objects.create_user(
            username='tutor',
            email='tutor@test.com',
            password='pass123',
            role='tutor'
        )
        
        self.subject = Subject.objects.create(
            name='Mathematics',
            description='Math lessons'
        )
        
        TutorSubject.objects.create(
            tutor=self.tutor,
            subject=self.subject
        )
        
    def test_complete_lesson_request_flow(self):
        """Tam ders talebi akış testi"""
        
        # 1. Öğrenci ders talebi oluşturur
        self.client.force_authenticate(user=self.student)
        
        create_data = {
            'tutor': self.tutor.id,
            'subject': self.subject.id,
            'message': 'Matematik dersinde yardıma ihtiyacım var',
            'preferred_date': (datetime.now() + timedelta(days=2)).isoformat(),
            'duration_hours': 2
        }
        
        create_url = reverse('lesson-request-create')
        response = self.client.post(create_url, create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        lesson_request_id = response.data['id']
        
        # 2. Öğrenci kendi taleplerini görüntüler
        list_url = reverse('lesson-request-list')
        response = self.client.get(list_url, {'role': 'student'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # 3. Öğretmen kendine yapılan talepleri görür
        self.client.force_authenticate(user=self.tutor)
        response = self.client.get(list_url, {'role': 'tutor'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # 4. Öğretmen talebi onaylar
        update_url = reverse('lesson-request-update', kwargs={'pk': lesson_request_id})
        response = self.client.patch(update_url, {'status': 'approved'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 5. Durum değişikliğini kontrol et
        lesson_request = LessonRequest.objects.get(id=lesson_request_id)
        self.assertEqual(lesson_request.status, 'approved')


class TutorSearchTestCase(APITestCase):
    """
    Öğretmen arama ve filtreleme testleri
    """
    
    def setUp(self):
        # Test verileri oluştur
        self.math_subject = Subject.objects.create(name='Mathematics')
        self.physics_subject = Subject.objects.create(name='Physics')
        
        self.tutor1 = User.objects.create_user(
            username='math_tutor',
            first_name='John',
            last_name='Doe',
            role='tutor',
            rating=4.5,
            bio='Experienced math teacher'
        )
        
        self.tutor2 = User.objects.create_user(
            username='physics_tutor',
            first_name='Jane',
            last_name='Smith',
            role='tutor',
            rating=4.8,
            bio='Physics expert'
        )
        
        TutorSubject.objects.create(tutor=self.tutor1, subject=self.math_subject)
        TutorSubject.objects.create(tutor=self.tutor2, subject=self.physics_subject)
        
    def test_tutor_list(self):
        """Öğretmen listesi testi"""
        url = reverse('tutor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_tutor_filter_by_subject(self):
        """Ders konusuna göre öğretmen filtreleme"""
        url = reverse('tutor-list')
        response = self.client.get(url, {'tutor_subjects__subject': self.math_subject.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['username'], 'math_tutor')
        
    def test_tutor_search(self):
        """Öğretmen arama testi"""
        url = reverse('tutor-list')
        response = self.client.get(url, {'search': 'John'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_tutor_ordering(self):
        """Öğretmen sıralama testi"""
        url = reverse('tutor-list')
        response = self.client.get(url, {'ordering': '-rating'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['rating'], 4.8)
