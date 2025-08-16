from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Subject, TutorSubject, LessonRequest


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Özel kullanıcı admin paneli
    """
    list_display = ('username', 'email', 'role', 'rating', 'total_lessons', 'is_active')
    list_filter = ('role', 'is_active', 'grade_level')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Ek Bilgiler', {
            'fields': ('role', 'bio', 'grade_level', 'rating', 'total_lessons')
        }),
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Ders konuları admin paneli
    """
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(TutorSubject)
class TutorSubjectAdmin(admin.ModelAdmin):
    """
    Öğretmen-Ders ilişkisi admin paneli
    """
    list_display = ('tutor', 'subject', 'experience_years')
    list_filter = ('subject', 'experience_years')
    search_fields = ('tutor__username', 'subject__name')


@admin.register(LessonRequest)
class LessonRequestAdmin(admin.ModelAdmin):
    """
    Ders talepleri admin paneli
    """
    list_display = ('student', 'tutor', 'subject', 'status', 'preferred_date', 'created_at')
    list_filter = ('status', 'subject', 'created_at')
    search_fields = ('student__username', 'tutor__username', 'subject__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
