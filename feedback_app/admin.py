from django.contrib import admin
from .models import  Message,Profile



class MessageAdmin (admin.ModelAdmin):
    list_display = ('belongs_to', 'message')
    readonly_fields = ('belongs_to', 'message', 'purpose')
    list_display_links = ('message',)
    list_filter = ('belongs_to',)
    list_per_page = 50


admin.site.register(Message, MessageAdmin)


class ProfileAdmin (admin.ModelAdmin):
    list_display = ('user', 'paid','total_response')
    # readonly_fields = ('belongs_to', 'message', 'purpose')
    list_display_links = ('user', 'paid')
    list_filter = ('paid',)
    list_per_page = 50


admin.site.register(Profile, ProfileAdmin)










