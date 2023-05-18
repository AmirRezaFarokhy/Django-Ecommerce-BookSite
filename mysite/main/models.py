from django.db import models
import datetime


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    born_date = models.DateTimeField()

    def __str__(self):
        return self.name + self.last_name


class Books(models.Model):
    book_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    img_book = models.ImageField(upload_to="Desktop")
    publication = models.CharField(max_length=200)

    @staticmethod
    def get_products_by_id(ids):
        return Books.objects.filter(id__in=ids)
  
    @staticmethod
    def get_all_products():
        return Books.objects.all()
  
    @staticmethod
    def get_all_products_by_authors(category_id):
        if category_id:
            return Books.objects.filter(category=category_id)
        else:
            return Books.get_all_products()

    def __str__(self):
        return self.book_name


class Customers(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def register(self):
        self.save()
 
    @staticmethod
    def get_customers_by_email(email):
        try:
            return Customers.objects.get(email=email)
        except:
            return False
    
    def ifExist(self):
        if Customers.objects.filter(email=self.email):
            return True
        else:
            return False


class Order(models.Model):
    book_product = models.ForeignKey(Books, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    price = models.IntegerField()
    address = models.CharField(max_length=200, default="", blank=True)
    phone = models.CharField(max_length=50, default="", blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def PlaceOrder(self):
        self.save()

    @staticmethod
    def get_order_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')


        
