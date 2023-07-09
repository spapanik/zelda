from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("grappelli/", include("grappelli.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("zelda.home.urls", namespace="home")),
    path("armor/", include("zelda.armor.urls", namespace="armor")),
]
