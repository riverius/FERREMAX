from django.urls import path , re_path
from django.conf import settings
from django.views.static import serve

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('', views.home, name='home'),
    path('contacto/', views.contacto, name='contacto'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('webpay/plus/commit/', views.webpay_plus_commit, name='webpay-plus-commit'),
    path('webpay/plus/create/', views.webpay_plus_create, name='webpay-plus-create'),

]