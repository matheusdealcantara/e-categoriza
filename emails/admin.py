from django.contrib import admin

# Register your models here.
from .models import Email
admin.site.register(Email)

class EmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'subject', 'category')
    search_fields = ('email', 'subject', 'category')
    list_filter = ('category',)
