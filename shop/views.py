from django.shortcuts import render, redirect
from .forms import ProductForm


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_product')
    else:
        form = ProductForm()

    return render(request, 'shop/add_product.html', {'form': form})
