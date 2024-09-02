from django.contrib import admin

from .models import Event, InviteUsage, Requirement

class RequirementInline(admin.TabularInline):
    model = Event.requirements.through
    extra = 3

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'location')
    search_fields = ('name', 'location', 'invite_code')
    list_filter = ('start_date', 'end_date', 'location')
    inlines = [RequirementInline]
    # hide the requirements field in the admin
    exclude = ('requirements','invite_code')

admin.site.register(Event, EventAdmin)

admin.site.register(InviteUsage)
admin.site.register(Requirement)