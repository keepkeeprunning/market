from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Product
from .models import Category

class CategoryDetailView(generic.DetailView): #import django.views.generic
  template_name = 'category_detail.html'
  context_object_name = 'category'
  model = Category

class ProductDetailView(generic.DetailView):
  template_name = 'product_detail.html'
  model = Product

class MainPageView(generic.TemplateView):
  template_name = 'main_page.html'
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['categories'] = Category.objects.all()
    context['products'] = Product.objects.all()
    return context
