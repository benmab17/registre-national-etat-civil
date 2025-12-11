from django.contrib import admin
from django.urls import path
from personnes import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    
    # Page d'accueil redirigée vers le login
    path("", views.login_view, name="accueil"),
]
