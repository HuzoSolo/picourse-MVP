from rest_framework import permissions


class IsStudentOrReadOnly(permissions.BasePermission):
    """
    Yalnızca öğrencilerin yazma izni olduğu permission
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated and request.user.role == 'student'


class IsTutorOrReadOnly(permissions.BasePermission):
    """
    Yalnızca öğretmenlerin yazma izni olduğu permission
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated and request.user.role == 'tutor'


class IsOwnerOrTutorForLessonRequest(permissions.BasePermission):
    """
    Ders talebi için özel permission:
    - Öğrenci kendi oluşturduğu talepleri görebilir
    - Öğretmen kendine yapılan talepleri görebilir ve durumlarını güncelleyebilir
    """
    def has_object_permission(self, request, view, obj):
        # Okuma izni: öğrenci kendi talepleri, öğretmen kendine yapılan talepler
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return (obj.student == request.user or obj.tutor == request.user)
        
        # Güncelleme izni: sadece öğretmen kendi taleplerine cevap verebilir
        if request.method in ['PUT', 'PATCH']:
            return (request.user.role == 'tutor' and obj.tutor == request.user)
        
        return False


class IsOwner(permissions.BasePermission):
    """
    Yalnızca nesnenin sahibi işlem yapabilir
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user or obj.user == request.user
