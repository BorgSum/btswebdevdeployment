from django.contrib import admin

# Register your models here.
from .models import Badge, Allocation
# Register your models here.
admin.site.register(Badge)
admin.site.register(Allocation)
