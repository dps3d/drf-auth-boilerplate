from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from bookstore.views import TokenLogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("bookstore.urls")),
    # Маршрути автентифікації Token
    path("api/v1/auth/token/", obtain_auth_token, name="token_login"),
    path("api/v1/auth/token/logout/", TokenLogoutView.as_view(), name="token_logout"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
