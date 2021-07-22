from django.db import models
from django.contrib.auth.models import User
class Customer(models.Model):
	user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE) #one to one means one user can have one customer and vice versa
	name=models.CharField(max_length=200,null=True)
	email=models.EmailField(max_length=200,null=True)
	def __str__(self):
		return self.name
	
class Product(models.Model):
	name=models.CharField(max_length=200,null=True)
	price=models.DecimalField(max_digits=5,decimal_places=2)
	digital=models.BooleanField(default=False,null=True,blank=False)#to check wether we need to ship it or not
	image=models.ImageField(null=True)

	def __str__(self):
		return self.name

	@property #if image is not present else we will get error if we dont want to use decorator simply use product.image.url in store.html
	def imageURL(self):
		try:
			url=self.image.url
		except:
			url=""
		return url

    
class Order(models.Model):
	customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
	date_ordered=models.DateTimeField(auto_now_add=True)
	complete=models.BooleanField(default=False,null=True,blank=False)
	transaction_id=models.CharField(max_length=200,null=True)
	def __str__(self):
		return str(self.id)

	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all() #if any one item is physical we will display the shipping page
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping


	@property
	def get_cart_total(self):
		orderitem=self.orderitem_set.all() #getting all orderitem in a given order in orderitem
		total=sum(item.get_total for item in orderitem) #looping over diff orderitems in a given order
		return total

	def get_cart_items(self):
		orderitem=self.orderitem_set.all() 
		total=sum(item.quantity for item in orderitem)
		return total
# Create your models here.
class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)#multiple orders multiple items in cart
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total=self.product.price*self.quantity
		return total


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)#if order gets deleted we ll still have shipping address feild
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address