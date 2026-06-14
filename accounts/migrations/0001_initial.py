from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('experience_level', models.CharField(
                    choices=[('fresher','Fresher (0-1 years)'),('junior','Junior (1-3 years)'),('mid','Mid-level (3-5 years)'),('senior','Senior (5-8 years)'),('lead','Lead/Principal (8+ years)')],
                    default='fresher', max_length=20
                )),
                ('target_role', models.CharField(blank=True, max_length=100)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='auth.user')),
            ],
        ),
    ]
