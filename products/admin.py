from django.contrib import admin

# Register your models here.
from .models import (
		Product,
		CuratedProducts,
		Attachment
	)

class AttachmentImageInline(admin.TabularInline):
	model = Attachment
	extra = 0

class ProductAdmin(admin.ModelAdmin):
	inlines = [
		AttachmentImageInline,
	]
	list_display = ["__unicode__", "short_description", "price", "timestamp", "updated"]
	search_fields = ["title", "description"]
	class Meta:
		model = Product



admin.site.register(Product, ProductAdmin)

admin.site.register(CuratedProducts)
