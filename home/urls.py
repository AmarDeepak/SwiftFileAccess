from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.views import HandleFileUpload, home, download
urlpatterns = [
    path("",home),
    path("download/<uid>",download),
    path(
        "handle/", HandleFileUpload.as_view(), name="home"
    )
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()