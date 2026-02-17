import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manac_lms.settings')
django.setup()

from lms.models import InternshipAgenda

def populate_agenda():
    # Clear existing data
    InternshipAgenda.objects.all().delete()

    # Create agenda items for Python Full Stack Development Internship
    agenda_data = [
        {
            'week': 'Week 1',
            'agenda': 'Python Fundamentals & Development Environment Setup\n\n- Introduction to Python programming\n- Variables, data types, and operators\n- Control flow statements (if-else, loops)\n- Functions and modules\n- Setting up Python development environment (VS Code, PyCharm)\n- Version control with Git & GitHub basics',
            'deliverables': 'Complete Python basic exercises\nSet up development environment\nCreate GitHub account and push first repository\nComplete the weekly milestone',
            'order': 1,
        },
        {
            'week': 'Week 2',
            'agenda': 'Python Data Structures & Object-Oriented Programming\n\n- Lists, tuples, dictionaries, and sets\n- File handling in Python\n- Introduction to OOP concepts\n- Classes, objects, inheritance, and polymorphism\n- Exception handling\n- Working with external libraries (pip, virtual environments)',
            'deliverables': 'Create a Python project demonstrating OOP concepts\nImplement file handling operations\nComplete the weekly milestone\nSubmit feedback form',
            'order': 2,
        },
        {
            'week': 'Week 3',
            'agenda': 'HTML, CSS & Frontend Fundamentals\n\n- HTML5 semantic elements and document structure\n- CSS3 styling, flexbox, and grid layout\n- Responsive web design principles\n- JavaScript basics (variables, functions, DOM manipulation)\n- Introduction to Bootstrap framework\n- Building a static portfolio website',
            'deliverables': 'Create a responsive personal portfolio webpage\nImplement CSS animations and transitions\nComplete the weekly milestone\nSubmit feedback form',
            'order': 3,
        },
        {
            'week': 'Week 4',
            'agenda': 'Django Web Framework - Backend Development\n\n- Introduction to Django framework\n- Django project structure and settings\n- Models, migrations, and database relationships\n- Django ORM queries\n- Django admin panel customization\n- Building REST APIs with Django REST Framework',
            'deliverables': 'Create a Django project with models\nSet up database and run migrations\nBuild CRUD APIs for a sample application\nComplete the weekly milestone\nSubmit feedback form',
            'order': 4,
        },
        {
            'week': 'Week 5',
            'agenda': 'Database Integration & Full Stack Project Development\n\n- PostgreSQL/MySQL database design\n- Database modeling and relationships\n- Connecting Django with production database\n- User authentication and authorization\n- AJAX and fetch API for async operations\n- Integrating frontend with backend APIs',
            'deliverables': 'Design and implement database schema\nImplement user authentication system\nBuild a full stack CRUD application\nComplete the weekly milestone\nSubmit feedback form',
            'order': 5,
        },
        {
            'week': 'Week 6',
            'agenda': 'Deployment, Testing & Final Project Presentation\n\n- Deploying Python applications (Heroku, AWS, Railway)\n- Docker containerization basics\n- Unit testing with pytest\n- Debugging and error handling best practices\n- Final project documentation\n- Mock project presentations and code review',
            'deliverables': 'Deploy application to a cloud platform\nWrite unit tests for the project\nPrepare project documentation (README, screenshots)\nFinal presentation of the complete project\nComplete internship feedback form',
            'order': 6,
        },
    ]

    # Create agenda items
    for data in agenda_data:
        InternshipAgenda.objects.create(**data)

    # Create notes and responsibilities
    notes = """📚 6-Week Python/Django Internship

🎯 Objectives: Python, web apps, databases, cloud deployment, final project

📋 Requirements: Basic coding knowledge, laptop, Python 3.8+, VS Code, GitHub

🏆 Certificate: Complete milestones, 80% attendance, pass final exam (60%)"""

    responsibilities = """⏰ 6 Weeks | Sessions: 5:30-7:30 PM | Daily: 2-3 hrs + self-study

📅 Attendance: 80% mandatory | Notify emergencies

🎯 Tasks: Attend sessions, complete milestones, final project with deployment, final assessment

💻 Tech: Laptop (4GB RAM), Python 3.8+, Git, VS Code, Zoom/Teams

📝 Conduct: Professional behavior, no plagiarism"""

    # Update the first item with notes and responsibilities
    first_item = InternshipAgenda.objects.filter(order=1).first()
    if first_item:
        first_item.notes = notes
        first_item.responsibilities = responsibilities
        first_item.save()

    print("Internship agenda populated successfully!")

if __name__ == '__main__':
    populate_agenda()
