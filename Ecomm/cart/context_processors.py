from . models import Cart,CartItem,WishlistItem
from .views import _cart_id
from django.core.exceptions import ObjectDoesNotExist

#CART ICON COUNT
def counter( request ):
    cart_count=0
    if 'admin' in request.path:
        return ()
    else:
        try:
            cart= Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:    
              cart_items=CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
             cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict (cart_count=cart_count)

        

#SIDE CART 
def sidecart(request, total=0, quantity=0, cart_items=None):
    wishedcount=0
    try:
        if request.user.is_authenticated:
           cart_items   = CartItem.objects.filter(user=request.user, is_active=True)
        else:
           cart         = Cart.objects.get(cart_id=_cart_id(request))
           cart_items   = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        wisheditems =WishlistItem.objects.filter(user=request.user.id)
        wishedcount=wisheditems.count() 

    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'wishedcount': wishedcount,
    }
    return dict(context)

