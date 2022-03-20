from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View

from finance.forms import ChargeWalletForm
from finance.models import Payment, Gateway
from finance.utils.zarinpal import zarinpal_request_handler, zarinpal_payment_checker


class ChargeWalletView(View):
    template_name = 'finance/charge_wallet.html'
    form_class = ChargeWalletForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            payment_link, authority = zarinpal_request_handler(
                merchant_id=settings.ZARINPAL['merchant_id'],
                amount=form.cleaned_data['amount'],
                detail='Charge Wallet',
                user_email='dayan7640@gmail.com',
                user_phone_number=None,
                callback=settings.ZARINPAL['gateway_callback_url']
            )

            if payment_link is not None:
                return redirect(payment_link)
        return render(request, self.template_name, {'form': form})


class VerifyView(View):
    template_name = 'finance/callback.html'

    def get(self, request, *args, **kwargs):
        authority = request.GET.get('Authority')
        status = request.GET.get('Status')  # for test

        payment = Payment.get_payment(authority=authority)
        if payment is None:
            raise Http404

        data = {
            'merchant_id': payment.gateway.auth_data,
            'amount': payment.amount,
            'authority': payment.authority
        }
        payment.verify(data)

        return render(request, self.template_name, {'payment': payment, 'status': status})


class PaymentView(View):
    template_name = 'finance/payment_detail.html'

    def get(self, request, invoice_number, *args, **kwargs):
        payment = Payment.get_payment(invoice_number=invoice_number)
        if payment is None:
            raise Http404

        gateways = Gateway.get_gateways()
        return render(request, self.template_name, {'payment': payment, 'gateways': gateways})


class PaymentGatewayView(View):
    template_name = 'finance/payment_detail.html'

    def get(self, request, invoice_number, gateway_code, *args, **kwargs):
        payment = Payment.get_payment(invoice_number=invoice_number)
        if payment is None:
            raise Http404

        gateway = Gateway.get_gateway(gateway_code=gateway_code)
        if gateway is None:
            raise Http404

        payment.gateway = gateway
        payment.save()

        payment_link = payment.bank_page
        if payment_link:
            return redirect(payment_link)

        gateways = Gateway.get_gateways()
        return render(request, self.template_name, {'payment': payment, 'gateways': gateways})
