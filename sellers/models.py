from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
# from django.contrib.auth.signals import user_logged_in

# import stripe
# from listlist.stripe_info import secret_key

# stripe.api_key = secret_key

# Create your models here.


class SellerAccount(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="manager_sellers", blank=True)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)


	def __unicode__(self):
		return str(self.user.username)

	def get_absolute_url(self):
		return reverse("products:vendor_detail", kwargs={"vendor_name": self.user.username})

# class SellerStripe(models.Model):
# 	user = models.OneToOneField(settings.AUTH_USER_MODEL)
# 	stripe_id = models.CharField(max_length=120, null=True, blank=True)
# 	phone_number = models.CharField(max_length=12, null=True, blank=True)
#
# 	def __unicode__(self):
# 		return str(self.user.username)
#
# def CreateStripeID(sender, user, request, **kwargs):
# 	new_id, created = SellerStripe.objects.get_or_create(user=user)
# 	if created:
# 		stripe_cust = stripe.Customer.create(email=user.email)
# 		new_id.stripe_id = stripe_cust.id
# 		new_id.save()
#
# user_logged_in.connect(CreateStripeID)

