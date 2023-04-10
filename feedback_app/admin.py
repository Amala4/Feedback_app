from django.contrib import admin
from .models import  Message,Profile, WebStat



class MessageAdmin (admin.ModelAdmin):
    list_display = ('belongs_to', 'message','personal_question', 'business_question')
    readonly_fields = ('belongs_to', 'message', 'purpose')
    list_display_links = ('message',)
    list_filter = ('belongs_to',)
    list_per_page = 50


admin.site.register(Message, MessageAdmin)


class ProfileAdmin (admin.ModelAdmin):
    list_display = ('user', 'paid', 'personal_question','total_response', 'business_question')
    list_display_links = ('user', 'paid')
    list_filter = ('paid',)
    list_per_page = 50


admin.site.register(Profile, ProfileAdmin)




class WebStatAdmin (admin.ModelAdmin):
    list_display = ('period','homePage', 'profile')
    list_display_links = ('period','homePage', 'profile')
    readonly_fields = ('period','homePage', 'profile', 'contact_admin', 'privacy_policy', 'personal_quest_edit', 'business_quest_edit', 'personal_message_open', 'personal_message_post', 'business_message_open', 'business_message_post')
    list_per_page = 12

admin.site.register(WebStat, WebStatAdmin)






