from django.contrib import admin

# Register your models here.
from file.models import *


#
class FileAdmin(admin.ModelAdmin):
    search_fields = ("directory",)
    list_display = ("directory", "file")


admin.site.register(Files, FileAdmin)