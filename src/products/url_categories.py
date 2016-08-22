from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import CategoryListView, CategoryDetailView
urlpatterns = [
    # Examples:
    url(r'^$', CategoryListView.as_view(template_name="products/product_list.html"), name='categories'),
    url(r'^(?P<slug>[\w-]+)/$', CategoryDetailView.as_view(template_name="products/category_detail.html"), name='category_detail'),
 
    # url(r'^(?P<id>\d+)$', product_detail_view_func, name='product_detail_function'),

]
