from django.contrib import admin
from django.core.paginator import Paginator

from app.models import *

# Register your models here.
@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','release_date','is_allowed')
@admin.register(Shifts)
class ShiftsAdmin(admin.ModelAdmin):
    search_fields = ['name_of_shift']
@admin.register(Positions)
class PositionsAdmin(admin.ModelAdmin):
    search_fields = ['name_of_position']
@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    search_fields = ['name']
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    search_fields = ['name']
@admin.register(PaymentTypes)
class PaymentTypesAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','is_active')
@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Authors)
class AuthorsAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name','sex']

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','price','date_of_expiry',)

@admin.register(Libraries)
class LibrariesAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','address','branch')

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    search_fields = ['price']
    list_filter = ['price']
    list_display = ('price','is_success','payment_type')

@admin.register(ChillZones)
class ChillZonesAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','is_active','free_seats','branch')

@admin.register(CategoryChillZones)
class CategoryChillZonesAdmin(admin.ModelAdmin):
    list_filter = ['is_available','updated_at']

@admin.register(BorrowABooks)
class BorrowABooksAdmin(admin.ModelAdmin):
    list_display = ('transaction_type','borrow_at')
    list_filter = ['transaction_type','borrow_at']

admin.site.register(ChillZoneBookings)

admin.site.register(Orders)

admin.site.register(Receipts)

admin.site.register(BorrowABook)

admin.site.register(ReceiptProducts)

@admin.register(LibraryBook)
class LibraryBookAdmin(admin.ModelAdmin):
    list_filter = ['library']
    list_display = ('library','book','quantity')

@admin.register(Suppliers)
class SuppliersAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','phone_number','email')

