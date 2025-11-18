from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_reclamation, name='add_reclamation'),
    path('contact/', views.contact_view, name='contact'),
]
