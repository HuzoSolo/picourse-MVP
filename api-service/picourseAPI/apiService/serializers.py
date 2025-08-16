from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, Subject, TutorSubject, LessonRequest


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Kullanıcı kayıt serializer'ı
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 
                 'last_name', 'role', 'bio', 'grade_level')
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Şifreler eşleşmiyor.")
        return attrs
    
    def validate_role(self, value):
        if value not in ['student', 'tutor']:
            raise serializers.ValidationError("Geçersiz rol. 'student' veya 'tutor' seçiniz.")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Kullanıcı giriş serializer'ı
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Geçersiz kullanıcı adı veya şifre.")
            if not user.is_active:
                raise serializers.ValidationError("Kullanıcı hesabı deaktif.")
            attrs['user'] = user
        else:
            raise serializers.ValidationError("Kullanıcı adı ve şifre gerekli.")
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Kullanıcı profil serializer'ı
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    grade_level_display = serializers.CharField(source='get_grade_level_display', read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 
                 'role_display', 'bio', 'grade_level', 'grade_level_display', 
                 'rating', 'total_lessons', 'date_joined')
        read_only_fields = ('id', 'username', 'role', 'rating', 'total_lessons', 'date_joined')


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Kullanıcı profil güncelleme serializer'ı
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'bio', 'grade_level')


class SubjectSerializer(serializers.ModelSerializer):
    """
    Ders konuları serializer'ı
    """
    class Meta:
        model = Subject
        fields = ('id', 'name', 'description', 'created_at')


class TutorSubjectSerializer(serializers.ModelSerializer):
    """
    Öğretmen ders uzmanlığı serializer'ı
    """
    subject = SubjectSerializer(read_only=True)
    
    class Meta:
        model = TutorSubject
        fields = ('subject', 'experience_years')


class TutorListSerializer(serializers.ModelSerializer):
    """
    Öğretmen listesi için serializer
    """
    subjects = TutorSubjectSerializer(source='tutor_subjects', many=True, read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'role', 'role_display',
                 'bio', 'rating', 'total_lessons', 'subjects')


class TutorDetailSerializer(serializers.ModelSerializer):
    """
    Öğretmen detay serializer'ı
    """
    subjects = TutorSubjectSerializer(source='tutor_subjects', many=True, read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    grade_level_display = serializers.CharField(source='get_grade_level_display', read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role', 
                 'role_display', 'bio', 'grade_level', 'grade_level_display',
                 'rating', 'total_lessons', 'subjects', 'date_joined')


class LessonRequestCreateSerializer(serializers.ModelSerializer):
    """
    Ders talebi oluşturma serializer'ı
    """
    class Meta:
        model = LessonRequest
        fields = ('tutor', 'subject', 'message', 'preferred_date', 'duration_hours')
    
    def validate_tutor(self, value):
        if value.role != 'tutor':
            raise serializers.ValidationError("Seçilen kullanıcı öğretmen değil.")
        return value
    
    def create(self, validated_data):
        # student bilgisini request'ten al
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)


class LessonRequestSerializer(serializers.ModelSerializer):
    """
    Ders talebi serializer'ı
    """
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_username = serializers.CharField(source='student.username', read_only=True)
    tutor_name = serializers.CharField(source='tutor.get_full_name', read_only=True)
    tutor_username = serializers.CharField(source='tutor.username', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = LessonRequest
        fields = ('id', 'student', 'student_name', 'student_username', 'tutor', 
                 'tutor_name', 'tutor_username', 'subject', 'subject_name', 'status', 
                 'status_display', 'message', 'preferred_date', 'duration_hours', 
                 'created_at', 'updated_at')
        read_only_fields = ('id', 'student', 'created_at', 'updated_at')


class LessonRequestUpdateSerializer(serializers.ModelSerializer):
    """
    Ders talebi durum güncelleme serializer'ı (öğretmen için)
    """
    class Meta:
        model = LessonRequest
        fields = ('status',)
    
    def validate_status(self, value):
        if value not in ['approved', 'rejected']:
            raise serializers.ValidationError("Durum 'approved' veya 'rejected' olmalı.")
        return value
