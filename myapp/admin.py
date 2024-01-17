from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Clients)
admin.site.register(Bills)
admin.site.register(Products)
admin.site.register(Bills_Products)