from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView

urlpatterns = i18n_patterns(
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    re_path(r"^admin$", RedirectView.as_view(url='/admin/', permanent=True)),
    path("rosetta/", include("rosetta.urls")),
    path("user/", include("userauths.urls")),
    path("", include("core.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    prefix_default_language=False,
)

handler404 = "core.views.error"

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)