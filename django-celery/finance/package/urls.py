from django.urls import path

from package import views

app_name = 'package'

urlpatterns = [
    path('pricing/', views.PricingView.as_view(), name='pricing')
]
