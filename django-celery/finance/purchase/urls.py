from django.urls import path

from purchase import views

app_name = 'purchase'

urlpatterns = [
    path('create/<int:package_id>/', views.PurchaseCreateView.as_view(), name='purchase-create'),
]
