from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from myblog.views import post, blog, add_comment, get_comments

urlpatterns = [
    url(r'^(?P<ID>[0-9]+)/post/$', post, name = 'post'),
    url(r'^(?P<ID>[0-9]+)/posts/$', blog, name = 'blog'),
    url(r'^(?P<ID>[0-9]+)/comment/$', add_comment, name = 'add_comment'),
    url(r'^(?P<ID>[0-9]+)/comments/$', get_comments, name='get_comments'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)