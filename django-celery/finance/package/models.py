from django.db import models


class Package(models.Model):
    title = models.CharField(max_length=48)
    price = models.BigIntegerField()
    description = models.TextField(blank=True)
    days = models.PositiveSmallIntegerField()
    is_enable = models.BooleanField(default=True)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_package(cls, **kwargs):
        package_qs = cls.objects.filter(**kwargs)
        if package_qs.exists():
            package = package_qs.first()
            return package
        raise None


class PackageAttribute(models.Model):
    package = models.ForeignKey(
        to=Package,
        on_delete=models.CASCADE,
        related_name='attributes'
    )
    title = models.CharField(max_length=255)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
