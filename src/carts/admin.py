from django.contrib import admin

# Register your models here.

from .models import CartItem,Cart
class CartItemAdmin(admin.ModelAdmin):
	list_display = ["item","quantity"]
	class Meta:
		model = CartItem


admin.site.register(Cart)
admin.site.register(CartItem,CartItemAdmin)
