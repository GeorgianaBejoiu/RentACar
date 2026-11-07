from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_client, name='login_client'),
    path('client/', views.client_home, name='client_home'),
    path('logout/', views.logout_client, name='logout_client'),
    path('masini/', views.lista_masini, name='lista_masini'),
    path('masini/<int:id_masina>/', views.detalii_masina, name='detalii_masina'),
]