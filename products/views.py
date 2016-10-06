from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured

#for django_filters
from django_filters import FilterSet, CharFilter, NumberFilter

#local imports
from .models import Product, Attachment
from .forms import ProductModelForm, ProductFilterForm, ProductModelUpdateForm
from .mixins import ProductManagerMixin
# from tags.models import Tag
# from analytics.models import TagView
from sellers.models import SellerAccount

#external imports
from listlist.mixins import (
		MultiSlugMixin,
		SubmitBtnMixin,
		LoginRequiredMixin,
		HeaderFormMixin,
	)

from zipcode.models import Zipcode
from zipcode.math_to_degrees import change_in_latitude, change_in_longitude

from sellers.mixins import SellerAccountMixin

# Create your views here.

class ProductCreateView(HeaderFormMixin, SellerAccountMixin, SubmitBtnMixin, CreateView):
	model = Product
	template_name = "form.html"
	form_class = ProductModelForm
	# success_url = "/products/add/"
	submit_btn = "Add Product"
	form_title = "Add Product"

	#when product is created attach user to product
	def form_valid(self, form):
		seller = self.get_account()
		form.instance.seller = seller
		zip_code_data = form.cleaned_data.get("zip_code_data")
		if zip_code_data:
			zipcode_obj, created = Zipcode.objects.get_or_create(zipcode=zip_code_data)
			form.instance.zipcode = zipcode_obj

		return super(ProductCreateView, self).form_valid(form)


class ProductUpdateView(HeaderFormMixin, ProductManagerMixin, SubmitBtnMixin, MultiSlugMixin, UpdateView):
	model = Product
	template_name = "form.html"
	form_class = ProductModelUpdateForm
	# success_url = "/products/"
	submit_btn = "Update Product"
	form_title = "Update Product"

	def get_initial(self):
		initial = super(ProductUpdateView,self).get_initial()

		#generate zipcode data
		zipcode = self.get_object().zipcode
		initial["zip_code_data"] = zipcode
		return initial

	def form_valid(self, form):
		obj = self.get_object()
		obj.tag_set.clear()

		# product = Product.objects.get(id=product_id)
		zip_code_data = form.cleaned_data.get("zip_code_data")
		if zip_code_data:
			zipcode_obj, created = Zipcode.objects.get_or_create(zipcode=zip_code_data)
			form.instance.zipcode = zipcode_obj

		return super(ProductUpdateView, self).form_valid(form)

class ProductDeleteView(ProductManagerMixin, DeleteView):
	model = Product

	def get_success_url(self):
		return reverse("sellers:product_list")

class ProductDetailView(MultiSlugMixin, DetailView):
	model = Product

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()

		return context


class SellerProductListView(SellerAccountMixin, ListView):
	model = Product
	template_name = "sellers/product_list_view.html"
	#paginate the seller list edit view
	paginate_by = 10

	def get_queryset(self, *args, **kwargs):
		qs = super(SellerProductListView, self).get_queryset(**kwargs)
		qs = qs.filter(seller=self.get_account()).order_by("-timestamp")
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)
				).order_by("-timestamp")
		return qs


class VendorListView(ListView):
	model = Product
	template_name = "products/product_list.html"
	paginate_by = 12

	def get_object(self):
		username= self.kwargs.get("vendor_name")
		seller = get_object_or_404(SellerAccount, user__username=username)
		return seller

	def get_context_data(self, *args, **kwargs):
		context = super(VendorListView, self).get_context_data(*args, **kwargs)
		context["vendor_name"] = str(self.get_object().user.username)
		context["filter_form"] = ProductFilterForm(data=self.request.GET or None)
		return context

	def get_queryset(self, *args, **kwargs):
		seller = self.get_object()
		qs = super(VendorListView, self).get_queryset(**kwargs).filter(seller=seller).order_by("-timestamp")
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)
				).order_by("-timestamp")
		return qs


class ProductFilter(FilterSet):
	title = CharFilter(name='title', lookup_type='icontains', distinct=True)
	min_price = NumberFilter(name='price', lookup_type='gte', distinct=True) # (some_price__gte=somequery)
	max_price = NumberFilter(name='price', lookup_type='lte', distinct=True)
	class Meta:
		model = Product
		fields = [
			'min_price',
			'max_price',
			'title',
			'description',
		]

class FilterMixin(object):
	filter_class = None
	search_ordering_param = "ordering"

	def get_queryset(self, *args, **kwargs):
		try:
			qs = super(FilterMixin, self).get_queryset(*args, **kwargs)
			return qs
		except:
			raise ImproperlyConfigured("You must have a queryset in order to use the FilterMixin")

	def get_context_data(self, *args, **kwargs):
		context = super(FilterMixin, self).get_context_data(*args, **kwargs)
		qs = self.get_queryset()
		ordering = self.request.GET.get(self.search_ordering_param)
		if ordering:
			qs = qs.order_by(ordering)
		filter_class = self.filter_class
		if filter_class:
			f = filter_class(self.request.GET, queryset=qs)
			context["object_list"] = f
		return context

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from geopy.geocoders import Nominatim
geolocator = Nominatim()


class ProductListView(FilterMixin, ListView):
	model = Product
	paginate_by = 12
	filter_class = ProductFilter

	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		context["filter_form"] = ProductFilterForm(data=self.request.GET or None)
		return context

	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(**kwargs).order_by("-timestamp")
		query = self.request.GET.get("q")

		#location for distance
		user_location = self.request.GET.get("location")
		distance = self.request.GET.get('distance_from')

		if user_location and distance:
			#get distance in miles and turn into degrees
			user_distance = change_in_longitude(change_in_latitude(int(distance)), int(distance))
			#turn user location into geopy Code
			location = geolocator.geocode("%s" %(user_location))
			user_lat_lon = Point(location.longitude, location.latitude)
			#run query
			zipcodes = Zipcode.objects.filter(geom__dwithin=(user_lat_lon, user_distance))
			raw_zipcode_list = [x.zipcode for x in zipcodes]
			products = qs.filter(
				Q(zipcode__zipcode__in=raw_zipcode_list)
			).order_by("-timestamp")
			return products

		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)|
					Q(seller__user__username__icontains=query)|
					Q(city__icontains=query)
				).order_by("-timestamp")

		return qs
