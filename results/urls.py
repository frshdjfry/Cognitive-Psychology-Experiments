# results/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('wason-task/', views.wason_results, name='wason_results'),
    path('wason-task-timing/', views.wason_timing_results, name='wason_timing_results'),
    path('linda/', views.linda_results, name='linda_results'),
    path('linda-timing/', views.linda_timing_results, name='linda_timing_results'),
    path('framing/', views.framing_results, name='framing_results'),
    path('anchoring/', views.anchoring_results, name='anchoring_results'),
    path('anchoring-timing/', views.anchoring_timing_results, name='anchoring_timing_results'),
    path('two-four-six/', views.two_four_six_results, name='two_four_six_results'),
]
