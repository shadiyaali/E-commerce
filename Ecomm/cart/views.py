from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product, Variation
from order.models import Profile


from .models import Cart, CartItem, WishlistItem

# Create your views here.

# CREATING SESSION 
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart



#ADDING CART USING SESSION ID
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    current_user= request.user
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key   = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass          
        is_cart_item_exists = CartItem.objects.filter(product=product,user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product,user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)   # type: ignore
            if product_variation in ex_var_list:
                #increase card item
                index          = ex_var_list.index(product_variation)
                item_id        = id[index]
                item           = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product,quantity=1,user=current_user)
                if len(product_variation) > 0:
                  item.variation.clear()
                  item.variation.add(*product_variation)
                  item.save()
        else:
            cart_item = CartItem.objects.create(
                product  = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save() 
        return redirect('cart')

#IF USER IS NOT AUTHENTICATED 
    else:
        print("not authenti")    
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key   = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)                   
                except:
                    pass   
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
        except Cart.DoesNotExist:
            cart  = Cart.objects.create(cart_id =_cart_id(request))
        # product_variation = product_variation[::-1]
        cart.save()
        is_cart_item_exists = CartItem.objects.filter(product=product,cart = cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product,cart = cart)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)   # type: ignore
            if product_variation in ex_var_list:
                #increase card item
                index          = ex_var_list.index(product_variation)
                item_id        = id[index]
                item           = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation) > 0:
                 item.variation.clear()
                 item.variation.add(*product_variation)
                 item.save()
        else:
            cart_item  = CartItem.objects.create(
                product  = product,
                quantity = 1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
        return redirect('cart')



#REMOVE CART ITEM
def remove_cart(request,product_id,cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
           cart_item    = CartItem.objects.get(product=product,user=request.user, id=cart_item_id)
        else:
           cart    = Cart.objects.get(cart_id=_cart_id(request))
           cart_item    = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save() 
        else:
         cart_item.delete()
    except:
        pass   
    return redirect ('cart')   



#DELETE CART 
def delete_cart(request,product_id,cart_item_id):
    
    product   = get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(product=product,user=request.user,id=cart_item_id)
    else:
        cart      = Cart.objects.get(cart_id=_cart_id(request))    
        cart_item = CartItem.objects.filter(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()

    return redirect('cart')   



# GET THE CART ITEM 
def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0   
    try:
        if request.user.is_authenticated:
           cart_items   = CartItem.objects.filter(user=request.user, is_active=True)
        else:
           cart         = Cart.objects.get(cart_id=_cart_id(request))
           cart_items   = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total    += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total   = total+tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total'      : total,
        'quantity'   : quantity,
        'cart_items' : cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    
    return render(request, 'store/cart.html', context)



#CHECK OUT CONDITONS 
@login_required(login_url='signin')
def checkout(request,total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        
        if request.user.is_authenticated:
           cart_items   = CartItem.objects.filter(user=request.user, is_active=True)
           userprofile = Profile.objects.filter(user=request.user).first() 
        else:
           cart         = Cart.objects.get(cart_id=_cart_id(request))
           cart_items   = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total    += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            tax = (2 * total)/100
            grand_total   = total+tax
           
    except ObjectDoesNotExist:
        pass
    context = {
        'total'      : total,
        'quantity'   : quantity,
        'cart_items' : cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'userprofile': userprofile, #type:ignore 
    }

    return render(request,'store/checkout.html',context)  


@login_required(login_url='signin')
def add_to_wishlist(request):
    user = request.user
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    print(user, product)
    is_wished = WishlistItem.objects.filter(product=product)
    if not is_wished:
        
        product = WishlistItem.objects.create(
            user=user,
            product=product,
            is_active=True,
        )
    
    else:
        print("no")

    
    return JsonResponse({'single_product':'success'})

@login_required(login_url='signin')
def wishlist(request):
    products = WishlistItem.objects.filter(user=request.user, is_active=True)

    return render(request, 'store/wishlist.html', {'products':products})
def delete_from_wishlist(request):
    prod_id = request.GET['id']
    print(prod_id)
    product = Product.objects.get(id=prod_id)
    wishlist_item = WishlistItem.objects.get(product=product)
    wishlist_item.delete()
    return redirect('wishlist')  