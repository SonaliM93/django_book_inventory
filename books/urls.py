from django.urls import path
from .views import home_view, login_view, logout_view, signup_view, show_books_view, show_store_view, add_store_view, del_store_view, add_book_view, Search, edit_book_view, del_book_view

urlpatterns = [
    path('', home_view),
    path('login/', login_view),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('showstore/', show_store_view, name='showstore'),
    path('addstore/', add_store_view, name='addstore'),
    path('showstore/del_store/<int:id>/',del_store_view),
    path('showbooks/<int:id>', show_books_view, name='showbooks'),
    path('addbook/<int:idd>/<str:id>/<str:title>/<path:img>', add_book_view, name='addbook'),
    path('search/<int:idd>', Search, name='search'),
    path('showbooks/edit_book/<int:id>/',edit_book_view),
    path('showbooks/del_book/<int:id>/',del_book_view),
]
