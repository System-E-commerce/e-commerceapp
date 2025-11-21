from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('a-propos/', views.about_view, name='about'),
    path('', views.home, name='home'),
]
