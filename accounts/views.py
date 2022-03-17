from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import Product, Customer, Order
from .forms import OrderForm
from .filters import OrderFilter


def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all().order_by('-date_created')

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

    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs

    context = {"customer": customer, "orders": orders, 'my_filter': my_filter}
    return render(request, 'accounts/customer.html', context)


def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)

    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
