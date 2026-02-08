from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import models
from .models import Student, Session, Attendance, Assessment, StudentAssessment, Project, StudyMaterial, Certificate, JobOpening, JobApplication, Notification, OfferLetter
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO

def dashboard(request):
    student, created = Student.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': request.user.get_full_name() or request.user.username,
            'college': 'Default College',
            'branch': 'Computer Science',
            'year': '1st',
            'enrollment_date': timezone.now().date()
        }
    )

    # Get recent sessions
    upcoming_sessions = Session.objects.filter(date__gte=timezone.now().date(), is_completed=False).order_by('date', 'start_time')[:3]

    # Get attendance stats
    total_sessions = Session.objects.filter(is_completed=True).count()
    attended_sessions = Attendance.objects.filter(student=student, is_present=True).count()
    attendance_percentage = (attended_sessions / total_sessions * 100) if total_sessions > 0 else 0

    # Get assessment stats
    total_assessments = Assessment.objects.filter(is_active=True).count()
    completed_assessments = StudentAssessment.objects.filter(student=student, is_completed=True).count()

    # Get recent activity
    recent_projects = Project.objects.filter(student=student).order_by('-submitted_at')[:3]
    recent_sessions = Attendance.objects.filter(student=student, is_present=True).order_by('-session__date')[:3]

    context = {
        'student': student,
        'upcoming_sessions': upcoming_sessions,
        'attendance_percentage': round(attendance_percentage, 1),
        'total_sessions': total_sessions,
        'attended_sessions': attended_sessions,
        'total_assessments': total_assessments,
        'completed_assessments': completed_assessments,
        'recent_projects': recent_projects,
        'recent_sessions': recent_sessions,
    }

    return render(request, 'lms/dashboard.html', context)

@login_required
def offer_letter(request):
    student = get_object_or_404(Student, user=request.user)
    offer_letter = OfferLetter.objects.filter(student=student).order_by('-issued_date').first()
    if not offer_letter:
        offer_letter = OfferLetter.objects.create(
            student=student,
            title='Full Stack Developer Intern',
            company='Manac Infotech Pvt Ltd',
            start_date=timezone.now().date() + timezone.timedelta(days=30),
            compensation=15000.00,
            reporting_to='Senior Engineering Manager',
            location='Hyderabad (Hybrid)',
        )
    context = {'student': student, 'offer_letter': offer_letter}
    return render(request, 'lms/offer_letter.html', context)

@login_required
def session_details(request):
    sessions = Session.objects.all().order_by('-date')
    context = {'sessions': sessions}
    return render(request, 'lms/session_details.html', context)

@login_required
def session_recordings(request):
    recordings = Session.objects.filter(recording_url__isnull=False).order_by('-date')
    context = {'recordings': recordings}
    return render(request, 'lms/session_recordings.html', context)

@login_required
def attendance(request):
    student = get_object_or_404(Student, user=request.user)
    attendances = Attendance.objects.filter(student=student).select_related('session').order_by('-session__date')

    total_sessions = attendances.count()
    present_count = attendances.filter(is_present=True).count()
    absent_count = total_sessions - present_count
    attendance_rate = (present_count / total_sessions * 100) if total_sessions > 0 else 0

    context = {
        'attendances': attendances,
        'total_sessions': total_sessions,
        'present_count': present_count,
        'absent_count': absent_count,
        'attendance_rate': round(attendance_rate, 1),
    }
    return render(request, 'lms/attendance.html', context)

@login_required
def project_details(request):
    student = get_object_or_404(Student, user=request.user)
    projects = Project.objects.filter(student=student).order_by('-submitted_at')
    context = {'projects': projects, 'student': student}
    return render(request, 'lms/project_details.html', context)

@login_required
def assessment(request):
    student = get_object_or_404(Student, user=request.user)
    assessments = Assessment.objects.filter(is_active=True)
    student_assessments = StudentAssessment.objects.filter(student=student, assessment__in=assessments).select_related('assessment')

    # Create StudentAssessment objects for assessments not yet taken
    for assessment in assessments:
        if not student_assessments.filter(assessment=assessment).exists():
            StudentAssessment.objects.create(student=student, assessment=assessment)

    student_assessments = StudentAssessment.objects.filter(student=student, assessment__in=assessments).select_related('assessment')

    pending_count = student_assessments.filter(is_completed=False, assessment__due_date__gte=timezone.now().date()).count()
    completed_count = student_assessments.filter(is_completed=True).count()
    average_score = student_assessments.filter(is_completed=True, score__isnull=False).aggregate(avg=models.Avg('score')).get('avg', 0) or 0

    context = {
        'student_assessments': student_assessments,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'average_score': round(average_score, 1),
    }
    return render(request, 'lms/assessment.html', context)

@login_required
def study_material(request):
    materials = StudyMaterial.objects.all().order_by('-uploaded_at')
    context = {'materials': materials}
    return render(request, 'lms/study_material.html', context)

@login_required
def certificate(request):
    student = get_object_or_404(Student, user=request.user)
    certificates = Certificate.objects.filter(student=student).order_by('-issued_date')
    context = {'certificates': certificates, 'student': student}
    return render(request, 'lms/certificate.html', context)

@login_required
def placement_form(request):
    student = get_object_or_404(Student, user=request.user)
    job_openings = JobOpening.objects.filter(is_active=True)
    applications = JobApplication.objects.filter(student=student).select_related('job_opening')

    if request.method == 'POST':
        selected_jobs = request.POST.getlist('job_opening')
        for job_id in selected_jobs:
            job = get_object_or_404(JobOpening, id=job_id)
            if not applications.filter(job_opening=job).exists():
                JobApplication.objects.create(student=student, job_opening=job)

        # Update student profile
        student.phone = request.POST.get('phone', student.phone)
        student.address = request.POST.get('address', student.address)
        student.linkedin_profile = request.POST.get('linkedin', student.linkedin_profile)
        student.github_profile = request.POST.get('github', student.github_profile)
        student.portfolio = request.POST.get('portfolio', student.portfolio)
        student.save()

        return JsonResponse({'success': True, 'message': 'Application submitted successfully!'})

    context = {
        'job_openings': job_openings,
        'student': student,
        'applications': applications,
    }
    return render(request, 'lms/placement_form.html', context)

@login_required
def placement_readiness(request):
    student = get_object_or_404(Student, user=request.user)

    # Mock readiness score calculation
    readiness_score = 75  # This could be calculated based on various factors

    # Mock checklist items
    checklist = [
        {'item': 'Resume Review', 'completed': True},
        {'item': 'Mock Interview 1', 'completed': True},
        {'item': 'Mock Interview 2', 'completed': False},
        {'item': 'Portfolio Project', 'completed': True},
    ]

    # Mock mock interviews
    mock_interviews = [
        {'title': 'Technical Round 1', 'status': 'completed', 'date': '2023-10-20', 'feedback': 'Strong in JS, need work on CSS Grid.'},
        {'title': 'HR Round', 'status': 'upcoming', 'date': '2023-11-05'},
    ]

    # Mock mock tests
    mock_tests = [
        {'title': 'Aptitude Series A', 'score': 85, 'date': '2023-10-15'},
        {'title': 'Reasoning Test', 'score': 78, 'date': '2023-10-18'},
        {'title': 'React Technical Assessment', 'status': 'pending'},
        {'title': 'JavaScript Fundamentals', 'score': 92, 'date': '2023-10-20'},
        {'title': 'Data Structures & Algorithms', 'status': 'pending'},
    ]

    context = {
        'readiness_score': readiness_score,
        'checklist': checklist,
        'mock_interviews': mock_interviews,
        'mock_tests': mock_tests,
    }
    return render(request, 'lms/placement_readiness.html', context)

@login_required
def profile(request):
    student = get_object_or_404(Student, user=request.user)
    context = {'student': student}
    return render(request, 'lms/profile.html', context)

@login_required
def edit_profile(request):
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        # Update user fields
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.save()

        # Update student fields
        student.full_name = request.user.get_full_name()
        student.phone = request.POST.get('phone', student.phone)
        student.date_of_birth = request.POST.get('date_of_birth') or None
        student.address = request.POST.get('address', student.address)
        student.college = request.POST.get('college', student.college)
        student.branch = request.POST.get('branch', student.branch)
        student.year = request.POST.get('year', student.year)
        student.linkedin_profile = request.POST.get('linkedin_profile', student.linkedin_profile)
        student.github_profile = request.POST.get('github_profile', student.github_profile)
        student.portfolio = request.POST.get('portfolio', student.portfolio)
        student.save()
        return JsonResponse({'success': True, 'message': 'Profile updated successfully!'})

    context = {'student': student}
    return render(request, 'lms/edit_profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            return JsonResponse({'success': False, 'message': 'Current password is incorrect.'})

        if new_password != confirm_password:
            return JsonResponse({'success': False, 'message': 'New passwords do not match.'})

        request.user.set_password(new_password)
        request.user.save()
        return JsonResponse({'success': True, 'message': 'Password changed successfully!'})

    return render(request, 'lms/change_password.html')

@csrf_exempt
@login_required
def submit_project(request):
    if request.method == 'POST':
        student = get_object_or_404(Student, user=request.user)
        data = json.loads(request.body)

        Project.objects.create(
            student=student,
            title=data.get('title', 'Project Submission'),
            description=data.get('description', ''),
            github_url=data.get('github_url', ''),
            live_demo_url=data.get('live_demo_url', ''),
        )

        return JsonResponse({'success': True, 'message': 'Project submitted successfully!'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required
def notifications(request):
    student = get_object_or_404(Student, user=request.user)
    notifications = Notification.objects.filter(student=student).order_by('-created_at')
    context = {'notifications': notifications}
    return render(request, 'lms/notifications.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('lms:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'lms/login.html')

def logout_view(request):
    logout(request)
    return redirect('lms:login')

@login_required
def download_offer_letter(request):
    student = get_object_or_404(Student, user=request.user)
    offer_letter = get_object_or_404(OfferLetter, student=student)

    # Create a buffer for the PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Define custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Center alignment
    )
    company_style = ParagraphStyle(
        'Company',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=20,
        alignment=1,
    )
    normal_style = styles['Normal']
    bold_style = styles['Heading4']

    # Build the PDF content
    content = []

    # Company header
    content.append(Paragraph("Manac Infotech Pvt Ltd", title_style))
    content.append(Paragraph("Excellence in Technology", company_style))
    content.append(Spacer(1, 0.5*inch))

    # Date
    content.append(Paragraph(f"Date: {offer_letter.issued_date.strftime('%B %d, %Y')}", normal_style))
    content.append(Spacer(1, 0.5*inch))

    # Salutation
    content.append(Paragraph(f"Dear {student.full_name},", bold_style))
    content.append(Spacer(1, 0.25*inch))

    # Body
    content.append(Paragraph(f"We are delighted to extend this offer of employment for the position of <b>{offer_letter.title}</b> with {offer_letter.company}. We were very impressed with your background and skills, and we are confident that you will make a significant contribution to our team.", normal_style))
    content.append(Spacer(1, 0.25*inch))

    # Offer details table
    data = [
        ['Start Date', offer_letter.start_date.strftime('%B %d, %Y')],
        ['Compensation', f"₹{offer_letter.compensation}/Month"],
        ['Reporting To', offer_letter.reporting_to],
        ['Location', offer_letter.location],
    ]

    table = Table(data, colWidths=[2*inch, 3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    content.append(table)
    content.append(Spacer(1, 0.25*inch))

    # Closing
    content.append(Paragraph("Please review the attached document for full terms and conditions. By accepting this offer, you agree to the policies and procedures of our company.", normal_style))
    content.append(Spacer(1, 0.5*inch))
    content.append(Paragraph("Sincerely,", normal_style))
    content.append(Paragraph("Manac Infotech Pvt Ltd", bold_style))

    # Build the PDF
    doc.build(content)

    # Get the PDF data
    pdf_data = buffer.getvalue()
    buffer.close()

    # Create the HTTP response
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="offer_letter_{student.full_name.replace(" ", "_")}.pdf"'

    return response
