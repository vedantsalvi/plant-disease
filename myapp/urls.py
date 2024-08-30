from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('fertilizer-calculator/', views.fertilizer_calculator, name='fertilizer_calculator'),
    path('disease_diagnosis/', views.disease_diagnosis, name='disease_diagnosis'),
    path('upload/', views.upload_image, name='upload_image'),
]

