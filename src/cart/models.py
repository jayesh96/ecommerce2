from decimal import Decimal 
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save

from products.models import Variation
# Create your models here.

class CartItem(models.Model):
	id = models.AutoField(primary_key=True)
	cart = models.ForeignKey("Cart")
	item = models.ForeignKey(Variation)
	quantity = models.PositiveIntegerField(default=1)
	line_item_total = models.DecimalField(max_digits=10, decimal_places=2)
	def __unicode__(self):
		return self.item.title

	def remove(self):
		return self.item.remove_from_cart()

	def get_price(self):
		return self.item.get_price()

	def get_title(self):
		return "%s - %s" %(self.item.product.title,self.item.title )

def cart_item_pre_save_reciever(sender, instance, *args, **kwargs):
	qty = instance.quantity
	if qty >=1:
		price = instance.item.get_price()
		line_item_total = Decimal(qty) * Decimal(price)
		instance.line_item_total = line_item_total

pre_save.connect(cart_item_pre_save_reciever, sender=CartItem)	


def cart_item_post_save_reciever(sender, instance, *args, **kwargs):
	instance.cart.update_subtotal()

post_save.connect(cart_item_post_save_reciever, sender=CartItem)

class Cart(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True)
	items = models.ManyToManyField(Variation, through=CartItem)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	subtotal = models.DecimalField(max_digits=50, decimal_places=2)

	def __unicode__(self):
		return str(self.id)

	def update_subtotal(self):
		subtotal = 0
		items = self.cartitem_set.all()
		for item in items:
			subtotal += item.line_item_total
			print subtotal
		self.subtotal = subtotal
		self.save()