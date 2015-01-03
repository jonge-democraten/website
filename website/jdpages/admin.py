from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from mezzanine.core.admin import TabularDynamicInlineAdmin
from .models import JDPage, JDHomePage, DocumentListing, Document

admin.site.register(JDPage, PageAdmin)
admin.site.register(JDHomePage, PageAdmin)

class DocumentInline(TabularDynamicInlineAdmin):
    model = Document

class DocumentListingAdmin(PageAdmin):
    inlines = (DocumentInline,)

admin.site.register(DocumentListing, DocumentListingAdmin)
