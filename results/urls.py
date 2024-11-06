# results/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('wason-task/', views.wason_results, name='wason_results'),
    path('linda/', views.linda_results, name='linda_results'),
    path('framing/', views.framing_results, name='framing_results'),
    path('anchoring/', views.anchoring_results, name='anchoring_results'),
]
