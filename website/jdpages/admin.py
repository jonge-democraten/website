from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import JDPage, JDHomePage

admin.site.register(JDPage, PageAdmin)
admin.site.register(JDHomePage, PageAdmin)
