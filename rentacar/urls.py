
from django.contrib import admin
from django.urls import path, include
from django.http import FileResponse
from pathlib import Path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from aplicatie.views import MasiniSitemap, PaginiSitemap


def robots_txt(request):
    fisier = Path(settings.BASE_DIR) / 'robots.txt'
    return FileResponse(open(fisier, 'rb'), content_type='text/plain')

sitemaps = {
    'masini': MasiniSitemap, 'pagini': PaginiSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('', include('aplicatie.urls')),
    path('sitemap.xml',sitemap,{'sitemaps': sitemaps}, name='sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
