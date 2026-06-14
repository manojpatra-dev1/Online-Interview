from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    EXPERIENCE_CHOICES = [
        ('fresher', 'Fresher (0-1 years)'),
        ('junior', 'Junior (1-3 years)'),
        ('mid', 'Mid-level (3-5 years)'),
        ('senior', 'Senior (5-8 years)'),
        ('lead', 'Lead/Principal (8+ years)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='fresher')
    target_role = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    @property
    def total_sessions(self):
        return self.user.interview_sessions.count()

    @property
    def completed_sessions(self):
        return self.user.interview_sessions.filter(status='completed').count()

    @property
    def average_score(self):
        from interviews.models import InterviewSession
        sessions = self.user.interview_sessions.filter(status='completed', overall_score__isnull=False)
        if sessions.exists():
            return round(sum(s.overall_score for s in sessions) / sessions.count(), 1)
        return 0
