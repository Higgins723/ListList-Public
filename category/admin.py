from django.contrib import admin

from .models import *
# Register your models here.
class CategoryImageInline(admin.TabularInline):
    model = CategoryImage
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        CategoryImageInline,
    ]
    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)