import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.contrib import admin
from django.utils.functional import curry

from mezzanine.pages.admin import PageAdmin
from mezzanine.core.admin import TabularDynamicInlineAdmin
from website.jdpages.models import JDPage, HomePage, ColumnElement, ColumnElementWidget, DocumentListing, Document

from website.utils.containers import HorizontalPosition


class ColumnElementWidgetInline(TabularDynamicInlineAdmin):
    """"""
    model = ColumnElementWidget

    def get_formset(self, request, obj=None, **kwargs):
        """ 
        Adds the initial value of the horizontal position to the formset.
        Note: does not work for the 'Add another' button in the admin.
        """
        initial = []
        initial.append({'horizontal_position': self.get_default_position(),})
        formset = super(ColumnElementWidgetInline, self).get_formset(request, obj, **kwargs)
        formset.__init__ = curry(formset.__init__, initial=initial)
        logger.warning(self.get_default_position())
        return formset


class LeftColumnElementWidgetInline(ColumnElementWidgetInline):
    """ """
    verbose_name_plural = 'Left column widgets'

    def get_queryset(self, request):
        return ColumnElementWidget.objects.filter(horizontal_position=self.get_default_position())

    def get_default_position(self):
        return HorizontalPosition.LEFT


class RightColumnElementWidgetInline(ColumnElementWidgetInline):
    """ """
    verbose_name_plural = 'Right column widgets'
    
    def get_queryset(self, request):
        return ColumnElementWidget.objects.filter(horizontal_position=self.get_default_position())
    
    def get_default_position(self):
        return HorizontalPosition.RIGHT


class HomePageAdmin(PageAdmin):
    inlines = [LeftColumnElementWidgetInline, RightColumnElementWidgetInline,]


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('description', 'document', 'document_listing')


class ColumnElementAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'content_type', 'object_id', 'site',)


class ColumnElementWidgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'column_element', 'page', 'max_items', 'horizontal_position', 'site')


class DocumentInline(TabularDynamicInlineAdmin):
    model = Document

    
class DocumentListingAdmin(PageAdmin):
    inlines = (DocumentInline,)


admin.site.register(JDPage, PageAdmin)
admin.site.register(HomePage, HomePageAdmin)
admin.site.register(DocumentListing, DocumentListingAdmin)

if settings.DEBUG:
    admin.site.register(ColumnElement, ColumnElementAdmin)
    admin.site.register(ColumnElementWidget, ColumnElementWidgetAdmin)
    admin.site.register(Document, DocumentAdmin)