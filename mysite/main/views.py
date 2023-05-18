from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Books, Author, Customers, Order
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password 
from django.views.generic import ListView
from django.db.models import Q
from django.http import HttpResponse
from django.views import View 
from django.contrib import messages 


# Create your views here.
class SearchView(ListView):
    model = Books
    template_name = "main/books_list.html"
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Books.objects.filter(
            Q(book_name__icontains=query)
        )
        if object_list.exists():
            return object_list
        else:
            return messages.info(self.request, "Your Book is't available...")
            


class Login(View):

    return_url = None
    def get(self, request):
        Login.return_url = request.GET.get("return_url")
        return render(request=request, template_name='main/login.html')

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        customer = Customers.get_customers_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    return_url = None
                    return redirect("main:homepage")
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        print(email, password)
        return render(request=request, 
                      template_name="main/login.html", 
                      context={"error":error_message})


class Signup(View):

    def get(self, request):
        return render(request=request, 
                      template_name="main/signup.html")

    def post(self, request):
        postData = request.POST 
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }

        error_message = None
        customer = Customers(firstname=first_name,
                             lastname=last_name,
                             phone=phone,
                             email=email,
                             password=password)

        error_message = self.validateCustomer(customer)
        print(error_message)
        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('main:homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request=request, 
                          template_name='main/signup.html', 
                          context={"data":data})


    def validateCustomer(self, customer):
        error_message = None
        if (not customer.firstname):
            error_message = "Please Enter your First Name !!"
        elif len(customer.firstname) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.lastname:
            error_message = 'Please Enter your Last Name'
        elif len(customer.lastname) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not customer.phone:
            error_message = 'Enter your Phone Number'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.ifExist():
            error_message = 'Email Address Already Registered..'

        return error_message


class OrderView(View):

    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_order_by_customer(customer)
        print(orders)
        return render(request=request, 
                      template_name='main/orders.html', 
                      context={'orders': orders})


def logout(request):
    request.session.clear()
    return redirect('/')


def homepage(request):
    return render(request=request,
                  template_name='main/home.html',
                  context={"Books":"Let's go to the site"})


def books(request):
    author = Author.objects.all()
    return render(request=request,
                  template_name="main/authorpage.html",
                  context={"author":author})


def authors(request, authors):
    name_author = [a.name for a in Author.objects.all()]
    if authors in name_author:
        books_this_author = Books.objects.filter(book_author__name=authors)
        return render(request=request, 
                      template_name="main/bookpage.html",
                      context={"book":books_this_author.all()})


def buy(request, n_book, authors):
    book = Books.objects.filter(book_name=n_book)
    if request.method=="POST":
        customer = request.session.get('customer')
        address = request.POST.get("Address")
        phone = request.POST.get("phone")
        print(address, phone, Customers(id=customer))
        for b in book:
            print(b.book_name)
            order = Order(book_product=b,
                          customer=Customers(id=customer),
                          price=b.price,
                          address=address,
                          phone=phone)
            order.save()
        return redirect("/orders")
        
    return render(request=request,
                template_name="main/buy.html",
                context={"data":book})

