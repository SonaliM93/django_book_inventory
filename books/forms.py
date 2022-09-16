from django import forms
from .models import StoreData, BooksData


class Add_Store_Form(forms.ModelForm):
    class Meta:
        model = StoreData
        fields = ["store_name","loc"]
        labels = {'store_name': 'Store Name',
                  'loc': 'Location'}


class Add_Books_Form(forms.ModelForm):
    class Meta:
        model = BooksData
        fields = '__all__'
        labels = {'bookname': 'Title of book',
                  'count': 'Quantity'}

class Search_Book_Form(forms.Form):
    search = forms.CharField(max_length=1000)
