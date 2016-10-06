from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Category

# Create your views here.
class CategoryListView(ListView):
	model = Category
	queryset = Category.objects.all()
	# template_name = "products/product_list.html"


class CategoryDetailView(DetailView):
	model = Category

	def get_context_data(self, *args, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()
		#order products in category page by date posted
		product_set = obj.product_set.all().order_by("-timestamp")
		products = product_set.distinct()
		context["products"] = products
		return context
