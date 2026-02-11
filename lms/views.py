from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import models
from .models import Student, Session, Attendance, Assessment, StudentAssessment, Project, StudyMaterial, Certificate, JobOpening, JobApplication, Notification, OfferLetter, MockTest, StudentMockTest, MockInterview
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO

@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('lms:login')

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

    # Sample data for stats
    attendance_percentage = 85.5
    total_sessions = 20
    attended_sessions = 17
    total_assessments = 10
    completed_assessments = 7

    # Sample recent activity
    recent_projects = [
        {'title': 'E-commerce Website', 'submitted_at': timezone.now() - timezone.timedelta(days=2)},
        {'title': 'Portfolio Site', 'submitted_at': timezone.now() - timezone.timedelta(days=5)},
        {'title': 'Blog Application', 'submitted_at': timezone.now() - timezone.timedelta(days=7)},
    ]
    recent_sessions = [
        {'session': {'title': 'Introduction to Django'}, 'marked_at': timezone.now() - timezone.timedelta(days=1)},
        {'session': {'title': 'React Basics'}, 'marked_at': timezone.now() - timezone.timedelta(days=3)},
        {'session': {'title': 'Database Design'}, 'marked_at': timezone.now() - timezone.timedelta(days=6)},
    ]

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

    # Fetch real mock interviews from database (exclude scheduled interviews)
    mock_interviews_queryset = MockInterview.objects.filter(student=student).exclude(status='scheduled')
    mock_interviews = []

    for interview in mock_interviews_queryset:
        mock_interviews.append({
            'id': interview.id,
            'title': interview.title,
            'status': interview.status,
            'status_display': interview.get_status_display(),
            'date': interview.scheduled_date.strftime('%Y-%m-%d') if interview.scheduled_date else interview.requested_date.strftime('%Y-%m-%d'),
            'feedback': interview.feedback if interview.feedback else '',
            'scheduled_date': interview.scheduled_date,
            'requested_date': interview.requested_date,
        })

    # Fetch real mock tests from database
    mock_tests_queryset = MockTest.objects.filter(is_active=True)
    mock_tests = []

    for mock_test in mock_tests_queryset:
        # Get the best attempt (highest score) for this student and mock test
        best_attempt = StudentMockTest.objects.filter(
            student=student,
            mock_test=mock_test,
            is_completed=True
        ).order_by('-score').first()

        if best_attempt:
            # Count total attempts
            total_attempts = StudentMockTest.objects.filter(
                student=student,
                mock_test=mock_test,
                is_completed=True
            ).count()

            mock_tests.append({
                'id': mock_test.id,
                'title': mock_test.title,
                'score': best_attempt.percentage_score,
                'date': best_attempt.submitted_at.strftime('%Y-%m-%d') if best_attempt.submitted_at else None,
                'attempts': total_attempts,
            })
        else:
            mock_tests.append({
                'id': mock_test.id,
                'title': mock_test.title,
                'status': 'pending',
            })

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
def quiz(request, mock_test_id=None):
    if mock_test_id:
        mock_test = get_object_or_404(MockTest, id=mock_test_id, is_active=True)
        context = {
            'mock_test': mock_test,
            'questions': json.dumps(mock_test.questions),
            'duration_minutes': mock_test.duration_minutes,
        }
    else:
        # Default quiz (existing behavior)
        default_questions = [
            {
                'question': 'What is the output of print(2 + 3)?',
                'options': ['5', '23', 'Error', 'None'],
                'correct': '5'
            },
            {
                'question': 'Which keyword is used to define a function in Python?',
                'options': ['def', 'function', 'fun', 'define'],
                'correct': 'def'
            },
            {
                'question': 'What does the len() function return?',
                'options': ['Length of a string or list', 'Type of variable', 'Memory usage', 'File size'],
                'correct': 'Length of a string or list'
            },
            {
                'question': 'Which data type is mutable in Python?',
                'options': ['List', 'Tuple', 'String', 'Integer'],
                'correct': 'List'
            },
            {
                'question': 'What is the correct way to comment in Python?',
                'options': ['# This is a comment', '// This is a comment', '/* This is a comment */', '-- This is a comment'],
                'correct': '# This is a comment'
            },
            {
                'question': 'Which statement is used for conditional execution?',
                'options': ['if', 'for', 'while', 'def'],
                'correct': 'if'
            },
            {
                'question': 'What is the built-in function to get user input?',
                'options': ['print', 'input', 'read', 'get'],
                'correct': 'input'
            },
            {
                'question': 'What is the result of 3 * 2?',
                'options': ['6', '32', 'Error', 'None'],
                'correct': '6'
            },
            {
                'question': 'Which symbol is used for string concatenation?',
                'options': ['+', '-', '*', '/'],
                'correct': '+'
            },
            {
                'question': 'What does the break statement do?',
                'options': ['Ends a loop prematurely', 'Starts a loop', 'Skips to next iteration', 'Ends the program'],
                'correct': 'Ends a loop prematurely'
            }
        ]
        context = {
            'questions': json.dumps(default_questions),
            'duration_minutes': 45,
        }
    return render(request, 'lms/quiz.html', context)

@login_required
def quiz_submit(request, mock_test_id=None):
    if request.method == 'POST':
        # Ensure student exists
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

        import json
        answers_str = request.POST.get('answers', '{}')
        try:
            answers = json.loads(answers_str) if answers_str else {}
        except json.JSONDecodeError:
            answers = {}

        if mock_test_id:
            # Handle mock test submission
            mock_test = get_object_or_404(MockTest, id=mock_test_id, is_active=True)
            questions = mock_test.questions

            score = 0
            total_questions = len(questions)
            results = []

            for i, question in enumerate(questions):
                user_answer = answers.get(str(i), '')
                correct = question['correct']
                is_correct = user_answer == correct
                if is_correct:
                    score += 1
                results.append({
                    'question_number': i + 1,
                    'user_answer': user_answer,
                    'correct_answer': correct,
                    'is_correct': is_correct
                })

            percentage = (score / total_questions) * 100 if total_questions > 0 else 0
            incorrect = total_questions - score

            # Get the next attempt number for this student and mock test
            last_attempt = StudentMockTest.objects.filter(
                student=student,
                mock_test=mock_test
            ).order_by('-attempt_number').first()

            attempt_number = (last_attempt.attempt_number + 1) if last_attempt else 1

            # Save to StudentMockTest (always create new record for each attempt)
            student_mock_test = StudentMockTest.objects.create(
                student=student,
                mock_test=mock_test,
                score=score,
                max_score=mock_test.total_marks,
                answers=answers,
                submitted_at=timezone.now(),
                is_completed=True,
                attempt_number=attempt_number
            )

            context = {
                'mock_test': mock_test,
                'score': score,
                'total_questions': total_questions,
                'percentage': round(percentage, 1),
                'incorrect': incorrect,
                'results': results
            }
        else:
            # Default quiz (existing behavior)
            questions = [
                {'correct': '14'},
                {'correct': 'def'},
                {'correct': 'Returns the length of a string or list'},
                {'correct': 'List'},
                {'correct': '# This is a comment'},
                {'correct': 'Executes code if a condition is true'},
                {'correct': 'print'},
                {'correct': '3'},
                {'correct': '[]'},
                {'correct': 'Ends a loop prematurely'}
            ]

            score = 0
            total_questions = len(questions)
            results = []

            for i, question in enumerate(questions):
                user_answer = answers.get(str(i), '')
                correct = question['correct']
                is_correct = user_answer == correct
                if is_correct:
                    score += 1
                results.append({
                    'question_number': i + 1,
                    'user_answer': user_answer,
                    'correct_answer': correct,
                    'is_correct': is_correct
                })

            percentage = (score / total_questions) * 100
            incorrect = total_questions - score

            # Save to database
            assessment, created = Assessment.objects.get_or_create(
                title='Python Basics Quiz',
                defaults={
                    'description': 'Test your knowledge of Python fundamentals',
                    'topic': 'Python Programming',
                    'total_marks': 10,
                    'duration_minutes': 45,
                    'due_date': timezone.now() + timezone.timedelta(days=30),
                    'is_active': True
                }
            )

            student_assessment, created = StudentAssessment.objects.get_or_create(
                student=student,
                assessment=assessment,
                defaults={
                    'max_score': 10,
                    'answers': answers,
                    'submitted_at': timezone.now(),
                    'is_completed': True
                }
            )
            student_assessment.score = score
            student_assessment.answers = answers
            student_assessment.submitted_at = timezone.now()
            student_assessment.is_completed = True
            student_assessment.save()

            context = {
                'score': score,
                'total_questions': total_questions,
                'percentage': round(percentage, 1),
                'incorrect': incorrect,
                'results': results
            }

        return render(request, 'lms/quiz_results.html', context)

    return JsonResponse({'error': 'Invalid request method'})

@login_required
def schedule_mock_interview(request):
    if request.method == 'POST':
        student = get_object_or_404(Student, user=request.user)
        title = request.POST.get('title')
        description = request.POST.get('description')
        requested_date_str = request.POST.get('scheduled_date')

        if title and requested_date_str:
            from datetime import datetime
            requested_date = datetime.strptime(requested_date_str, '%Y-%m-%dT%H:%M')
            MockInterview.objects.create(
                student=student,
                title=title,
                description=description,
                requested_date=requested_date,
                status='requested'
            )
            return JsonResponse({'success': True, 'message': 'Mock interview request submitted successfully!'})

        return JsonResponse({'success': False, 'message': 'Please provide all required fields.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required
def cancel_mock_interview(request, interview_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, user=request.user)
        interview = get_object_or_404(MockInterview, id=interview_id, student=student, status='requested')
        interview.delete()
        return JsonResponse({'success': True, 'message': 'Mock interview request cancelled successfully!'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required
def download_offer_letter(request):
    student = get_object_or_404(Student, user=request.user)
    offer_letter = OfferLetter.objects.filter(student=student).order_by('-issued_date').first()
    if not offer_letter:
        raise Http404("Offer letter not found")

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
