import json
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from finance.utils.zarinpal import zarinpal_request_handler, zarinpal_payment_checker


class Gateway(models.Model):
    FUNCTION_SAMAN = 'saman'
    FUNCTION_SHAPARAK = 'shaparak'
    FUNCTION_FINOTECH = 'finotech'
    FUNCTION_ZARINPAL = 'zarinpal'
    FUNCTION_PARSIAN = 'parsian'

    GATEWAY_FUNCTIONS = (
        (FUNCTION_SAMAN, _('Saman')),
        (FUNCTION_SHAPARAK, _('Shaparak')),
        (FUNCTION_FINOTECH, _('Finotech')),
        (FUNCTION_ZARINPAL, _('Zarinpal')),
        (FUNCTION_PARSIAN, _('Parsian')),
    )

    title = models.CharField(
        max_length=100, verbose_name=_('gateway title')
    )
    gateway_request_url = models.CharField(
        max_length=150, verbose_name=_('request url'),
        blank=True, null=True
    )
    gateway_verify_url = models.CharField(
        max_length=150, verbose_name=_('verify url'),
        blank=True, null=True
    )
    gateway_code = models.CharField(
        max_length=12,
        choices=GATEWAY_FUNCTIONS,
        verbose_name=_('gateway code')
    )

    is_enable = models.BooleanField(
        verbose_name=_('is enable'), default=True
    )

    auth_data = models.TextField(
        verbose_name=_('auth data'), null=True, blank=True
    )  # Include merchant_id or secret_key or private_key

    class Meta:
        verbose_name = _('Gateway')
        verbose_name_plural = _('Gateways')

    def __str__(self):
        return self.title

    def get_request_handler(self):
        handlers = {
            self.FUNCTION_SAMAN: None,
            self.FUNCTION_SHAPARAK: None,
            self.FUNCTION_FINOTECH: None,
            self.FUNCTION_ZARINPAL: zarinpal_request_handler,
            self.FUNCTION_PARSIAN: None,
        }
        return handlers.get(self.gateway_code)

    def get_verify_handler(self):
        handlers = {
            self.FUNCTION_SAMAN: None,
            self.FUNCTION_SHAPARAK: None,
            self.FUNCTION_FINOTECH: None,
            self.FUNCTION_ZARINPAL: zarinpal_payment_checker,
            self.FUNCTION_PARSIAN: None,
        }
        return handlers.get(self.gateway_code)

    @property
    def credentials(self):
        return json.loads(self.auth_data)

    @classmethod
    def get_gateways(cls):
        gateways = cls.objects.filter(is_enable=True)
        return gateways

    @classmethod
    def get_gateway(cls, **kwargs):
        gateway_qs = cls.objects.filter(is_enable=True, **kwargs)
        if gateway_qs.exists():
            gateway = gateway_qs.first()
            return gateway
        return None


class Payment(models.Model):
    invoice_number = models.UUIDField(verbose_name=_('invoice number'), unique=True, default=uuid4)
    amount = models.PositiveIntegerField(verbose_name=_('payment amount'), editable=True)
    gateway = models.ForeignKey(
        to=Gateway,
        on_delete=models.SET_NULL,
        related_name='payments',
        verbose_name=_('gateway'),
        null=True,
        blank=True
    )
    is_paid = models.BooleanField(verbose_name=_('is paid status'), default=False)
    payment_log = models.TextField(verbose_name=_('log'), blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='payments',
        verbose_name=_('user'),
        null=True
    )
    authority = models.CharField(max_length=64, verbose_name=_('authority'), blank=True)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        """Convert UUID to str"""
        return self.invoice_number.hex

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._backup_is_paid = self.is_paid

    @property
    def get_handler_data(self):
        return {
            'merchant_id': self.gateway.auth_data,
            'amount': self.amount,
            'detail': self.title,
            'user_email': self.user.email,
            'user_phone_number': getattr(self.user, 'phone_number', None),
            'callback': self.gateway.gateway_verify_url
        }

    @property
    def bank_page(self):
        handler = self.gateway.get_request_handler()
        if handler is not None:
            data = self.get_handler_data
            link, authority = handler(**data)
            if authority is not None:
                self.authority = authority
                self.save()
            return link

    @property
    def title(self):
        return _('Instant payment')

    def status_changed(self):
        """Check status changed"""
        return self.is_paid != self._backup_is_paid

    def verify(self, data):
        handler = self.gateway.get_verify_handler()
        if not self.is_paid and handler is not None:
            handler(**data)
        return self.is_paid

    def get_gateway(self):
        gateway = Gateway.objects.filter(is_enable=True).first()
        return gateway.gateway_code

    def save_log(self, data, scope='Request handlers', save=True):
        generate_log = f'[{timezone.now()}][{scope}] {data}\n'
        if self.payment_log != '':
            self.payment_log += generate_log
        else:
            self.payment_log = generate_log
        if save:
            self.save()

    @classmethod
    def create(cls, amount, user):
        payment = cls.objects.create(
            amount=amount, user=user
        )
        return payment

    @classmethod
    def get_payment(cls, **kwargs):
        payment_qs = Payment.objects.filter(**kwargs)
        if payment_qs.exists():
            payment = payment_qs.first()
            return payment
        return None
