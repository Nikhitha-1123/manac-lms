from django.contrib import admin
from .models import Student, Session, Attendance, Assessment, StudentAssessment, Project, StudyMaterial, Certificate, JobOpening, JobApplication, Notification

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'college', 'branch', 'year')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'full_name')
    list_filter = ('branch', 'year', 'college')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'start_time', 'end_time', 'mentor', 'is_completed')
    list_filter = ('date', 'is_completed', 'mentor')
    search_fields = ('title', 'description', 'mentor')
    ordering = ('-date', '-start_time')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'is_present', 'marked_at')
    list_filter = ('is_present', 'session__date', 'marked_at')
    search_fields = ('student__user__username', 'student__full_name', 'session__title')

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'total_marks', 'duration_minutes', 'is_active')
    list_filter = ('is_active', 'due_date')
    search_fields = ('title', 'description')

@admin.register(StudentAssessment)
class StudentAssessmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'assessment', 'score', 'is_completed', 'submitted_at')
    list_filter = ('is_completed', 'assessment__due_date', 'submitted_at')
    search_fields = ('student__user__username', 'student__full_name', 'assessment__title')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'submitted_at', 'github_url', 'live_demo_url')
    list_filter = ('submitted_at',)
    search_fields = ('student__user__username', 'student__full_name', 'title', 'description')

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_type', 'uploaded_by', 'uploaded_at', 'file_size')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('title', 'description', 'uploaded_by__username')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'issued_date', 'verification_code')
    list_filter = ('issued_date',)
    search_fields = ('student__user__username', 'student__full_name', 'title', 'verification_code')

@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'salary_range', 'is_active', 'posted_at')
    list_filter = ('is_active', 'location', 'posted_at')
    search_fields = ('title', 'company', 'description', 'requirements')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job_opening', 'applied_at', 'status')
    list_filter = ('status', 'applied_at', 'job_opening__company')
    search_fields = ('student__user__username', 'student__full_name', 'job_opening__title')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('student__user__username', 'student__full_name', 'title', 'message')
