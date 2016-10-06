from __future__ import unicode_literals
from django.conf import settings

from django.db import models
from products.models import Product

# Create your models here.
class CommentManager(models.Manager):
	def create_comment(self, user=None, comment=None, path=None, product=None):
		if not path:
			raise ValueError("Must include a path when adding a Comment")
		if not user:
			raise ValueError("Must include a user when adding a Comment")

		comment = self.model(
			user = user,
			path = path,
			comment = comment
		)
		if product is not None:
			comment.product = product
		comment.save(using=self._db)
		return comment


class Comment(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	path = models.CharField(max_length=350)
	product = models.ForeignKey(Product, null=True, blank=True)
	text = models.TextField()
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	active = models.BooleanField(default=True)

	objects = CommentManager()

	def __unicode__(self):
		return str(self.user.username)

	@property
	def get_comment(self):
		return self.text