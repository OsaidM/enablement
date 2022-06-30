from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^books/(?P<book_id>\d+)$', views.books_id),
    url(r'^users/(?P<user_id>\d+)$', views.users_id),
    url(r'^books/add$', views.add_book),
    url(r'^books/create$', views.books_create),
    url(r'^books/(?P<book_id>\d+)/update$', views.books_id_update),
    url(r'^books/(?P<book_id>\d+)/destroy$', views.book_destroy),
    url(r'^reviews/(?P<review_id>\d+)/destroy$', views.review_destroy),
    url(r'^books/(?P<book_id>\d+)/edit$', views.books_id_edit),
]
