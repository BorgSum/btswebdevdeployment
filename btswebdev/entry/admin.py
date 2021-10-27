from django.contrib import admin

from .models import Entry, EntryImage
# Register your models here.
admin.site.register(Entry)
admin.site.register(EntryImage)