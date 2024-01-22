from django.db import models
from .category import Category
class Discount(models.Model):
    code = models.CharField(max_length=4)
    price= models.IntegerField(default=0)

    @staticmethod
    def get_discounts_by_code(code):
        return Discount.objects.filter (id__in=code)
    @staticmethod
    def get_all_products():
        return Discount.objects.all()