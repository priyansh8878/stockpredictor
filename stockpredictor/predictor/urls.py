from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_stock, name='predict_stock'),
]
