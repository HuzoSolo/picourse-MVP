from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apiService.models import Subject, TutorSubject, LessonRequest
from datetime import datetime, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Veritabanına örnek veri ekler (öğrenci, öğretmen, ders konuları)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Mevcut verileri temizler ve yeni veri ekler',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Mevcut veriler temizleniyor...')
            LessonRequest.objects.all().delete()
            TutorSubject.objects.all().delete()
            Subject.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Mevcut veriler temizlendi.'))

        # Ders konuları oluştur
        self.stdout.write('Ders konuları oluşturuluyor...')
        subjects_data = [
            {
                'name': 'Matematik',
                'description': 'Temel matematik, cebir, geometri ve analiz konuları'
            },
            {
                'name': 'Fizik',
                'description': 'Klasik fizik, modern fizik ve uygulamalı fizik'
            },
            {
                'name': 'Kimya',
                'description': 'Genel kimya, organik ve inorganik kimya'
            },
            {
                'name': 'İngilizce',
                'description': 'İngilizce dil bilgisi, konuşma ve yazma becerileri'
            },
            {
                'name': 'Tarih',
                'description': 'Türk tarihi, dünya tarihi ve tarih metodolojisi'
            }
        ]

        subjects = []
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                name=subject_data['name'],
                defaults={'description': subject_data['description']}
            )
            subjects.append(subject)
            if created:
                self.stdout.write(f'  ✓ {subject.name} ders konusu oluşturuldu')

        # Öğretmenler oluştur
        self.stdout.write('Öğretmenler oluşturuluyor...')
        tutors_data = [
            {
                'username': 'ahmet_ogretmen',
                'email': 'ahmet@example.com',
                'first_name': 'Ahmet',
                'last_name': 'Yılmaz',
                'bio': 'Matematik alanında 10 yıllık deneyime sahip. Üniversite hazırlık kurslarında ders vermekteyim.',
                'rating': 4.8,
                'total_lessons': 150,
                'subjects': ['Matematik', 'Fizik']
            },
            {
                'username': 'fatma_ogretmen',
                'email': 'fatma@example.com',
                'first_name': 'Fatma',
                'last_name': 'Demir',
                'bio': 'İngilizce öğretmeniyim. TOEFL ve IELTS hazırlık kursları veriyorum.',
                'rating': 4.9,
                'total_lessons': 200,
                'subjects': ['İngilizce']
            },
            {
                'username': 'mehmet_ogretmen',
                'email': 'mehmet@example.com',
                'first_name': 'Mehmet',
                'last_name': 'Kaya',
                'bio': 'Kimya ve Fizik alanlarında uzmanım. Üniversite öğrencilerine ders veriyorum.',
                'rating': 4.6,
                'total_lessons': 85,
                'subjects': ['Kimya', 'Fizik']
            },
            {
                'username': 'ayse_ogretmen',
                'email': 'ayse@example.com',
                'first_name': 'Ayşe',
                'last_name': 'Öztürk',
                'bio': 'Tarih öğretmeniyim. LYS ve TYT hazırlık konularında deneyimliyim.',
                'rating': 4.7,
                'total_lessons': 120,
                'subjects': ['Tarih']
            },
            {
                'username': 'ali_ogretmen',
                'email': 'ali@example.com',
                'first_name': 'Ali',
                'last_name': 'Çelik',
                'bio': 'Matematik ve Fizik dersleri veriyorum. Özellikle sayısal konularda uzmanım.',
                'rating': 4.5,
                'total_lessons': 95,
                'subjects': ['Matematik', 'Fizik']
            }
        ]

        tutors = []
        for tutor_data in tutors_data:
            tutor, created = User.objects.get_or_create(
                username=tutor_data['username'],
                defaults={
                    'email': tutor_data['email'],
                    'first_name': tutor_data['first_name'],
                    'last_name': tutor_data['last_name'],
                    'role': 'tutor',
                    'bio': tutor_data['bio'],
                    'rating': tutor_data['rating'],
                    'total_lessons': tutor_data['total_lessons']
                }
            )
            if created:
                tutor.set_password('password123')
                tutor.save()
                
                # Öğretmenin ders konularını ekle
                for subject_name in tutor_data['subjects']:
                    subject = Subject.objects.get(name=subject_name)
                    TutorSubject.objects.create(
                        tutor=tutor,
                        subject=subject,
                        experience_years=random.randint(2, 15)
                    )
                
                tutors.append(tutor)
                self.stdout.write(f'  ✓ {tutor.get_full_name()} öğretmen oluşturuldu')

        # Öğrenciler oluştur
        self.stdout.write('Öğrenciler oluşturuluyor...')
        students_data = [
            {
                'username': 'can_ogrenci',
                'email': 'can@example.com',
                'first_name': 'Can',
                'last_name': 'Yıldız',
                'grade_level': 11,
                'bio': '11. sınıf öğrencisiyim. Üniversite sınavına hazırlanıyorum.'
            },
            {
                'username': 'elif_ogrenci',
                'email': 'elif@example.com',
                'first_name': 'Elif',
                'last_name': 'Aydın',
                'grade_level': 12,
                'bio': '12. sınıf öğrencisiyim. Matematik ve fen bilimlerinde destek istiyorum.'
            },
            {
                'username': 'berk_ogrenci',
                'email': 'berk@example.com',
                'first_name': 'Berk',
                'last_name': 'Çakır',
                'grade_level': 10,
                'bio': '10. sınıf öğrencisiyim. İngilizce konularında yardıma ihtiyacım var.'
            }
        ]

        students = []
        for student_data in students_data:
            student, created = User.objects.get_or_create(
                username=student_data['username'],
                defaults={
                    'email': student_data['email'],
                    'first_name': student_data['first_name'],
                    'last_name': student_data['last_name'],
                    'role': 'student',
                    'grade_level': student_data['grade_level'],
                    'bio': student_data['bio']
                }
            )
            if created:
                student.set_password('password123')
                student.save()
                students.append(student)
                self.stdout.write(f'  ✓ {student.get_full_name()} öğrenci oluşturuldu')

        # Örnek ders talepleri oluştur
        self.stdout.write('Örnek ders talepleri oluşturuluyor...')
        if students and tutors:
            lesson_requests_data = [
                {
                    'student': students[0],  # Can
                    'tutor': tutors[0],      # Ahmet (Matematik)
                    'subject': Subject.objects.get(name='Matematik'),
                    'message': 'Matematik dersinde limit ve türev konularında yardıma ihtiyacım var.',
                    'status': 'pending',
                    'duration_hours': 2
                },
                {
                    'student': students[1],  # Elif
                    'tutor': tutors[1],      # Fatma (İngilizce)
                    'subject': Subject.objects.get(name='İngilizce'),
                    'message': 'İngilizce yazma becerilerimi geliştirmek istiyorum.',
                    'status': 'approved',
                    'duration_hours': 1
                },
                {
                    'student': students[2],  # Berk
                    'tutor': tutors[2],      # Mehmet (Kimya)
                    'subject': Subject.objects.get(name='Kimya'),
                    'message': 'Organik kimya konularında zorlanıyorum.',
                    'status': 'pending',
                    'duration_hours': 2
                },
                {
                    'student': students[0],  # Can
                    'tutor': tutors[3],      # Ayşe (Tarih)
                    'subject': Subject.objects.get(name='Tarih'),
                    'message': 'Osmanlı tarihi konularında desteğe ihtiyacım var.',
                    'status': 'rejected',
                    'duration_hours': 1
                }
            ]

            for req_data in lesson_requests_data:
                lesson_request = LessonRequest.objects.create(
                    student=req_data['student'],
                    tutor=req_data['tutor'],
                    subject=req_data['subject'],
                    message=req_data['message'],
                    status=req_data['status'],
                    preferred_date=datetime.now() + timedelta(days=random.randint(1, 14)),
                    duration_hours=req_data['duration_hours']
                )
                self.stdout.write(f'  ✓ {lesson_request.student.first_name} -> {lesson_request.tutor.first_name} ders talebi oluşturuldu')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Seed data başarıyla oluşturuldu!\n'
                f'  - {Subject.objects.count()} ders konusu\n'
                f'  - {User.objects.filter(role="tutor").count()} öğretmen\n'
                f'  - {User.objects.filter(role="student").count()} öğrenci\n'
                f'  - {LessonRequest.objects.count()} ders talebi\n'
                f'\nTest kullanıcıları şifresi: password123'
            )
        )
