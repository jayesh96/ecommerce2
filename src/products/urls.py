from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import(
    ProductListView,
    ProductDetailView
    )
urlpatterns = [
    # Examples:
    url(r'^$', ProductListView.as_view(template_name="products/product_list.html"), name='products'),
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(template_name="products/product_detail.html"), name='product_detail'),
    # url(r'^(?P<id>\d+)$', product_detail_view_func, name='product_detail_function'),

]
