from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('topics/', views.topic_list, name='topic_list'),
    path('start/<slug:topic_slug>/', views.start_session, name='start_session'),
    path('session/<int:session_id>/', views.interview_session, name='interview_session'),
    path('session/<int:session_id>/submit/', views.submit_answer, name='submit_answer'),
    path('session/<int:session_id>/finalize/', views.finalize_session, name='finalize_session'),
    path('session/<int:session_id>/results/', views.session_results, name='session_results'),
    path('session/<int:session_id>/abandon/', views.abandon_session, name='abandon_session'),
    path('history/', views.session_history, name='session_history'),
]
