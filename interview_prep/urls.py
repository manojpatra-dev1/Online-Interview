from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from interviews import views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.landing_page, name='landing'),
    path('dashboard/', home_views.dashboard, name='dashboard'),
    path('accounts/', include('accounts.urls')),
    path('interviews/', include('interviews.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
