from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Avg, Count

from .models import Topic, InterviewSession, Question, Answer
from .ai_service import generate_questions, evaluate_answer
from accounts.models import UserProfile


# ---------------- LANDING PAGE ----------------
def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'interviews/landing.html', {
        "features": [
            {"icon": "bi-cpu-fill", "color": "#7c3aed", "title": "AI Question Generation", "desc": "Generate realistic interview questions"},
            {"icon": "bi-lightning-charge-fill", "color": "#06b6d4", "title": "Instant Feedback", "desc": "Get feedback instantly"},
            {"icon": "bi-graph-up", "color": "#10b981", "title": "Track Progress", "desc": "Monitor your improvement"},
        ],
        "steps": [
            {"num": 1, "title": "Choose Topic", "desc": "Pick interview topic"},
            {"num": 2, "title": "Start Session", "desc": "Generate questions"},
            {"num": 3, "title": "Answer", "desc": "Write your answers"},
            {"num": 4, "title": "Get Feedback", "desc": "AI evaluates you"},
        ]
    })


# ---------------- DASHBOARD ----------------
@login_required
def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    sessions = request.user.interview_sessions

    topics = Topic.objects.filter(is_active=True)
    recent_sessions = sessions.select_related('topic').order_by('-created_at')[:6]

    total_sessions = sessions.count()
    completed_sessions = sessions.filter(status='completed').count()

    avg_score = sessions.filter(
        status='completed',
        overall_score__isnull=False
    ).aggregate(avg=Avg('overall_score'))['avg']

    topic_stats = (
        sessions.filter(status='completed', overall_score__isnull=False)
        .values('topic__name')
        .annotate(avg_score=Avg('overall_score'), count=Count('id'))
        .order_by('-avg_score')[:5]
    )

    in_progress = sessions.filter(status='in_progress').first()

    return render(request, 'interviews/dashboard.html', {
        'profile': profile,
        'topics': topics,
        'recent_sessions': recent_sessions,
        'total_sessions': total_sessions,
        'completed_sessions': completed_sessions,
        'avg_score': round(avg_score, 1) if avg_score else 0,
        'topic_stats': list(topic_stats),
        'in_progress': in_progress,
    })


# ---------------- TOPICS ----------------
@login_required
def topic_list(request):
    category = request.GET.get('category', '')
    topics = Topic.objects.filter(is_active=True)

    if category:
        topics = topics.filter(category=category)

    return render(request, 'interviews/topic_list.html', {
        'topics': topics,
        'categories': Topic.CATEGORY_CHOICES,
        'selected_category': category,
    })


# ---------------- START SESSION ----------------
@login_required
def start_session(request, topic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug, is_active=True)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    difficulty_options = [
        {"value": "easy", "label": "Easy"},
        {"value": "medium", "label": "Medium"},
        {"value": "hard", "label": "Hard"},
        {"value": "mixed", "label": "Mixed"},
    ]

    if request.method == 'POST':
        difficulty = request.POST.get('difficulty', 'medium')

        try:
            num_questions = int(request.POST.get('num_questions', 5))
        except (ValueError, TypeError):
            num_questions = 5

        num_questions = max(3, min(10, num_questions))

        raw_questions = generate_questions(
            topic_name=topic.name,
            difficulty=difficulty,
            num_questions=num_questions,
            experience_level=profile.experience_level,
        )

        if not raw_questions:
            messages.error(request, 'Failed to generate questions.')
            return redirect('start_session', topic_slug=topic_slug)

        session = InterviewSession.objects.create(
            user=request.user,
            topic=topic,
            difficulty=difficulty,
            total_questions=len(raw_questions),
            status='in_progress',
        )

        Question.objects.bulk_create([
            Question(
                session=session,
                question_text=q.get('question_text', ''),
                question_type=q.get('question_type', 'conceptual'),
                expected_answer_points=q.get('expected_answer_points', ''),
                order=i + 1,
            )
            for i, q in enumerate(raw_questions)
        ])

        messages.success(request, f'{len(raw_questions)} questions generated!')
        return redirect('interview_session', session_id=session.id)

    return render(request, 'interviews/start_session.html', {
        'topic': topic,
        'profile': profile,
        'difficulty_options': difficulty_options
    })


# ---------------- SESSION ----------------
@login_required
def interview_session(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)

    if session.status == 'completed':
        return redirect('session_results', session_id=session.id)

    if session.status == 'abandoned':
        messages.warning(request, 'This session was abandoned.')
        return redirect('dashboard')

    answered_ids = session.answers.values_list('question_id', flat=True)
    current_question = session.questions.exclude(id__in=answered_ids).first()

    if not current_question:
        return redirect('finalize_session', session_id=session.id)

    progress = session.answers.count()

    return render(request, 'interviews/session.html', {
        'session': session,
        'question': current_question,
        'progress': progress,
        'total': session.total_questions,
        'progress_percent': int((progress / session.total_questions) * 100),
    })


# ---------------- SUBMIT ANSWER ----------------
@login_required
@require_POST
def submit_answer(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)

    if session.status != 'in_progress':
        messages.error(request, 'Session is not active.')
        return redirect('dashboard')

    question_id = request.POST.get('question_id')

    if not question_id:
        messages.error(request, 'Invalid question.')
        return redirect('interview_session', session_id=session_id)

    question = get_object_or_404(Question, id=question_id, session=session)

    answer_text = request.POST.get('answer_text', '').strip()

    if not answer_text:
        messages.error(request, 'Answer required.')
        return redirect('interview_session', session_id=session_id)

    eval_result = evaluate_answer(
        question=question.question_text,
        question_type=question.question_type,
        expected_points=question.expected_answer_points,
        user_answer=answer_text,
        topic=session.topic.name,
        difficulty=session.difficulty,
    )

    Answer.objects.create(
        session=session,
        question=question,
        answer_text=answer_text,
        score=eval_result.get('score', 5.0),
        feedback=eval_result.get('feedback', ''),
    )

    if session.answers.count() >= session.total_questions:
        return redirect('finalize_session', session_id=session_id)

    return redirect('interview_session', session_id=session_id)


# ---------------- FINALIZE ----------------
@login_required
def finalize_session(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)

    if session.status == 'completed':
        return redirect('session_results', session_id=session.id)

    answers = session.answers.all()

    if not answers.exists():
        messages.warning(request, 'No answers found.')
        return redirect('dashboard')

    scores = [a.score for a in answers if a.score is not None]
    overall_score = round(sum(scores) / len(scores), 1) if scores else 0

    session.status = 'completed'
    session.overall_score = overall_score
    session.completed_at = timezone.now()
    session.save()

    return redirect('session_results', session_id=session_id)


# ---------------- RESULTS ----------------
@login_required
def session_results(request, session_id):
    session = InterviewSession.objects.get(id=session_id)
    answers = session.answers.all()

    processed_answers = []

    for ans in answers:
        processed_answers.append({
            "question": ans.question.question_text,
            "feedback": ans.feedback,
            "score": ans.score,
            "strengths_list": [s.strip() for s in ans.strengths.split(";") if s.strip()] if ans.strengths else [],
            "improvements_list": [i.strip() for i in ans.improvements.split(";") if
                                  i.strip()] if ans.improvements else [],
        })

    return render(request, 'interviews/results.html', {
        "session": session,
        "answers": processed_answers,
    })

# ---------------- HISTORY ----------------
@login_required
def session_history(request):
    sessions = request.user.interview_sessions.select_related('topic').order_by('-created_at')

    return render(request, 'interviews/history.html', {
        'sessions': sessions,
    })


# ---------------- ABANDON ----------------
@login_required
@require_POST
def abandon_session(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)

    if session.status == 'completed':
        messages.warning(request, 'Cannot abandon a completed session.')
        return redirect('dashboard')

    session.status = 'abandoned'
    session.save()

    messages.info(request, 'Session abandoned.')
    return redirect('dashboard')