from django.contrib import admin
from .models import BooksData, StoreData
# Register your models here.

class StoreDataAdmin(admin.ModelAdmin):
    list_display = ['user', 'store_name', 'loc']

class BooksDataAdmin(admin.ModelAdmin):
    list_display = ['store', 'count', 'bookid', 'img', 'bookname']

admin.site.register(StoreData, StoreDataAdmin)
admin.site.register(BooksData, BooksDataAdmin)
