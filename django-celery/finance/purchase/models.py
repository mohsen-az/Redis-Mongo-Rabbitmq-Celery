from django.conf import settings
from django.db import models, transaction

from finance.models import Payment
from package.models import Package


class Purchase(models.Model):
    PAID = 10
    NOT_PAID = -10

    STATUS_CHOICES = (
        (PAID, 'Paid'),
        (NOT_PAID, 'Not Paid'),
    )

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='purchases',
        null=True
    )
    package = models.ForeignKey(
        to=Package,
        on_delete=models.SET_NULL,
        related_name='purchases',
        null=True
    )
    price = models.PositiveBigIntegerField()
    status = models.SmallIntegerField(
        choices=STATUS_CHOICES, default=NOT_PAID
    )
    payment = models.ForeignKey(
        to=Payment,
        on_delete=models.PROTECT,
        related_name='purchases'
    )

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.package} - {self.price} - {self.get_status_display()}'

    @classmethod
    def create(cls, user, package):
        if package.is_enable:
            with transaction.atomic():
                payment = Payment.create(amount=package.price, user=user)
                purchase = cls.objects.create(
                    user=user,
                    package=package,
                    price=package.price,
                    payment=payment
                )
            return purchase
        return None
