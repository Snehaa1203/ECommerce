import json
from .models import*  #contains the whole logic for guest user 
def cookieCart(request):
	try:
			cart = json.loads(request.COOKIES['cart'])
	except:
			cart = {}
			print('CART:', cart)
		#Create empty cart for now for non-logged in user
	items = []
	order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
	cartItems = order['get_cart_items']
	for i in cart:#whole logic for non logged in user
		    try:
				   cartItems += cart[i]['quantity']

				   product = Product.objects.get(id=i)
				   total = (product.price * cart[i]['quantity'])

				   order['get_cart_total'] += total
				   order['get_cart_items'] += cart[i]['quantity']
				   item = { #getting list items jaise logged in user ke lye cart me hota tha we are not saving this to our database just using js here .
					'id':product.id,
					'product':{'id':product.id,'name':product.name, 'price':product.price, 
					'imageURL':product.imageURL}, 'quantity':cart[i]['quantity'],
					'digital':product.digital,'get_total':total,
					}
				   items.append(item)#appending item to items dict we made above
				   if product.digital == False:
					   order['shipping'] = True #making shipping form accessible
		    except:
			     pass #we did this beaucse if the product gets removed somehow we dont want the guest user to see the error.
	return {'cartItems':cartItems ,'order':order, 'items':items}
def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		#object exists with given value toh okay else it will create one
		items = order.orderitem_set.all() #querying with parent table order we get orderitem
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']
	return {'cartItems':cartItems, 'order':order, 'items':items}	

def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items'] #item is a list of dict

	customer, created = Customer.objects.get_or_create(
			email=email, #we check if the customer is regularly shopping with us email can be same thats why name is outside maybe he changes name.
			)
	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for item in items:
		product = Product.objects.get(id=item['id']) #getting object by id we declared above in func
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=item['quantity'],
		)
	return customer, order