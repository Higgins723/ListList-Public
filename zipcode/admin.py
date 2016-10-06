from django.contrib.gis import admin

# Register your models here.
from .models import Zipcode


# class ProductAdmin(admin.ModelAdmin):
# 	list_display = ["__unicode__"]
# 	search_fields = ["zipcode"]
# 	class Meta:
# 		model = USBorder

admin.site.register(Zipcode)