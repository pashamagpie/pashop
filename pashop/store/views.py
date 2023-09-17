from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from cart.views import _get_cart_id
from core.models import Category, Product, CartItem


def store(request, category_slug=None):
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(
            category=selected_category, is_available=True
        )
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    products_count = products.count()
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'products': paged_products,
        'products_count': products_count
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    in_cart = CartItem.objects.filter(
        cart__cart_id=_get_cart_id(request),
        product=product
    ).exists()
    context = {'product': product, 'in_cart': in_cart}
    return render(request, 'store/product_detail.html', context)


def search(request):
    products = None
    products_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(
                Q(name__icontains=keyword) | Q(description__icontains=keyword)
            ).order_by('id')
            products_count = products.count()
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'products_count': products_count
    }
    return render(request, 'store/store.html', context)
