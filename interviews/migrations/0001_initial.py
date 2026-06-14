from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('category', models.CharField(choices=[('programming','Programming Languages'),('web','Web Development'),('data','Data Science & ML'),('system','System Design'),('behavioral','Behavioral'),('database','Databases'),('devops','DevOps & Cloud'),('dsa','Data Structures & Algorithms')], max_length=20)),
                ('description', models.TextField()),
                ('icon', models.CharField(default='bi-code-slash', max_length=50)),
                ('color', models.CharField(default='#6366f1', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['order', 'name']},
        ),
        migrations.CreateModel(
            name='InterviewSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty', models.CharField(choices=[('easy','Easy'),('medium','Medium'),('hard','Hard'),('mixed','Mixed')], default='medium', max_length=10)),
                ('status', models.CharField(choices=[('in_progress','In Progress'),('completed','Completed'),('abandoned','Abandoned')], default='in_progress', max_length=15)),
                ('total_questions', models.PositiveIntegerField(default=5)),
                ('current_question_index', models.PositiveIntegerField(default=0)),
                ('overall_score', models.FloatField(blank=True, null=True)),
                ('ai_summary', models.TextField(blank=True)),
                ('strengths', models.TextField(blank=True)),
                ('improvements', models.TextField(blank=True)),
                ('duration_minutes', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interview_sessions', to='auth.user')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='interviews.topic')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('question_type', models.CharField(choices=[('conceptual','Conceptual'),('coding','Coding'),('scenario','Scenario-based'),('behavioral','Behavioral'),('system_design','System Design')], default='conceptual', max_length=20)),
                ('expected_answer_points', models.TextField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='interviews.interviewsession')),
            ],
            options={'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField()),
                ('score', models.FloatField(blank=True, null=True)),
                ('feedback', models.TextField(blank=True)),
                ('strengths', models.TextField(blank=True)),
                ('improvements', models.TextField(blank=True)),
                ('model_answer', models.TextField(blank=True)),
                ('time_taken_seconds', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='interviews.interviewsession')),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='interviews.question')),
            ],
        ),
    ]
