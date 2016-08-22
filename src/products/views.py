from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
# Create your views here.

from .models import Product, Variation
from .forms import VariationInventoryFormSet
from .mixins import StaffRequiredMixin

class VariationListView(StaffRequiredMixin, ListView):
	model = Variation
	queryset = Variation.objects.all()
	
	def get_context_data(self, *args, **kwargs):
		context = super(VariationListView, self).get_context_data(*args, **kwargs)
		context["formset"] = VariationInventoryFormSet(queryset = self.get_queryset())
		
	 	return context

	def get_queryset(self, *args, **kwargs):
		product_pk = self.kwargs.get("pk")
		if product_pk:
			product = get_object_or_404(Product, pk=product_pk)
			queryset = Variation.objects.filter(product=product)	
				
		return queryset

	def post(self, request, *args, **kwargs):
		formset = VariationInventoryFormSet(request.POST, request.FILES)
		if formset.is_valid():
			formset.save(commit=False)
			for form in formset:
				new_item = form.save(commit=False)
				product_pk = self.kwargs.get("pk")
				product = get_object_or_404(Product, pk=product_pk)
				new_item.product = product
				new_item.save()

			messages.success(request, "Your Inventory is Updated")	
			return redirect('products')	
			



class ProductListView(ListView):
	model = Product
	queryset = Product.objects.all()
	
	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		context["query"] = self.request.GET.get("q")
		return context

	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = self.model.objects.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query)
				)
			try:
				qs2 = self.model.objects.filter(
					Q(price=query)
					)
				qs = (qs | qs2).distinct()
			except:
				pass
		return qs

class ProductDetailView(DetailView):
	model = Product


def product_detail_view_func(request, id):
 	product_instance = get_object_or_404(Product, id=id)
 	try:
 		product_instance = Product.objects.id(id=id)
 	except Product.DoesNotExist:
 		raise Http404
