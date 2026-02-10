import os
import django
from django.utils import timezone
from datetime import date, time, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manac_lms.settings')
django.setup()

from django.contrib.auth.models import User
from lms.models import Student, Session, Attendance, Assessment, StudentAssessment, Project, StudyMaterial, Notification

# Get or create a user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com'
    }
)
if created:
    user.set_password('password123')
    user.save()

# Get or create student
student, created = Student.objects.get_or_create(
    user=user,
    defaults={
        'full_name': 'Test User',
        'college': 'Test College',
        'branch': 'Computer Science',
        'year': '2nd',
        'enrollment_date': date.today() - timedelta(days=30)
    }
)

# Create additional students
additional_students_data = [
    {
        'username': 'student1',
        'first_name': 'Alice',
        'last_name': 'Johnson',
        'email': 'alice@example.com',
        'full_name': 'Alice Johnson',
        'college': 'Tech University',
        'branch': 'Information Technology',
        'year': '3rd'
    },
    {
        'username': 'student2',
        'first_name': 'Bob',
        'last_name': 'Smith',
        'email': 'bob@example.com',
        'full_name': 'Bob Smith',
        'college': 'Engineering College',
        'branch': 'Computer Engineering',
        'year': '2nd'
    },
    {
        'username': 'student3',
        'first_name': 'Charlie',
        'last_name': 'Brown',
        'email': 'charlie@example.com',
        'full_name': 'Charlie Brown',
        'college': 'Science Institute',
        'branch': 'Software Engineering',
        'year': '4th'
    }
]

additional_students = []
for student_data in additional_students_data:
    user_obj, created = User.objects.get_or_create(
        username=student_data['username'],
        defaults={
            'first_name': student_data['first_name'],
            'last_name': student_data['last_name'],
            'email': student_data['email']
        }
    )
    if created:
        user_obj.set_password('password123')
        user_obj.save()
    
    stud, created = Student.objects.get_or_create(
        user=user_obj,
        defaults={
            'full_name': student_data['full_name'],
            'college': student_data['college'],
            'branch': student_data['branch'],
            'year': student_data['year'],
            'enrollment_date': date.today() - timedelta(days=30)
        }
    )
    additional_students.append(stud)

# Clear existing sessions
Session.objects.all().delete()

# Create Sessions
sessions_data = [
    {
        'title': 'Introduction to HTML',
        'topic': 'HTML Basics',
        'mentor': 'John Doe',
        'date': date.today() - timedelta(days=10),
        'start_time': time(10, 0),
        'end_time': time(11, 0),
        'is_completed': True,
        'recording_url': 'https://www.youtube.com/live/tpVgfaWiftA?si=0fbUVDctUS6vqxbr'
    },
    {
        'title': 'CSS Fundamentals',
        'topic': 'Styling Web Pages',
        'mentor': 'Jane Smith',
        'date': date.today() - timedelta(days=8),
        'start_time': time(10, 0),
        'end_time': time(11, 0),
        'is_completed': True,
        'recording_url': 'https://www.youtube.com/live/hcGnztmTeeo?si=7B7MLuIvszMVeKww'
    },
    {
        'title': 'JavaScript Basics',
        'topic': 'Programming Logic',
        'mentor': 'Bob Johnson',
        'date': date.today() - timedelta(days=5),
        'start_time': time(10, 0),
        'end_time': time(11, 0),
        'is_completed': True,
        'recording_url': 'https://www.youtube.com/live/9rx43uKQYOA?si=dHoHWMHIIJzG7iw4'
    },
    {
        'title': 'Introduction to React',
        'topic': 'React Basics',
        'mentor': 'Alice Brown',
        'date': date.today() - timedelta(days=3),
        'start_time': time(10, 0),
        'end_time': time(11, 0),
        'is_completed': True,
        'recording_url': 'https://www.youtube.com/live/KwNU8LjEhSg?si=AazicjfLj_1Mh8F_'
    },
    {
        'title': 'React Components',
        'topic': 'Building UI',
        'mentor': 'Alice Brown',
        'date': date.today() + timedelta(days=2),
        'start_time': time(10, 0),
        'end_time': time(11, 0),
        'is_completed': False,
        'recording_url': 'https://www.youtube.com/live/GPTceu7L7jQ?si=Y8LIUge-40BwEZZK'
    },
    {
        'title': 'Advanced React Components',
        'topic': 'Advanced React',
        'mentor': 'Alice Brown',
        'date': date.today() + timedelta(days=4),
        'start_time': time(10, 0),
        'end_time': time(11, 0),
        'is_completed': False,
        'recording_url': 'https://www.youtube.com/live/g9_3tnDJeX4?si=w00vk6VJCGpF6CHL'
    },
    {
        'title': 'Django Models',
        'topic': 'Backend Development',
        'mentor': 'Charlie Wilson',
        'date': date.today() + timedelta(days=5),
        'start_time': time(10, 0),
        'end_time': time(11, 0),
        'is_completed': False,
        'recording_url': 'https://www.youtube.com/live/_8MF7oY6TNk?si=qrNfXT92qtN0fOF5'
    }
]

for session_data in sessions_data:
    session, created = Session.objects.get_or_create(
        title=session_data['title'],
        date=session_data['date'],
        defaults=session_data
    )
    if not created:
        session.recording_url = session_data['recording_url']
        session.save()

# Create Attendance for past sessions
past_sessions = Session.objects.filter(is_completed=True)
all_students = [student] + additional_students
for session in past_sessions:
    for stud in all_students:
        Attendance.objects.get_or_create(
            student=stud,
            session=session,
            defaults={'is_present': random.choice([True, False])}
        )

# Create Assessments
assessments_data = [
    {
        'title': 'HTML Assessment',
        'description': 'Test your HTML knowledge',
        'topic': 'HTML',
        'total_marks': 100,
        'duration_minutes': 60,
        'due_date': timezone.now() + timedelta(days=7),
        'is_active': True
    },
    {
        'title': 'CSS Assessment',
        'description': 'Test your CSS skills',
        'topic': 'CSS',
        'total_marks': 100,
        'duration_minutes': 60,
        'due_date': timezone.now() + timedelta(days=7),
        'is_active': True
    },
    {
        'title': 'JavaScript Assessment',
        'description': 'Test your JavaScript knowledge',
        'topic': 'JavaScript',
        'total_marks': 100,
        'duration_minutes': 60,
        'due_date': timezone.now() + timedelta(days=7),
        'is_active': True
    }
]

for assessment_data in assessments_data:
    Assessment.objects.get_or_create(
        title=assessment_data['title'],
        defaults=assessment_data
    )

# Create StudentAssessments
assessments = Assessment.objects.all()
for assessment in assessments:
    StudentAssessment.objects.get_or_create(
        student=student,
        assessment=assessment,
        defaults={
            'score': 85 if 'HTML' in assessment.title else 78 if 'CSS' in assessment.title else 92,
            'is_completed': True,
            'submitted_at': timezone.now() - timedelta(days=1)
        }
    )

# Create Projects
projects_data = [
    {
        'title': 'Personal Portfolio Website',
        'description': 'A responsive portfolio website built with HTML, CSS, and JavaScript',
        'github_url': 'https://github.com/testuser/portfolio',
        'live_demo_url': 'https://testuser.github.io/portfolio',
        'technologies': 'HTML, CSS, JavaScript',
        'status': 'completed',
        'submitted_at': timezone.now() - timedelta(days=3)
    },
    {
        'title': 'Todo App with React',
        'description': 'A simple todo application using React and local storage',
        'github_url': 'https://github.com/testuser/todo-react',
        'live_demo_url': 'https://testuser.github.io/todo-react',
        'technologies': 'React, JavaScript, CSS',
        'status': 'completed',
        'submitted_at': timezone.now() - timedelta(days=1)
    }
]

for project_data in projects_data:
    Project.objects.get_or_create(
        student=student,
        title=project_data['title'],
        defaults=project_data
    )

# Create Notifications
notifications_data = [
    {
        'title': 'Welcome to LMS',
        'message': 'Welcome to the Manac LMS Portal! Explore your dashboard and start learning.',
        'notification_type': 'info',
        'is_read': True
    },
    {
        'title': 'New Session Available',
        'message': 'A new session on React Components has been scheduled for tomorrow.',
        'notification_type': 'info',
        'is_read': False
    },
    {
        'title': 'Assessment Due Soon',
        'message': 'Your JavaScript Assessment is due in 3 days. Make sure to complete it on time.',
        'notification_type': 'warning',
        'is_read': False
    }
]

for notification_data in notifications_data:
    Notification.objects.get_or_create(
        student=student,
        title=notification_data['title'],
        defaults=notification_data
    )

# Create Study Materials
study_materials_data = [
    {
        'title': 'HTML5 Complete Guide',
        'description': 'Comprehensive guide to HTML5 including semantic elements, forms, and multimedia',
        'file_url': 'https://www.w3.org/TR/html5/',
        'file_type': 'pdf',
        'file_size': 2048000,  # 2MB
        'uploaded_by': user
    },
    {
        'title': 'CSS3 Master Reference',
        'description': 'Complete reference for CSS3 properties, selectors, and advanced styling techniques',
        'file_url': 'https://developer.mozilla.org/en-US/docs/Web/CSS',
        'file_type': 'pdf',
        'file_size': 1536000,  # 1.5MB
        'uploaded_by': user
    },
    {
        'title': 'JavaScript Fundamentals',
        'description': 'Essential JavaScript concepts including variables, functions, objects, and DOM manipulation',
        'file_url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide',
        'file_type': 'epub',
        'file_size': 1024000,  # 1MB
        'uploaded_by': user
    },
    {
        'title': 'React Development Toolkit',
        'description': 'Source code examples and templates for React development including hooks, components, and state management',
        'file_url': 'https://github.com/facebook/react/archive/main.zip',
        'file_type': 'zip',
        'file_size': 5120000,  # 5MB
        'uploaded_by': user
    },
    {
        'title': 'Django Web Development',
        'description': 'Presentation covering Django framework, models, views, templates, and deployment',
        'file_url': 'https://docs.djangoproject.com/en/stable/',
        'file_type': 'ppt',
        'file_size': 3072000,  # 3MB
        'uploaded_by': user
    },
    {
        'title': 'Full Stack Development Roadmap',
        'description': 'Complete learning path for becoming a full-stack developer with modern technologies',
        'file_url': 'https://roadmap.sh/full-stack',
        'file_type': 'pdf',
        'file_size': 512000,  # 512KB
        'uploaded_by': user
    }
]

for material_data in study_materials_data:
    StudyMaterial.objects.get_or_create(
        title=material_data['title'],
        defaults=material_data
    )

print("Sample data populated successfully!")
