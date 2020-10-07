from django.shortcuts import render, get_object_or_404

from .models import Category, Product
from .recommender import Recommender
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    return render(
        request,
        "shopp/product/list.html",
        {"category": category, "categories": categories, "products": products},
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    categories = Category.objects.all()
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(
        request,
        "shopp/product/detail.html",
        {
            "product": product,
            "categories": categories,
            "cart_product_form": cart_product_form,
            "recommended_products": recommended_products,
        },
    )
