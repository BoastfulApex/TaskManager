from django.contrib import admin
from django.urls import path
from django.conf import settings
from .settings import *
from django.conf.urls.static import static
from django.urls import path, include

# from backend.api_urls import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path("web_app/", include("backend.urls")),
    # path("api/", include(router.urls)),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
