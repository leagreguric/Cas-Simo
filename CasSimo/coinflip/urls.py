from django.urls import path
from . import views

urlpatterns = [
    path('', views.coin_flip, name='coin_flip'),

]
