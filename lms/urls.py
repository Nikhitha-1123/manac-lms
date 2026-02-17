from django.urls import path
from . import views

app_name = 'lms'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard_redirect'),
    path('offer-letter/', views.offer_letter, name='offer_letter'),
    path('session-details/', views.session_details, name='session_details'),
    path('session-recordings/', views.session_recordings, name='session_recordings'),
    path('attendance/', views.attendance, name='attendance'),
    path('project-details/', views.project_details, name='project_details'),
    path('assessment/', views.assessment, name='assessment'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/<int:mock_test_id>/', views.quiz, name='mock_test_quiz'),
    path('quiz-submit/', views.quiz_submit, name='quiz_submit'),
    path('mock-test-quiz-submit/<int:mock_test_id>/', views.quiz_submit, name='mock_test_quiz_submit'),
    path('quiz-submit/<int:mock_test_id>/', views.quiz_submit, name='mock_test_quiz_submit'),
    path('study-material/', views.study_material, name='study_material'),
    path('certificate/', views.certificate, name='certificate'),
    path('placement-readiness/', views.placement_readiness, name='placement_readiness'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('notifications/', views.notifications, name='notifications'),
    path('submit-project/', views.submit_project, name='submit_project'),
    path('schedule-mock-interview/', views.schedule_mock_interview, name='schedule_mock_interview'),
    path('cancel-mock-interview/<int:interview_id>/', views.cancel_mock_interview, name='cancel_mock_interview'),
    path('internship-agenda/', views.internship_agenda, name='internship_agenda'),
    path('download-offer-letter/', views.download_offer_letter, name='download_offer_letter'),
]
