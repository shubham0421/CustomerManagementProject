from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

# Create your views here
from django.contrib.auth.models import Group
from .models import *
from .forms import OrderForm,CreateUserForm,CustomerForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from .decorators import  allowed_users, admin_only

from django.contrib import messages


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')

	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				user = form.save()
				username = form.cleaned_data.get('username')

				messages.success(request, 'Account was created for ' + username)

				return redirect('login')
			

	context={'form':form}
	return render(request,'accounts/register.html',context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')

	else:
		if request.method=='POST':
			username=request.POST.get('username')
			password=request.POST.get('password')

			user=authenticate(request,username=username,password=password)

			if user is not None:
				login(request,user)
				return redirect('home')

			else:
				messages.info(request,'Username Or Password is incorrect')

		context={}
		return render(request,'accounts/login.html',context)

def logoutUser(request):

	logout(request)
	return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	print('ORDERS:', orders)

	context = {'orders':orders, 'total_orders':total_orders,
	'delivered':delivered,'pending':pending}
	return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/accounts_settings.html', context)



	
@login_required(login_url='login')
@admin_only
def home(request):
	customers=Customer.objects.all()
	orders=Order.objects.all()

	total_orders=Order.objects.count()
	pending=Order.objects.filter(status="Pending").count()
	delivered=Order.objects.filter(status="Delivered").count()
	context={"customers":customers,"orders":orders,"total_orders":total_orders,"pending":pending,"delivered":delivered}
	return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products=Product.objects.all()
	return render(request,'accounts/products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer':customer, 'orders':orders, 'order_count':order_count,'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context) 

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createorder(request,pk):
	OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=4)
	customer=Customer.objects.get(id=pk)
	#form=OrderForm()
	formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
	if request.method=="POST":
		formset=OrderFormSet(request.POST,instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context={'formset':formset}
	return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateorder(request,pk):
	

	order=Order.objects.get(id=pk)
	form=OrderForm(instance=order)


	if request.method=="POST":
		form=OrderForm(request.POST,instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context={'form':form}
	return render(request,'accounts/updateform.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteorder(request,pk):
	
	order=Order.objects.get(id=pk)
	if request.method=='POST':
		order.delete()
		return redirect('/')

	context={'item':order}
	return render(request,'accounts/delete.html',context)

