from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import JDPage

admin.site.register(JDPage, PageAdmin)