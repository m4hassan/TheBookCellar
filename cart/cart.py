from core.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get the request
        self.request = request
        # Get the current session key if it exists
        cart = self.session.get('session_key')
        # If the user is new, no session key. Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        # Make sure cart is available on all pages of the site
        self.cart = cart


    def add(self, product, product_qty):
        """
        Add a product to cart
        """
        product_id = str(product.id)
        # Logic
        if product_id in self.cart:
            # self.cart[product_id] = int(product_qty)
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        
        self.session.modified = True

        # Deal with logged in user profile
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'3':1, '4':5} to {"3":1, "4":5} 
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            # Save Carty to the Profile model
            current_user.update(old_cart=carty)

    def db_add(self, product, product_qty):
        """
        Add products from the saved DB cart
        """
        if product in self.cart:
            pass
        else:
            self.cart[product] = int(product_qty)

        self.session.modified = True

        # Deal with logged in user profile
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'3':1, '4':5} to {"3":1, "4":5} 
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            # Save Carty to the Profile model
            current_user.update(old_cart=carty)
        

    def update(self, product, quantity):
        """
        Update a product in cart 
        """
        product_id = str(product)
        product_qty = int(quantity)
        # get cart {'2':4, '5':3}
        
        # update dict/cart
        self.cart[product_id] = product_qty
        # Deal with logged in user profile

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'3':1, '4':5} to {"3":1, "4":5} 
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            # Save Carty to the Profile model
            current_user.update(old_cart=carty)

        self.session.modified = True
        return self.cart
        

    def delete(self, product):
        """
        Delete a product from cart
        """
        product_id = str(product)

        # delete item from cart
        if product_id in self.cart:
            # ourcart.pop(product_id)
            del self.cart[product_id]
        
        self.session.modified = True
        # Deal with logged in user profile
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'3':1, '4':5} to {"3":1, "4":5} 
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            # Save Carty to the Profile model
            current_user.update(old_cart=carty)
        return f'Removed Product number {product_id} from cart'
    

    def __len__(self):
        """
        Returns numbers of items in cart
        """
        return len(self.cart)
    

    def get_prods(self):
        """
        Get list of products in cart
        """
        # Get product IDs in cart 
        product_ids = self.cart.keys()
        # Look up products in Products DB 
        products = Product.objects.filter(id__in=product_ids)

        return products


    def get_quants(self):
        """
        Get quantity of each product in cart
        """
        quantities = self.cart

        return quantities
    
    def cart_total(self):
        """
        Get running total of the cart
        """
        # Get products IDs in cart
        product_ids = self.cart.keys()
        # Look up those keys in product DB
        products = Product.objects.filter(id__in=product_ids)
        total = 0
        for key, value in self.cart.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sales:
                        total += (product.sales_price * value)
                    else:
                        total += (product.price * value)

        return total

    