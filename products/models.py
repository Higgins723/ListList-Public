from __future__ import unicode_literals
from django.template.defaultfilters import truncatechars
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.conf import settings
from django.core.urlresolvers import reverse

from django.db import models

from sellers.models import SellerAccount

from zipcode.models import Zipcode

from category.models import Category

# Create your models here.
class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)


class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	#return all instances in database that are active
	def all(self, *args, **kwargs):
		return self.get_queryset().active()

	def get_related(self, instance):
		products_one = self.get_queryset().filter(categories=instance.categories)
		qs = (products_one).exclude(id=instance.id).distinct()
		return qs

def image_upload_to(instance, filename):
	return "%s/%s" %(instance.slug, filename)

PRODUCT_CONDITION = (
	('new', 'New'),
	('used - like new', 'Used - Like New'),
	('used - very good', 'Used - Very Good'),
	('used - good', 'Used - Good'),
	('used - acceptable', 'Used - Acceptable'),
)

class Product(models.Model):
	seller = models.ForeignKey(SellerAccount)
	title = models.CharField(max_length=120)
	main_img = models.ImageField(null=True, upload_to=image_upload_to)
	slug = models.SlugField(blank=True, unique=True)
	description = models.TextField()
	city = models.CharField(max_length=30, null=True)
	categories = models.ForeignKey(Category, null=True)
	condition = models.CharField(max_length=120, choices=PRODUCT_CONDITION, null=True)
	zipcode = models.ForeignKey(Zipcode)
	price = models.DecimalField(default=9.99, max_digits=100, decimal_places=2, blank=True, null=True)
	active_product = models.BooleanField(default=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		view_name = "products:detail_slug"
		return reverse(view_name, kwargs={"slug": self.slug})

	def get_edit_url(self):
		view_name = "sellers:product_edit"
		return reverse(view_name, kwargs={"slug": self.slug})

	def get_delete_url(self):
		view_name = "sellers:product_delete"
		return reverse(view_name, kwargs={"slug": self.slug})

	@property
	def short_description(self):
		return truncatechars(self.description, 50)

def attachment_upload_to(instance, filename):
	return "%s/%s" %(instance.product, filename)

class Attachment(models.Model):
	product = models.ForeignKey(Product)
	file = models.ImageField(upload_to=attachment_upload_to)


def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Product.objects.filter(slug=slug)
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug


def product_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(product_pre_save_reciever, sender=Product)



class CuratedProducts(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	section_name = models.CharField(max_length=120)
	products = models.ManyToManyField(Product, blank=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.section_name

