from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import StoreData, BooksData
from .forms import Add_Books_Form, Add_Store_Form, Search_Book_Form
import requests
import json

# Create your views here.

# Home Page View
def home_view(request):
    return render(request, 'books/home.html')

# Login Page View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            usrname = form.cleaned_data['username']
            passw = form.cleaned_data['password']
            user = authenticate(username=usrname, password=passw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/showstore/')
    else:
        form = AuthenticationForm()
    return render(request, 'books/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

# Sign-up View
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
    else:
        form = UserCreationForm()
    return render(request, 'books/signup.html', {'form': form})

# To show Stores of a particular user
def show_store_view(request):
    if request.user.is_authenticated:
        s = StoreData.objects.filter(user = request.user) #fetches data from storedata table based on user
        if s.exists():
            return render(request, 'books/showstores.html', {'data': s})
        else:
            return HttpResponseRedirect('/addstore/')
    else:
        return HttpResponseRedirect('/login/')

# To add new store for a particular user
def add_store_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST': # will execute when we click on submit button
            form = Add_Store_Form(request.POST)
            if form.is_valid():
                user = request.user
                store_name = form.cleaned_data['store_name']
                loc = form.cleaned_data['loc']
                if not StoreData.objects.filter(store_name=store_name).exists(): # if there in no store with same name already in database, then add store
                    s = StoreData(user=user,store_name=store_name,loc=loc)
                    s.save()
                    return HttpResponseRedirect('/showstore/')
                else:
                    messages.success(request,"Store Already Exists")
        else:
            form = Add_Store_Form() # display the form to add new store
        return render(request, 'books/addstore.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

# To show books related to a particular store
def show_books_view(request, id):
    if request.user.is_authenticated:
        book = BooksData.objects.filter(store=id) # fetches the data from book tabke based on store
        if not book.exists():
            messages.success(request, '')
        return render(request, 'books/showbooks.html', {'data': book, 'idd': id})
    else:
        return HttpResponseRedirect('/login/')

# To delete a store
def del_store_view(request, id):
    if request.user.is_authenticated:
        StoreData.objects.get(id=id).delete()
        return HttpResponseRedirect('/showstore/')
    else:
        return HttpResponseRedirect('/login/')

# To add books related to a particular store
def add_book_view(request, idd, id, title, img):
    if request.user.is_authenticated:
        s = StoreData.objects.get(id = idd)
        form = BooksData.objects.filter(bookid=id, store=s)
        if form:
            form[0].count += 1
            form[0].save()
        else:
            form = BooksData(store=s, bookid=id, bookname=title, img=img, count=1)
            form.save()
        return HttpResponseRedirect(f'/showbooks/{idd}')
    else:
        return HttpResponseRedirect('/login/')

# To search books using googleapi
def Search(request, idd):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = Search_Book_Form(request.POST)
            if fm.is_valid():
                googleapi = 'https://www.googleapis.com/books/v1/volumes?q='
                search = fm.cleaned_data['search']
                googleapi += search
                j = requests.get(googleapi)
                j = j.json()
                if j['totalItems'] == 0:
                    messages.success(request, 'Book not found')
                else:
                    l1, l2, l3 = [], [], []

                    for i in j['items']:
                        l1.append(i['id'])
                        l2.append(i['volumeInfo']['title'])
                        try:
                            l3.append(i['volumeInfo']['imageLinks']['thumbnail'])
                        except:
                            l3.append('#')

                    d = zip(l1, l2, l3)
                    return render(request, 'books/insert.html', {'d': d, 'idd': idd})
        else:
            fm = Search_Book_Form()
        return render(request, 'books/search.html', {'forms': fm})
    else:
        return HttpResponseRedirect('/login/')

# To do chnages in particular book info
def edit_book_view(request, id):
    if request.user.is_authenticated:
        book = BooksData.objects.get(id=id)
        if request.method == 'POST':
            form = Add_Books_Form(instance=book, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Changes Done Successfully')
        else:
            form = Add_Books_Form(instance=book)
        return render(request, 'books/edit.html', {'forms': form})
    else:
        return HttpResponseRedirect('/login/')

# To delete a book
def del_book_view(request, id):
    if request.user.is_authenticated:
        BooksData.objects.get(id=id).delete()
        return HttpResponseRedirect('/showstore/')
    else:
        return HttpResponseRedirect('/login/')
