from django.shortcuts import render
from store.models import Product

# Create your views here.


def index(request):
    products = Product.objects.all().filter(is_available=True)
    print(products)
    context = {
        'products': products,
    }

    return render(request, 'accounts/index.html',context)

