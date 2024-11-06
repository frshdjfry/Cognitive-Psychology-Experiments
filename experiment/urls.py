from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('wason-task/', views.wason_task, name='wason_task'),
    path('linda-problem/', views.linda_problem, name='linda_problem'),
    path('framing-effect/', views.framing_effect, name='framing_effect'),
    path('anchoring-bias/', views.anchoring_bias, name='anchoring_bias'),
    path('two-four-six/', views.two_four_six_experiment, name='two_four_six_experiment'),
    path('thanks/', views.thanks_page, name='thanks_page'),
]

