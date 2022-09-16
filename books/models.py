from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#To save book_store information
class StoreData(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE) # it will fetch the user from user table of whome store is
    store_name = models.CharField(max_length = 150)
    loc = models.CharField(max_length = 150)

    def __str__(self):
        return self.store_name

#To save books information related to a particular store
class BooksData(models.Model):
    store = models.ForeignKey(StoreData, on_delete = models.CASCADE)
    count = models.IntegerField(default = 0)
    bookid = models.CharField(max_length = 200)
    img = models.ImageField()
    bookname = models.CharField(max_length = 300)
