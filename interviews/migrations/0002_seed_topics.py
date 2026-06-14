from django.db import migrations

TOPICS = [
    {'name': 'Python', 'slug': 'python', 'category': 'programming', 'description': 'Core Python concepts, OOP, data structures, libraries and best practices.', 'icon': 'bi-filetype-py', 'color': '#3776ab', 'order': 1},
    {'name': 'JavaScript', 'slug': 'javascript', 'category': 'programming', 'description': 'ES6+, async/await, closures, prototypes, and modern JS patterns.', 'icon': 'bi-filetype-js', 'color': '#f7df1e', 'order': 2},
    {'name': 'Django & REST APIs', 'slug': 'django', 'category': 'web', 'description': 'Django ORM, REST framework, authentication, and web development patterns.', 'icon': 'bi-globe', 'color': '#092e20', 'order': 3},
    {'name': 'React', 'slug': 'react', 'category': 'web', 'description': 'Hooks, state management, component patterns, and React ecosystem.', 'icon': 'bi-bootstrap', 'color': '#61dafb', 'order': 4},
    {'name': 'Data Structures & Algorithms', 'slug': 'dsa', 'category': 'dsa', 'description': 'Arrays, trees, graphs, sorting, dynamic programming and complexity analysis.', 'icon': 'bi-diagram-3', 'color': '#e34c26', 'order': 5},
    {'name': 'System Design', 'slug': 'system-design', 'category': 'system', 'description': 'Scalability, microservices, databases, caching, and distributed systems.', 'icon': 'bi-buildings', 'color': '#ff6b6b', 'order': 6},
    {'name': 'Machine Learning', 'slug': 'machine-learning', 'category': 'data', 'description': 'ML algorithms, model evaluation, feature engineering, and deep learning.', 'icon': 'bi-cpu', 'color': '#ff9900', 'order': 7},
    {'name': 'SQL & Databases', 'slug': 'sql-databases', 'category': 'database', 'description': 'SQL queries, indexing, normalization, transactions, and database design.', 'icon': 'bi-database', 'color': '#336791', 'order': 8},
    {'name': 'Docker & Kubernetes', 'slug': 'docker-kubernetes', 'category': 'devops', 'description': 'Containerization, orchestration, CI/CD pipelines, and cloud deployment.', 'icon': 'bi-box', 'color': '#2496ed', 'order': 9},
    {'name': 'Behavioral Interview', 'slug': 'behavioral', 'category': 'behavioral', 'description': 'STAR method, leadership, teamwork, conflict resolution, and soft skills.', 'icon': 'bi-people', 'color': '#6366f1', 'order': 10},
    {'name': 'Java', 'slug': 'java', 'category': 'programming', 'description': 'Core Java, OOP principles, collections, multithreading, and JVM concepts.', 'icon': 'bi-filetype-java', 'color': '#ed8b00', 'order': 11},
    {'name': 'AWS Cloud', 'slug': 'aws', 'category': 'devops', 'description': 'EC2, S3, Lambda, RDS, VPC and core AWS services and architecture.', 'icon': 'bi-cloud', 'color': '#ff9900', 'order': 12},
]


def seed_topics(apps, schema_editor):
    Topic = apps.get_model('interviews', 'Topic')
    for t in TOPICS:
        Topic.objects.get_or_create(slug=t['slug'], defaults=t)


def unseed_topics(apps, schema_editor):
    Topic = apps.get_model('interviews', 'Topic')
    Topic.objects.filter(slug__in=[t['slug'] for t in TOPICS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('interviews', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_topics, unseed_topics),
    ]
