from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from Home.sitemaps import StaticViewSitemap, BlogSitemap, DestinationSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'destination': DestinationSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('Home.urls', 'Home'), namespace='Home')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
