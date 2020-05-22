from django.db import models
from datetime import datetime

# Create your models here.

class Realtor(models.Model):
	name = models.CharField(max_length=120)
	image = models.ImageField(upload_to="photos/%Y/%m/%d", blank=True)
	description = models.TextField(blank=True)
	email = models.CharField(max_length=100, blank=True)
	phone = models.CharField(max_length=40, blank=True)
	is_mvp = models.BooleanField(default=False)
	hired_date = models.DateTimeField(default=datetime.now, blank=True)
	
	def __str__(self):
		return self.name




class Listing(models.Model):
	realtor = models.ForeignKey(Realtor, on_delete=models.CASCADE)
	title = models.CharField(max_length=150)
	price = models.IntegerField()
	description = models.TextField(blank=True, null=True)
	address = models.CharField(max_length=400, blank=True)
	state = models.CharField(max_length=30, blank=True)
	city =models.CharField(max_length=60, blank=True)
	zipcode = models.CharField(max_length=20, blank=True)
	area = models.FloatField(blank=True)
	lot_size = models.DecimalField(blank=True, max_digits=5, decimal_places=1, null=True)
	bedroom = models.IntegerField(blank=True)
	bathroom = models.DecimalField(blank=True, max_digits=2, decimal_places=1)
	d_time = models.DateTimeField(auto_now_add=True, blank=True) #default=datetime.now
	garage = models.IntegerField(default=0)
	image_main = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
	image_1 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
	image_2 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
	image_3 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
	image_4 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
	image_5 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
	image_6 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
	is_published = models.BooleanField(default=True)
	
	def __str__(self):
		return self.title
		
		
		
class Contact(models.Model):
	listing = models.CharField(max_length=150)
	listing_id = models.IntegerField()
	user_id = models.IntegerField()
	name = models.CharField(max_length=150)
	email = models.CharField(max_length=180)
	phone = models.CharField(max_length=50)
	date_created = models.DateTimeField(default=datetime.now)
	message = models.TextField(blank=True)
	
	def __str__(self):
		return self.name
	
	
	
	
