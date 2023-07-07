from django.urls import path

from zelda.home import views

app_name = "home"
urlpatterns = [path("", views.HomeView.as_view(), name="home")]
