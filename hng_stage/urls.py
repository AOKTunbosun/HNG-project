from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.me_endpoint, name='me')
]
