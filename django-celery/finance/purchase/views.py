from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.views import View

from package.models import Package
from purchase.models import Purchase
from purchase.tasks import simple_purchased_app_task


class PurchaseCreateView(LoginRequiredMixin, View):
    template_name = 'purchase/create.html'

    def get(self, request, package_id, *args, **kwargs):
        package = Package.get_package(pk=package_id)
        if package is None:
            raise Http404

        purchase = Purchase.create(user=request.user, package=package)

        simple_purchased_app_task.delay()  # Run task

        return render(request, self.template_name, {'purchase': purchase})
