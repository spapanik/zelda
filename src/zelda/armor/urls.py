from django.urls import path

from zelda.armor import views

app_name = "armor"
urlpatterns = [path("", views.ArmorView.as_view(), name="armor")]
