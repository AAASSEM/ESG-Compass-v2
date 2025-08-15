"""
URL configuration for esg_platform project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve
from apps.dashboard.views import test_social_dashboard
import os

# Custom view to serve React app with proper error handling
def serve_react_app(request, path=''):
    """Serve the React app's index.html for all non-API routes"""
    try:
        return TemplateView.as_view(template_name='index.html')(request)
    except:
        # If index.html is not found, return a debug message
        from django.http import HttpResponse
        return HttpResponse(
            f"<h1>React app not found</h1>"
            f"<p>Looking for index.html in: {settings.TEMPLATES[0]['DIRS']}</p>"
            f"<p>Current working directory: {os.getcwd()}</p>"
            f"<p>Files in frontend-react/dist: {os.listdir(os.path.join(settings.BASE_DIR.parent, 'frontend-react', 'dist')) if os.path.exists(os.path.join(settings.BASE_DIR.parent, 'frontend-react', 'dist')) else 'Directory not found'}</p>"
        )

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Test dashboard (no auth required)
    path('test/social/', test_social_dashboard, name='test_social_dashboard'),
    
    # API endpoints
    path('api/auth/', include('apps.authentication.urls')),
    path('api/companies/', include('apps.companies.urls')),
    path('api/esg/', include('apps.esg_assessment.urls')),
    path('api/tasks/', include('apps.tasks.urls')),
    path('api/reports/', include('apps.reports.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('api/users/', include('apps.user_management.urls')),
]

# Serve static files explicitly in production
if not settings.DEBUG:
    # Serve static files
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR.parent, 'frontend-react', 'dist', 'assets')}),
    ]

# Serve media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# React app routes - MUST be last
urlpatterns += [
    # Root URL
    path('', serve_react_app, name='home'),
    # Catch-all for React Router - excludes api/, admin/, static/, assets/, media/
    re_path(r'^(?!api/|admin/|static/|assets/|media/).*$', serve_react_app),
]
