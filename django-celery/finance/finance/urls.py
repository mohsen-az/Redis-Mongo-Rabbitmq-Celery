from django.urls import path

from finance import views

app_name = 'finance'

urlpatterns = [
    path('charge/', views.ChargeWalletView.as_view(), name='charge'),
    path('verify/', views.VerifyView.as_view(), name='verify'),
    path('pay/<str:invoice_number>/', views.PaymentView.as_view(), name='payment'),
    path('pay/<str:invoice_number>/<str:gateway_code>/', views.PaymentGatewayView.as_view(), name='payment-gateway'),
]
