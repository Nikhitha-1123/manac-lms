from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    college = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=50, blank=True)
    year = models.CharField(max_length=20, blank=True)
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)
    enrollment_date = models.DateField(default=timezone.now)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    @property
    def get_year_display(self):
        return self.year


class Session(models.Model):
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    mentor = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True)
    recording_url = models.URLField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date', '-start_time']


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)
    marked_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['student', 'session']

    def __str__(self):
        return f"{self.student} - {self.session} - {'Present' if self.is_present else 'Absent'}"


class Assessment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    topic = models.CharField(max_length=100)
    total_marks = models.PositiveIntegerField(default=100)
    duration_minutes = models.PositiveIntegerField(default=60)
    due_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class StudentAssessment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    submitted_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    answers = models.JSONField(blank=True, null=True)  # Store answers as JSON

    class Meta:
        unique_together = ['student', 'assessment']

    def __str__(self):
        return f"{self.student} - {self.assessment}"

    @property
    def percentage_score(self):
        if self.score is not None and self.max_score > 0:
            return (self.score / self.max_score) * 100
        return 0


class Project(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    github_url = models.URLField(blank=True)
    live_demo_url = models.URLField(blank=True)
    technologies = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('submitted', 'Submitted')
    ], default='in_progress')
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.title}"


class StudyMaterial(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='study_materials/', blank=True, null=True)
    file_url = models.URLField(blank=True)
    file_type = models.CharField(max_length=10, choices=[
        ('pdf', 'PDF'),
        ('doc', 'DOC'),
        ('docx', 'DOCX'),
        ('ppt', 'PPT'),
        ('pptx', 'PPTX'),
        ('zip', 'ZIP'),
        ('epub', 'EPUB'),
        ('other', 'Other')
    ], default='pdf')
    file_size = models.PositiveIntegerField(null=True, blank=True)  # Size in bytes
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    issued_date = models.DateField(default=timezone.now)
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.verification_code:
            import uuid
            self.verification_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)


class JobOpening(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=[
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract')
    ], default='full_time')
    is_active = models.BooleanField(default=True)
    posted_at = models.DateTimeField(default=timezone.now)
    application_deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

    @property
    def salary_range(self):
        if self.salary_min and self.salary_max:
            return f"₹{self.salary_min} - ₹{self.salary_max} LPA"
        elif self.salary_min:
            return f"₹{self.salary_min} LPA+"
        elif self.salary_max:
            return f"Up to ₹{self.salary_max} LPA"
        return "Not disclosed"


class JobApplication(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job_opening = models.ForeignKey(JobOpening, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interviewed', 'Interviewed'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected')
    ], default='applied')
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    cover_letter = models.TextField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)

    class Meta:
        unique_together = ['student', 'job_opening']

    def __str__(self):
        return f"{self.student} - {self.job_opening}"


class Notification(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=[
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('error', 'Error')
    ], default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student} - {self.title}"

    class Meta:
        ordering = ['-created_at']


class OfferLetter(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="Full Stack Developer Intern")
    company = models.CharField(max_length=100, default="Manac Infotech Pvt Ltd")
    start_date = models.DateField()
    compensation = models.DecimalField(max_digits=10, decimal_places=2)
    reporting_to = models.CharField(max_length=100, default="Senior Engineering Manager")
    location = models.CharField(max_length=100, default="Hyderabad (Hybrid)")
    issued_date = models.DateField(default=timezone.now)
    offer_letter_file = models.FileField(upload_to='offer_letters/', blank=True, null=True)
    is_accepted = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Offer Letter - {self.student}"

    class Meta:
        ordering = ['-issued_date']


class MockTest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    topic = models.CharField(max_length=100)
    total_marks = models.PositiveIntegerField(default=100)
    duration_minutes = models.PositiveIntegerField(default=60)
    questions = models.JSONField()  # Store questions as JSON
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class StudentMockTest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mock_test = models.ForeignKey(MockTest, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    submitted_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    answers = models.JSONField(blank=True, null=True)  # Store answers as JSON
    attempt_number = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student} - {self.mock_test} (Attempt {self.attempt_number})"

    @property
    def percentage_score(self):
        if self.score is not None and self.max_score > 0:
            return (self.score / self.max_score) * 100
        return 0


class MockInterview(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    requested_date = models.DateTimeField(default=timezone.now)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('requested', 'Requested'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='requested')
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student} - {self.title}"

    class Meta:
        ordering = ['-requested_date']
