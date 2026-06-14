from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programming Languages'),
        ('web', 'Web Development'),
        ('data', 'Data Science & ML'),
        ('system', 'System Design'),
        ('behavioral', 'Behavioral'),
        ('database', 'Databases'),
        ('devops', 'DevOps & Cloud'),
        ('dsa', 'Data Structures & Algorithms'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='bi-code-slash')  # Bootstrap icon class
    color = models.CharField(max_length=20, default='#6366f1')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class InterviewSession(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('mixed', 'Mixed'),
    ]
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_sessions')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='sessions')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='in_progress')
    total_questions = models.PositiveIntegerField(default=5)
    current_question_index = models.PositiveIntegerField(default=0)
    overall_score = models.FloatField(null=True, blank=True)
    ai_summary = models.TextField(blank=True)
    strengths = models.TextField(blank=True)
    improvements = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.topic.name} ({self.created_at.strftime('%Y-%m-%d')})"

    @property
    def answered_questions(self):
        return self.answers.count()

    @property
    def progress_percent(self):
        if self.total_questions == 0:
            return 0
        return int((self.answered_questions / self.total_questions) * 100)


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('conceptual', 'Conceptual'),
        ('coding', 'Coding'),
        ('scenario', 'Scenario-based'),
        ('behavioral', 'Behavioral'),
        ('system_design', 'System Design'),
    ]

    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='conceptual')
    expected_answer_points = models.TextField(blank=True)  # Key points Claude expects
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:60]}..."


class Answer(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='answers')
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='answer')
    answer_text = models.TextField()
    score = models.FloatField(null=True, blank=True)  # 0-10
    feedback = models.TextField(blank=True)
    strengths = models.TextField(blank=True)
    improvements = models.TextField(blank=True)
    model_answer = models.TextField(blank=True)
    time_taken_seconds = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to Q{self.question.order} by {self.session.user.username}"

    @property
    def score_label(self):
        if self.score is None:
            return 'Not graded'
        if self.score >= 8:
            return 'Excellent'
        elif self.score >= 6:
            return 'Good'
        elif self.score >= 4:
            return 'Average'
        else:
            return 'Needs Work'

    @property
    def score_color(self):
        if self.score is None:
            return 'secondary'
        if self.score >= 8:
            return 'success'
        elif self.score >= 6:
            return 'info'
        elif self.score >= 4:
            return 'warning'
        else:
            return 'danger'
