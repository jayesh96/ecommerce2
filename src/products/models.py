from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
# Create your models here.

class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self, *args, **kwags):
		return self.get_queryset().active()

class Product(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	quantity = models.IntegerField(default=0)
	active = models.BooleanField(default=True)

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