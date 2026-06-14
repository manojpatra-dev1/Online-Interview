# ⚡ PrepAI — AI Interview Preparation Platform

A full-stack Django + MySQL application powered by Claude AI (Anthropic) that generates
realistic interview questions, evaluates answers, and provides detailed feedback.

---

## 🗂️ Project Structure

```
interview_prep/
├── manage.py
├── requirements.txt
├── .env.example                  ← Copy to .env and fill in values
├── interview_prep/               ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                     ← User auth & profiles
│   ├── models.py   (UserProfile)
│   ├── views.py    (register, login, logout, profile)
│   ├── forms.py
│   ├── urls.py
│   └── migrations/
├── interviews/                   ← Core interview logic
│   ├── models.py   (Topic, InterviewSession, Question, Answer)
│   ├── views.py    (dashboard, session, submit, results…)
│   ├── ai_service.py             ← Claude API integration ⭐
│   ├── urls.py
│   └── migrations/
│       ├── 0001_initial.py
│       └── 0002_seed_topics.py   ← Auto-seeds 12 topics
└── templates/
    ├── base.html
    ├── accounts/
    │   ├── register.html
    │   ├── login.html
    │   └── profile.html
    └── interviews/
        ├── landing.html
        ├── dashboard.html
        ├── topic_list.html
        ├── start_session.html
        ├── session.html          ← Live interview UI
        ├── results.html          ← Detailed results
        └── history.html
```

---

## ⚙️ Step-by-Step Setup

### STEP 1 — Prerequisites

Make sure you have installed:
- Python 3.10+       → https://python.org
- MySQL 8.0+         → https://mysql.com  (or MariaDB)
- pip                → comes with Python

```bash
python --version    # Should be 3.10+
mysql --version     # Should be 8.0+
```

---

### STEP 2 — Create MySQL Database

Open MySQL shell:
```bash
mysql -u root -p
```

Run these SQL commands:
```sql
CREATE DATABASE interview_prep_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'prepai_user'@'localhost' IDENTIFIED BY 'YourStrongPassword123';
GRANT ALL PRIVILEGES ON interview_prep_db.* TO 'prepai_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

### STEP 3 — Get Your Anthropic API Key

1. Go to https://console.anthropic.com
2. Sign up / Login
3. Navigate to API Keys → Create new key
4. Copy the key (starts with `sk-ant-...`)

---

### STEP 4 — Clone / Extract and Configure

```bash
# Navigate to the project folder
cd interview_prep

# Copy the environment template
cp .env.example .env
```

Edit `.env` with your values:
```
SECRET_KEY=your-random-secret-key-here
DEBUG=True
DB_NAME=interview_prep_db
DB_USER=prepai_user
DB_PASSWORD=YourStrongPassword123
DB_HOST=localhost
DB_PORT=3306
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Generate a Django secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### STEP 5 — Create Virtual Environment & Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install all packages
pip install -r requirements.txt
```

> Note: If mysqlclient install fails on Ubuntu/Debian:
> ```bash
> sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
> pip install mysqlclient
> ```
> On macOS:
> ```bash
> brew install mysql-client pkg-config
> pip install mysqlclient
> ```
> On Windows: Download the mysqlclient .whl from https://www.lfd.uci.edu/~gohlke/pythonlibs/

---

### STEP 6 — Run Database Migrations

```bash
# Apply all migrations (creates all tables + seeds 12 topics automatically)
python manage.py migrate
```

You should see output including:
```
Running migrations:
  Applying interviews.0001_initial... OK
  Applying interviews.0002_seed_topics... OK   ← 12 topics loaded!
```

---

### STEP 7 — Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

---

### STEP 8 — Run the Development Server

```bash
python manage.py runserver
```

Open your browser:
- **App:**   http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/

---

## 🎯 How to Use the Platform

1. **Register** → Create an account at `/accounts/register/`
2. **Set Profile** → Set your experience level (affects question difficulty)
3. **Choose Topic** → Browse 12+ topics on the Topics page
4. **Configure** → Set difficulty (Easy/Medium/Hard/Mixed) and question count (3-10)
5. **Interview** → Answer AI-generated questions (live timer)
6. **Get Results** → Instant AI feedback, score (0-10), model answers
7. **Track Progress** → Dashboard shows avg scores, topic performance

---

## 📋 Topics Available (Auto-seeded)

| Topic              | Category          |
|--------------------|-------------------|
| Python             | Programming       |
| JavaScript         | Programming       |
| Django & REST APIs | Web Dev           |
| React              | Web Dev           |
| DSA                | Algorithms        |
| System Design      | System Design     |
| Machine Learning   | Data Science      |
| SQL & Databases    | Databases         |
| Docker & Kubernetes| DevOps            |
| Behavioral         | Behavioral        |
| Java               | Programming       |
| AWS Cloud          | DevOps            |

---

## 🤖 AI Features (Claude Integration)

Located in `interviews/ai_service.py`:

| Function                  | Description                                     |
|---------------------------|-------------------------------------------------|
| `generate_questions()`    | Creates N interview questions for a topic       |
| `evaluate_answer()`       | Scores user answer 0-10 with detailed feedback  |
| `generate_session_summary()` | Overall session report with recommendations  |

---

## 🗄️ Database Models

```
User (Django built-in)
 └── UserProfile (experience_level, target_role, bio)

Topic (name, slug, category, icon, color)
 └── InterviewSession (user, topic, difficulty, status, overall_score)
      ├── Question (question_text, question_type, expected_answer_points)
      └── Answer   (answer_text, score, feedback, strengths, improvements, model_answer)
```

---

## 🔧 URL Routes

| URL                              | View                 | Description               |
|----------------------------------|----------------------|---------------------------|
| `/`                              | landing_page         | Public landing page       |
| `/dashboard/`                    | dashboard            | User dashboard            |
| `/accounts/register/`            | register_view        | Registration              |
| `/accounts/login/`               | login_view           | Login                     |
| `/accounts/profile/`             | profile_view         | Edit profile              |
| `/interviews/topics/`            | topic_list           | Browse topics             |
| `/interviews/start/<slug>/`      | start_session        | Configure & start         |
| `/interviews/session/<id>/`      | interview_session    | Live interview            |
| `/interviews/session/<id>/submit/` | submit_answer      | Submit an answer          |
| `/interviews/session/<id>/results/` | session_results   | View results              |
| `/interviews/history/`           | session_history      | All past sessions         |
| `/admin/`                        | Django Admin         | Admin panel               |

---

## 🚀 Production Deployment Tips

1. Set `DEBUG=False` in `.env`
2. Set `ALLOWED_HOSTS=yourdomain.com` in `.env`
3. Run `python manage.py collectstatic`
4. Use Gunicorn: `pip install gunicorn && gunicorn interview_prep.wsgi`
5. Set up Nginx as a reverse proxy
6. Use environment variables for secrets (never commit `.env`)

---

## 🐛 Common Issues

**MySQL connection error:** Verify DB credentials in `.env` and that MySQL is running.

**mysqlclient install fails:** See platform-specific instructions in Step 5.

**AI returns generic feedback:** Make sure `ANTHROPIC_API_KEY` is set correctly in `.env`.

**Static files not loading:** Run `python manage.py collectstatic` and check `STATIC_ROOT`.

**Migration errors:** Try `python manage.py migrate --run-syncdb` if models aren't found.
