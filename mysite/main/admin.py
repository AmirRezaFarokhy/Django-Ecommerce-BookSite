from django.contrib import admin
from .models import Author, Books, Customers, Order

# Register your models here.
admin.site.register(Author)
admin.site.register(Books)
admin.site.register(Customers)
admin.site.register(Order)
