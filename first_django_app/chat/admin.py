from django.contrib import admin

from .models import Message


class MessageAdmin(admin.ModelAdmin):
    fields = ('text', 'created_at', 'author')
    list_display = ('created_at', 'author', 'text') # show this info in a list; make order as you wish
    search_fields =  ('text',)

# Register your models here.

admin.site.register(Message, MessageAdmin)