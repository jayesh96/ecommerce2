from django.contrib import admin

# Register your models here.
from .models import Product,Variation,ProductImage,Category

class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 0

class VariationInline(admin.TabularInline):
	model = Variation
	extra = 0

class VariationAdmin(admin.ModelAdmin):
	list_display = ["id","title","price","product","price","sale_price","active","inventory"]
	class Meta:
		model = Variation

class ProductAdmin(admin.ModelAdmin):
	list_display = ["title","price","active","default"]
	inlines = [
	VariationInline,ProductImageInline
	]
	class Meta:
		model = Product


admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ProductImage)
admin.site.register(Category)

