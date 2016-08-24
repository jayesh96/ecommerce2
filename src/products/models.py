from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
# Create your models here.

class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self, *args, **kwags):
		return self.get_queryset().active()

	def get_related(self, instance):
		products_one = self.get_queryset().filter(categories__in = instance.categories.all())
		products_two = self.get_queryset().filter(default = instance.default)
		qs = (products_one | products_two).exclude(id=instance.id).distinct()
		return qs

class Category(models.Model):
	title = models.CharField(max_length=120, null=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("category_detail", kwargs={"slug": self.slug})


class Product(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	quantity = models.IntegerField(default=0)
	active = models.BooleanField(default=True)
	categories = models.ManyToManyField(Category, blank=True)
	default = models.ForeignKey(Category, related_name='default_category', null=True, blank=True)


	objects = ProductManager()

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("product_detail", kwargs={"pk": self.pk})


class Variation(models.Model):
	product = models.ForeignKey(Product)
	title = models.CharField(max_length=120)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	sale_price = models.DecimalField(decimal_places = 2,max_digits=20, null=True, blank=True)
	active = models.BooleanField(default=True)
	inventory = models.IntegerField(null=True,blank=True)

	def __unicode__(self):
		return self.title

	def get_price():
		if self.sale_price is not None:
			return self.sale_price
		else:
			return self.price

	def get_absolute_url(self):
		return self.product.get_absolute_url()

def product_self_saved_resolver(sender, instance, created,*args, **kwargs):
	product = instance
	variation = product.variation_set.all()
	#variation = Variation.objects.filter(product=product)
	print variation
	if variation.count() == 0:
		new_var = Variation()
	 	new_var.product = product
	 	new_var.title = "default"
	 	new_var.price = product.price
	 	new_var.save()

post_save.connect(product_self_saved_resolver, sender=Product)       


def image_upload_to(instance, filename):
	title = instance.product.title
	print title
	slug = slugify(title)
	print slug
	return "products/%s/%s" %(slug, filename)

class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = models.FileField(upload_to=image_upload_to)

	def __unicode__(self):
		return self.product.title




