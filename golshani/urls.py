from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView 


admin.site.login = login_required('/')




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('account/', include('accounts.urls')),
    path('nikan-manager/', include('managements.urls')),
    path("robots.txt",TemplateView.as_view(template_name="pages/robots.txt", content_type="text/plain")), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'pages.views.error_404_view'
