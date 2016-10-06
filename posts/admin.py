from django.contrib import admin

# Register your models here.
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "updated", "timestamp"]
    #list display links is what is href in the db
    list_display_links = ["__unicode__"]
    #adds a filter to app in the db
    list_filter = ["updated", "timestamp"]
    #lets you search app in the db
    search_fields = ["title", "content"]
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
