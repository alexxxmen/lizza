from django.conf.urls import url, include
from django.contrib import admin
from lizza import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^', include('magazine.urls', namespace='magazine')),

]

if settings.DEBUG:
    try:
        from django.conf.urls.static import static
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    except ImportError as e:
        import logging
        l = logging.getLogger(__name__)
        l.warning(e)
