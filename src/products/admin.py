from django.contrib import admin

# Register your models here.
from .models import Product,Variation,ProductImage,Category

class VariationAdmin(admin.ModelAdmin):
	list_display = ["title","price","product","price","sale_price","active","inventory"]
	class Meta:
		model = Variation

class ProductAdmin(admin.ModelAdmin):
	list_display = ["title","price","quantity","active","default"]
	class Meta:
		model = Product


admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ProductImage)
admin.site.register(Category)

