from django.contrib import admin

from website.jdevents.models import Event, Occurence

class EventAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event, EventAdmin)
