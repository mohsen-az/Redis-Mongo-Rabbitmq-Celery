from django.db.models import Sum

from finance.models import Payment

from celery import shared_task


@shared_task()
def simple_finance_app_task():
    pass


@shared_task(name="get and send total purchased")
def get_report():
    """
    Get and send total purchased
    :return:
    """
    total_payment = Payment.objects.filter(is_paid=True).aggregate(
        total=Sum("amount")
    )
    print(f"Total Payment: {total_payment.get('total', 0)}")