from store.models import Product
class Cart():
    def __init__(self, request):
        self.session = request.session

        # get the current seesion if it exists
        cart = self.session.get('session_key')
        # if user new, no session key so we create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}


        # make sure cart is available on all pages
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

    # logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True


    def __len__(self):
        return len(self.cart)

    def get_products(self):
        # getting id from cart
        product_ids = self.cart.keys()
        # use the ids to lookup prods in the database model
        products = Product.objects.filter(id__in=product_ids)
        # return the looked up products
        return products


    def get_quants(self):
        quantities = self.cart
        return quantities