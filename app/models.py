from django.contrib.auth.models import Group
from django.db import models as m

from users.models import User, Employee


# Create your models here.

class Suppliers(m.Model):
    name = m.CharField(max_length=100)
    age = m.SmallIntegerField()
    about=m.TextField()
    phone_number = m.CharField(max_length=20)
    email = m.EmailField(null=True)
    def __str__(self):
        return self.name

class Categories(m.Model):
    name = m.CharField(max_length=100)
    def __str__(self):
        return self.name

class Shifts(m.Model):
    name_of_shift = m.CharField(max_length=100)
    start_shift= m.TimeField()
    end_shift = m.TimeField()
    def __str__(self):
        return self.name_of_shift

class Positions(m.Model):
    name_of_position = m.CharField(max_length=100)
    default_group = m.ForeignKey(Group, null=True, blank=True, on_delete=m.SET_NULL)
    def __str__(self):
        return self.name_of_position

class Cities(m.Model):
    name=m.CharField(max_length=100)
    def __str__(self):
        return self.name

class PaymentTypes(m.Model):
    name=m.CharField(max_length=100)
    is_active=m.BooleanField(default=True)
    def __str__(self):
        return self.name

class Genres(m.Model):
    name=m.CharField(max_length=100)
    def __str__(self):
        return self.name

class Authors(m.Model):
    name=m.CharField(max_length=100)
    about=m.TextField()
    sex=(('Female','Female'),('Male','Male'))
    sex=m.CharField(choices=sex,default='Female',max_length=10)
    date_of_birth=m.DateField(null=True,blank=True)
    date_of_death=m.DateField(null=True,blank=True)
    image_url = m.URLField(max_length=500, null=True, blank=True)
    def __str__(self):
        return self.name

class Books(m.Model):
    name=m.CharField(max_length=100)
    release_date=m.DateField()
    original_language=m.CharField(max_length=100)
    rented=m.PositiveIntegerField(default=0)
    rent_price=m.DecimalField(max_digits=10,decimal_places=2,help_text='Rental price per day ༼ つ ◕_◕ ༽つ')
    price=m.DecimalField(max_digits=10,decimal_places=2)
    is_allowed=m.BooleanField(default=True)
    image_url = m.URLField(max_length=500, null=True, blank=True)
    author=m.ManyToManyField(Authors,related_name='books')
    genre=m.ManyToManyField(Genres,related_name='books')
    def __str__(self):
        return self.name

class Products(m.Model):
    name=m.CharField(max_length=100)
    price=m.DecimalField(max_digits=10,decimal_places=2)
    date_of_expiry=m.DateField()
    image_url = m.URLField(max_length=500, null=True, blank=True)
    category=m.ManyToManyField(Categories,related_name='category')
    supplier=m.ManyToManyField(Suppliers,related_name='suppliers')
    def __str__(self):
        return self.name

class Libraries(m.Model):
    name = m.CharField(max_length=100)
    address = m.CharField(max_length=100)
    square = m.SmallIntegerField()
    branch = m.CharField(max_length=10)
    book = m.ManyToManyField(Books, through='LibraryBook', related_name='libraries')
    city = m.ForeignKey(Cities, on_delete=m.CASCADE)
    shift = m.ManyToManyField(Shifts, related_name='shift')
    payment_type = m.ManyToManyField(PaymentTypes, related_name='payment_type')
    def __str__(self):
        return self.name

class LibraryBook(m.Model):
    library = m.ForeignKey(Libraries, on_delete=m.CASCADE, related_name='library_books')
    book = m.ForeignKey(Books, on_delete=m.CASCADE, related_name='library_books')
    quantity = m.PositiveIntegerField(default=0)
    class Meta:
        unique_together = ('library', 'book')
    def __str__(self):
        return f'{self.book} - {self.library} ({self.quantity} шт.)'

class Payments(m.Model):
    price=m.DecimalField(max_digits=10,decimal_places=2)
    is_success=m.BooleanField(default=False)
    payment_type=m.ForeignKey(PaymentTypes,on_delete=m.PROTECT)
    def __str__(self):
        return str(self.price)

class ChillZones(m.Model):
    name = m.CharField(max_length=100)
    branch=m.CharField(max_length=10)
    capacity=m.PositiveIntegerField(default=25)
    free_seats=m.PositiveIntegerField(default=0)
    is_active=m.BooleanField(default=True)
    square=m.SmallIntegerField()
    payment_type=m.ForeignKey(PaymentTypes,on_delete=m.PROTECT)
    library=m.ForeignKey(Libraries,on_delete=m.CASCADE,related_name='chill_zones')
    def __str__(self):
        return f'{self.name} ({self.branch})'

class ChillZoneBookings(m.Model):
    client = m.ForeignKey('users.User', on_delete=m.CASCADE, related_name='chill_zone_bookings')
    chill_zone = m.ForeignKey(ChillZones, on_delete=m.CASCADE, related_name='bookings')
    seats = m.PositiveIntegerField(default=1)
    created_at = m.DateTimeField(auto_now_add=True)
    is_active = m.BooleanField(default=True)

    def __str__(self):
        return f'{self.client} - {self.chill_zone} ({self.seats})'

class CategoryChillZones(m.Model):
    updated_at=m.DateField(auto_now=True)
    category=m.ForeignKey(Categories,on_delete=m.CASCADE,related_name='category_chill_zones')
    chill_zone=m.ForeignKey(ChillZones,on_delete=m.CASCADE,related_name='category_chill_zones')
    is_available=m.BooleanField(default=False)
    class Meta:
        unique_together = ('category', 'chill_zone')

    def __str__(self):
        return f'{self.category} - {self.chill_zone} - {self.is_available}'

class Orders(m.Model):
    created_at=m.DateField(auto_now_add=True)
    note=m.TextField(blank=True, null=True)
    client=m.ForeignKey(User,on_delete=m.CASCADE,related_name='orders')
    chill_zone=m.ForeignKey(ChillZones,on_delete=m.CASCADE)
    employee=m.ForeignKey(Employee,on_delete=m.SET_NULL,null=True,blank=True,related_name='orders')
    payment=m.OneToOneField(Payments, on_delete=m.CASCADE)

    def __str__(self):
        employee_name = self.employee.user.name if self.employee_id else 'Самообслуживание （づ￣3￣）づ╭❤️～'
        return f'{self.chill_zone.branch} - {employee_name} - {self.payment}'

class BorrowABooks(m.Model):
    choice=(('rent','rent'),('purchase','purchase'))
    transaction_type=m.CharField(choices=choice,max_length=50,default='rent')
    borrow_at = m.DateField()
    until = m.DateField(null=True, blank=True)
    library = m.ForeignKey(Libraries, on_delete=m.CASCADE)
    employee = m.ForeignKey(Employee, on_delete=m.SET_NULL, related_name='borrow_books', null=True, blank=True)
    client_card = m.ForeignKey(User, on_delete=m.CASCADE, related_name='borrow_books')
    payment=m.OneToOneField(Payments, on_delete=m.CASCADE)
    book = m.ManyToManyField(Books, through='BorrowABook', related_name='borrow_books')
    def __str__(self):
        return f'{self.borrow_at} - {self.until}'

class BorrowABook(m.Model):
    borrow_at = m.ForeignKey(BorrowABooks, on_delete=m.CASCADE, related_name='borrow_book')
    book = m.ForeignKey(Books, on_delete=m.CASCADE, related_name='borrow_book')
    returned_at = m.DateField(blank=True, null=True)
    def __str__(self):
        return f'{self.borrow_at} - {self.book}'

    @property
    def is_returned(self):
        return self.returned_at is not None

class Receipts(m.Model):
    create_at=m.DateField(auto_now_add=True)
    order=m.OneToOneField(Orders,on_delete=m.CASCADE,related_name='receipts')
    def __str__(self):
        return f'{self.create_at} - {self.order.chill_zone.branch}'

class ReceiptProducts(m.Model):
    product=m.ForeignKey(Products,on_delete=m.CASCADE)
    receipt=m.ForeignKey(Receipts,on_delete=m.CASCADE)
    quantity=m.PositiveIntegerField(default=0)
    total_amount=m.DecimalField(max_digits=10,decimal_places=2)
    def __str__(self):
        return f'{self.product.name} - {self.receipt}'

# ProductOrders/ProductOrderItems убраны: отдельная "покупка без визита"
# не имела смысла (некому доставлять товар) — товары теперь заказываются
# только как меню внутри посещения зоны отдыха, через существующие
# Orders → Receipts → ReceiptProducts.