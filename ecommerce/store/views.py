#username Sneha psswd sneha1203
from django.shortcuts import render
from .models import *
from django.http import JsonResponse 
import json#bcs we dont want to return any template or kind of thing we just need to have a message kind of thing json subclass of httpresponse json cant render out templates
import datetime
from.utility import*
# Create your views here.
def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.all()
	context = {'products':products,'cartItems':cartItems}
	return render(request,'store/store.html',context)

def cart(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
		
	context = {'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'store/cart.html', context)


def checkout(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	context ={'items':items,'order':order,'cartItems':cartItems,}
	return render(request,'store/checkout.html',context)

def update_item(request):
	#return JsonResponse('item was added',safe=False) #if we dont use safe=false we wont be able to send first param as string as only dict is allowed default safe=true
	data = json.loads(request.body) #getting whole body of json before we were getting only string
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False) #same logic as checkout if object is not there we create one

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp() #using datetime to set t_id
	data = json.loads(request.body) #we parsed the data in body of json now we access it

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		
	else:
		customer,order=guestOrder(request, data)
		
	total = float(data['form']['total']) #like 2d array
	order.transaction_id = transaction_id
	if total == order.get_cart_total:
			order.complete = True
	order.save()

	if order.shipping == True:
			ShippingAddress.objects.create( #model
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
	return JsonResponse('Payment Complete',safe=False)
