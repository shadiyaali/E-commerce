from django.shortcuts import render
from store.models import product

# Create your views here.


def index(request):
    products = product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }

    return render(request, 'accounts/index.html',context)

