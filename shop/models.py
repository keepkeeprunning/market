from django.db import models

class Product(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=500)
  category = models.ForeignKey('Category', 
                               on_delete='CASCADE', 
                               null=True, 
                               blank=True, 
                               related_name='products')
  def __str__(self):
    return self.title

class Category(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=5000, blank=True)
  def __str__(self):
    return self.title
  