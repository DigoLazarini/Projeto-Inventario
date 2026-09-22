from django.urls import path

from . import views

app_name = "assets"
# As URLs apontam para as operações do inventário e usam nomes para os templates.
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("novo/", views.asset_create, name="create"),
    path("<int:pk>/", views.asset_detail, name="detail"),
    path("<int:pk>/editar/", views.asset_update, name="update"),
    path("<int:pk>/excluir/", views.asset_delete, name="delete"),
]
