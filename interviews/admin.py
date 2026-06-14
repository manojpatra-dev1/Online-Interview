from django.contrib import admin
from .models import Topic, InterviewSession, Question, Answer


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'order']
    list_filter = ['category', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']


@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'topic', 'difficulty', 'status', 'overall_score', 'created_at']
    list_filter = ['status', 'difficulty', 'topic']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'completed_at']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['session', 'question_type', 'order']
    list_filter = ['question_type']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['session', 'question', 'score', 'created_at']
    list_filter = ['score']
