import logging
logger = logging.getLogger(__name__)

from django.contrib import admin

from mezzanine.pages.admin import PageAdmin
from mezzanine.core.admin import TabularDynamicInlineAdmin

from website.jdpages.models import JDPage, HomePage, ColumnElement, ColumnElementWidget
from website.utils.containers import HorizontalPosition


class LeftColumnElementWidgetInline(TabularDynamicInlineAdmin):
    """"""
    model = ColumnElementWidget
    verbose_name_plural = 'Left column widgets'
    
    def queryset(self, request):
        return ColumnElementWidget.get_widgets(HorizontalPosition.LEFT)


class RightColumnElementWidgetInline(TabularDynamicInlineAdmin):
    """"""
    model = ColumnElementWidget
    verbose_name_plural = 'Right column widgets'
    
    def queryset(self, request):
        return ColumnElementWidget.get_widgets(HorizontalPosition.RIGHT)


class HomePageAdmin(PageAdmin):
    inlines = [LeftColumnElementWidgetInline, RightColumnElementWidgetInline,]


class ColumnElementAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'content_type', 'object_id', 'site', 'title',)


admin.site.register(JDPage, PageAdmin)
admin.site.register(HomePage, HomePageAdmin)
admin.site.register(ColumnElement, ColumnElementAdmin)
admin.site.register(ColumnElementWidget)
