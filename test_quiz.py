import os
import sys
import django
from django.conf import settings

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manac_lms.settings')
django.setup()

from lms.models import Student, Assessment, StudentAssessment

def test_quiz_submission():
    # Create a test client
    client = Client()

    # Create a test user
    user = User.objects.create_user(username='testuser_quiz', password='password123')
    student = Student.objects.create(user=user, full_name='Test User', college='Test College', branch='CS', year='1st')

    # Login the user
    client.login(username='testuser_quiz', password='password123')

    # Simulate quiz submission with some answers
    answers = {
        '0': '14',  # correct
        '1': 'def',  # correct
        '2': 'Returns the length of a string or list',  # correct
        '3': 'List',  # correct
        '4': '# This is a comment',  # correct
        '5': 'Executes code if a condition is true',  # correct
        '6': 'print',  # correct
        '7': '3',  # correct
        '8': '[]',  # correct
        '9': 'Ends a loop prematurely'  # correct
    }

    response = client.post(reverse('lms:quiz_submit'), {
        'answers': json.dumps(answers),
        'csrfmiddlewaretoken': 'dummy'  # Django test client handles CSRF
    })

    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.content.decode()[:500]}...")

    # Check if StudentAssessment was created
    assessment = Assessment.objects.filter(title='Python Basics Quiz').first()
    if assessment:
        student_assessment = StudentAssessment.objects.filter(student=student, assessment=assessment).first()
        if student_assessment:
            print(f"Score saved: {student_assessment.score}")
            print(f"Is completed: {student_assessment.is_completed}")
            print(f"Answers saved: {student_assessment.answers}")
        else:
            print("StudentAssessment not found")
    else:
        print("Assessment not found")

    # Cleanup
    user.delete()

if __name__ == '__main__':
    test_quiz_submission()
