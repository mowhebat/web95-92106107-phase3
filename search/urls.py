from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from search.views import search

urlpatterns = [
    url(r'^blog/$', search, name='search'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)