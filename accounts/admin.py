from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'experience_level', 'target_role', 'created_at']
    list_filter = ['experience_level']
    search_fields = ['user__username', 'user__email', 'target_role']
