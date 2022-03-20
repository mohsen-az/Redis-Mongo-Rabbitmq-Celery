from django.contrib import admin

from package.models import Package, PackageAttribute


class PackageAttributeInline(admin.TabularInline):
    model = PackageAttribute
    extra = 3


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    inlines = [PackageAttributeInline]
    list_display = ['title', 'price', 'days']
