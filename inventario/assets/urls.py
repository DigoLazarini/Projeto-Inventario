from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from . import views

app_name = "assets"
# As URLs apontam para as operações do inventário e usam nomes para os templates.
urlpatterns = [
    path("", RedirectView.as_view(pattern_name="assets:dashboard", permanent=False), name="home"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("inventario/", views.dashboard, name="dashboard"),
    path("novo/", views.asset_create, name="create"),
    path("hospedagens/", views.hosting_list, name="hosting-list"),
    path("hospedagens/nova/", views.hosting_create, name="hosting-create"),
    path("hospedagens/<int:pk>/", views.hosting_detail, name="hosting-detail"),
    path("hospedagens/<int:pk>/editar/", views.hosting_update, name="hosting-update"),
    path("hospedagens/<int:pk>/excluir/", views.hosting_delete, name="hosting-delete"),
    path("licencas-office/", views.office_license_list, name="office-license-list"),
    path("<int:pk>/", views.asset_detail, name="detail"),
    path("<int:pk>/editar/", views.asset_update, name="update"),
    path("<int:pk>/excluir/", views.asset_delete, name="delete"),
]
