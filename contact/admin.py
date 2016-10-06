from django.contrib import admin

from .models import Contact
from .forms import ContactForm

# Register your models here.
class ContactModelAdmin(admin.ModelAdmin):
    #be able to edit from list view
    list_editable = ["message_status"]
    #will show in the admin site
    list_display = ["__unicode__", "message_type", "message_status", "short_message", "message_recieved"]
    #will alow you to filter results from db
    list_filter = ["message_recieved", "message_type", "message_status"]
    #give you search box for db
    search_fields = ["full_name", "email", "message", "message_type"]
    #import form from forms.py
    form = ContactForm

admin.site.register(Contact, ContactModelAdmin)