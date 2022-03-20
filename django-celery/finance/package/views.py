from django.shortcuts import render
from django.views import View

from package.models import Package


class PricingView(View):
    template_name = 'package/pricing.html'

    @property
    def get_packages(self):
        packages = Package.objects.prefetch_related('attributes').filter(is_enable=True)
        return {'packages': packages}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_packages)
