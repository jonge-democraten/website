import logging
logger = logging.getLogger(__name__)

from django.contrib import admin

from mezzanine.pages.admin import PageAdmin

from website.jdpages.models import JDPage, JDHomePage, ColumnElementWidget, BlogCategoryElement


class JDHomePageAdmin(PageAdmin):
   
    def get_fieldsets(self, request, obj=None):
        fs = super(JDHomePageAdmin, self).get_fieldsets(request, obj)
        fieldset_none = fs[0]
        fieldset_metadata = fs[1]
        
        # remove the column items, these are shown in a new set
        new_fields_none = []
        for field in fieldset_none[1]['fields']:
            if not field == 'column_elements_left' and not field == 'column_elements_right':
                new_fields_none.append(field)
        fieldset_none[1]['fields'] = new_fields_none
                
        fieldset_column_elements = (("Column elements"), 
                                 {
                                  "fields": ["column_elements_left", 'column_elements_right'],
                                  "classes": ("collapse-closed",)
                                 })
        fieldsets = (fieldset_none, fieldset_metadata, fieldset_column_elements) 
        return fieldsets
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        self_page_id = request.resolver_match.args[0]
        jdhomepage = JDHomePage.objects.get(id=self_page_id)
        if db_field.name == 'column_elements_left' or db_field.name == 'column_elements_right':
            kwargs["queryset"] = ColumnElementWidget.objects.filter(site=jdhomepage.site)
        return super(JDHomePageAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


class JDColumnItemAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'content_type', 'object_id', 'site', 'title',)


admin.site.register(JDPage, PageAdmin)
admin.site.register(JDHomePage, JDHomePageAdmin)
admin.site.register(ColumnElementWidget, JDColumnItemAdmin)
