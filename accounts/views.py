from django.shortcuts import render
from .models import Product, Customer, Order


def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    pending = orders.filter(status='Pending').count()
    delivered = orders.filter(status='Delivered').count()

    context = {'customers': customers, 'orders': orders, 'total_customers': total_customers,
               'total_orders': total_orders, 'pending': pending, 'delivered': delivered}
    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()

    context = {"customer": customer, "orders": orders}
    return render(request, 'accounts/customer.html', context)
