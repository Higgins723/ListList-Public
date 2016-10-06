from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ["title"]

    def __unicode__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("categories:category_detail", kwargs={"slug": self.slug})

    def get_category_image_url(self):
        img = self.categoryimage_set.first()
        if img:
            return img.image.url
        return img


def image_upload_to_category(instance, filename):
    title = instance.category.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (basename, instance.id, file_extension)
    return "categories/%s/%s" % (slug, new_filename)

class CategoryImage(models.Model):
    category = models.ForeignKey(Category)
    image = models.ImageField(upload_to=image_upload_to_category)

    def __unicode__(self):
        return self.category.title