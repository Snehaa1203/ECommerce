var updateBtns = document.getElementsByClassName('update-cart') //querying all items in update car class we created in add cart button option

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){ //adding event on evry button item on click
		var productId = this.dataset.product
		var action = this.dataset.action //getting both values 
		console.log('productId:', productId, 'Action:', action)

		console.log('USER:', user)
		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
			
		}else{
			updateUserOrder(productId,action)
		}

	})
}
function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}
function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'  //which view.func to be rendered

		fetch(url, { //fetching url in backend
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken
			}, 
			body:JSON.stringify({'productId':productId, 'action':action}) //data to be send as object stringify makes it a string
		})
		.then((response) => {   //getting promise to know item was added
		   return response.json();
		})
		.then((data) => {
		    console.log('Data:', data) //printing the string value we get from json response "item was added"
			location.reload()
		});
}