from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404
# Create your views here.

from django.views.generic.edit import FormMixin

from .forms import NewSellerForm
from .models import SellerAccount
from products.models import Product
from .mixins import SellerAccountMixin

class SellerProductDetailRedirectView(RedirectView):
	permanent = True
	def get_redirect_url(self, *args, **kwargs):
		obj = get_object_or_404(Product, slug=kwargs['slug'])
		return obj.get_absolute_url()

class SellerDashboard(SellerAccountMixin, FormMixin, View):
	form_class = NewSellerForm
	template_name = 'sellers/dashboard.html'
	success_url = "/seller/"

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			return self.form_valid(form)
		else:
			context = {
				'apply_form': form,
				'title': "Apply for Account",
			}
			return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		apply_form = self.get_form() #NewSellerForm()
		account = self.get_account()
		exists = account
		active = None

		context = {}

		if exists:
			active = account.active

		if not exists and not active:
			context["title"] = "Apply for Account"
			context["apply_form"] = apply_form
			context["active"] = active
		elif exists and not active:
			context["title"] = "Account Under Investigation"
			context["active"] = active
		elif exists and active:
			context["title"] = "Seller Dashboard"
			context["active"] = active
			#order by -timestamp and limit to top 4 on the seller dashboard
			context["products"] = self.get_products().order_by("-timestamp")[:4]
		else:
			pass

		return render(request, "sellers/dashboard.html", context)

	def form_valid(self, form):
		valid_data = super(SellerDashboard, self).form_valid(form)
		obj = SellerAccount.objects.create(user=self.request.user)
		return valid_data
