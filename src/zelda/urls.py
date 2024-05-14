from django.urls import include, path

urlpatterns = [
    path("api/users/", include("zelda.users.urls", namespace="users")),
    path("api/armor/", include("zelda.armor.urls", namespace="armor")),
]
