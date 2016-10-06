import random

from django.views.generic import View
from django.shortcuts import render

# Create your views here.

from products.models import CuratedProducts

class DashboardView(View):
	def get(self, request, *args, **kwargs):
		curated = CuratedProducts.objects.filter(active=True).order_by("?")

		context = {
			"curated": curated,
		}
		return render(request, "dashboard/view.html", context)

class LegalView(View):
	def get(self, request, *args, **kwargs):
		context = {
			"title": "Terms and Conditions",
		}
		return render(request, "dashboard/legal.html", context)