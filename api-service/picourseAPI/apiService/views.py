from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import User, Subject, LessonRequest
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserUpdateSerializer, SubjectSerializer, TutorListSerializer, 
    TutorDetailSerializer, LessonRequestCreateSerializer, 
    LessonRequestSerializer, LessonRequestUpdateSerializer
)
from .permissions import IsStudentOrReadOnly, IsOwnerOrTutorForLessonRequest, IsOwner


@extend_schema(
    summary="Kullanıcı Kaydı",
    description="Yeni kullanıcı kaydı oluşturur (öğrenci veya öğretmen)",
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """
    Kullanıcı kayıt endpoint'i
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Kullanıcı başarıyla oluşturuldu.',
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Kullanıcı Girişi",
    description="JWT token ile kullanıcı girişi",
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    """
    Kullanıcı giriş endpoint'i
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Giriş başarılı.',
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Kullanıcı profil görüntüleme ve güncelleme
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserProfileSerializer


class SubjectListView(generics.ListAPIView):
    """
    Ders konuları listesi (herkese açık)
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]


class TutorListView(generics.ListAPIView):
    """
    Öğretmen listesi - filtreleme ve arama destekli
    """
    serializer_class = TutorListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tutor_subjects__subject']
    search_fields = ['username', 'first_name', 'last_name', 'bio']
    ordering_fields = ['rating', 'total_lessons', 'date_joined']
    ordering = ['-rating']
    
    def get_queryset(self):
        return User.objects.filter(role='tutor').prefetch_related('tutor_subjects__subject')
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='subject',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Ders konusu ID ile filtreleme'
            ),
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Öğretmen adı, soyadı veya biyografide arama'
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Sıralama: rating, -rating, total_lessons, -total_lessons'
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TutorDetailView(generics.RetrieveAPIView):
    """
    Öğretmen detay bilgileri
    """
    serializer_class = TutorDetailSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return User.objects.filter(role='tutor').prefetch_related('tutor_subjects__subject')


class LessonRequestCreateView(generics.CreateAPIView):
    """
    Ders talebi oluşturma (sadece öğrenciler)
    """
    serializer_class = LessonRequestCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lesson_request = serializer.save(student=request.user)
        return Response(
            LessonRequestSerializer(lesson_request).data,
            status=status.HTTP_201_CREATED
        )


class LessonRequestListView(generics.ListAPIView):
    """
    Ders talepleri listesi - rol bazlı filtreleme
    """
    serializer_class = LessonRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_queryset(self):
        user = self.request.user
        role = self.request.query_params.get('role')
        
        if role == 'student' and user.role == 'student':
            return LessonRequest.objects.filter(student=user)
        elif role == 'tutor' and user.role == 'tutor':
            return LessonRequest.objects.filter(tutor=user)
        else:
            # Varsayılan: kullanıcının kendi talepleri
            if user.role == 'student':
                return LessonRequest.objects.filter(student=user)
            elif user.role == 'tutor':
                return LessonRequest.objects.filter(tutor=user)
        
        return LessonRequest.objects.none()
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='role',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Rol bazlı filtreleme: student veya tutor',
                enum=['student', 'tutor']
            ),
            OpenApiParameter(
                name='status',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Durum bazlı filtreleme',
                enum=['pending', 'approved', 'rejected']
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LessonRequestUpdateView(generics.UpdateAPIView):
    """
    Ders talebi durum güncelleme (sadece öğretmenler)
    """
    serializer_class = LessonRequestUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrTutorForLessonRequest]
    
    def get_queryset(self):
        return LessonRequest.objects.filter(tutor=self.request.user)
    
    def perform_update(self, serializer):
        if self.request.user.role != 'tutor':
            return Response(
                {'error': 'Sadece öğretmenler ders taleplerini güncelleyebilir.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        lesson_request = self.get_object()
        if lesson_request.tutor != self.request.user:
            return Response(
                {'error': 'Bu talebi güncelleme yetkiniz yok.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save()
