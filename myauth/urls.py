from django.conf.urls import url
from myauth.views import myregister, mylogin, myblogid
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^register/$', myregister, name = 'register'),
    url(r'^login/$', mylogin, name = 'login'),
  #  url(r'^blog-(?P<id>[0-9]+)$', myblogid, name = 'blog-id'),
    url(r'^blog-id/$', myblogid, name = 'blog-id'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)