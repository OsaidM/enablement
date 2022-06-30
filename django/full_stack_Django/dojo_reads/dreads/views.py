from .models import User, Book, Review, Author
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    if 'user' in request.session:    
        del request.session['user']
    return render (request, 'books_app/index.html')

def register(request):
    if request.method =='POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/')
        else:
            password=request.POST['password']
            pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash.decode())
            request.session['user']=request.POST['first_name']
            request.session['user_id']=new_user.id
            return redirect ('/books')
    return redirect ('/')

def login(request):
    print('*'*80)
    print("in the login method")
    if request.method =='POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user=User.objects.filter(email=request.POST['email'])
            logged_user=user[0]
            request.session['user'] = logged_user.first_name
            request.session['user_id']=logged_user.id
            return redirect ('/books')
    return redirect ('/')


def books(request):
    context = {
        'recent_reviews' : Review.objects.all().order_by('-created_at'),
        'other_books' : Book.objects.all(),
    }
    return render (request, 'books_app/books.html', context)

def add_book(request):
    context={
        'all_authors': Author.objects.all()
    }
    return render(request, 'books_app/add_book.html', context)

def books_create(request):
    if request.method =='POST':
        errors = User.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        else:
            this_user = User.objects.get(id= request.session['user_id'])
            if "author_select" in request.POST.keys():
                this_book=Book.objects.create(title=request.POST['title'],
                author=Author.objects.get(id=request.POST['author_select'])
                )
            else:
                this_book=Book.objects.create(title=request.POST['title'],
                author=Author.objects.create(author_name=request.POST['add_author'])
                )
            Review.objects.create(content = request.POST['content'], rating = request.POST['rating'], user = this_user, book=this_book)
            this_book.reviews.add(this_user)
            return redirect ('/books/'+str(this_book.id))

def books_id(request, book_id):
    this_book=Book.objects.get(id=book_id)
    this_book_reviews = Review.objects.filter(book=this_book)
    print(this_book_reviews)
    context = {
        'thisbook' : this_book,
        'this_book_reviews': this_book_reviews
    }
    return render (request, 'books_app/books_id.html', context)

def users_id(request, user_id):
    this_user=User.objects.get(id=user_id)
    total_reviews = Review.objects.filter(user=this_user)
    print(total_reviews)
    # print(dir(this_user))
    context = {
        'thisuser' : this_user,
        'userreviews':total_reviews
    }
    return render (request, 'books_app/users_id.html', context)

def books_id_update(request, book_id):
    if request.method =='POST': 
        updates=Book.objects.get(id=book_id)
        updates.title=request.POST['title']
        updates.description=request.POST['description']
        updates.save()
        return redirect ('/books/'+book_id)
    else:
        return redirect ('/books')


def book_destroy(request, book_id):
    print('*'*80)
    print("in the destroy method")
    deleted=Book.objects.get(id=book_id)
    deleted.delete()
    return redirect ('/books')

def review_destroy(request, review_id):
    print('*'*80)
    print("in the destroy method")
    deleted=Review.objects.get(id=review_id)
    deleted.delete()
    return redirect ('/books')


def books_id_edit(request, book_id):
    print('*'*80)
    print("in the edit method")
    thisbook=Book.objects.get(id=book_id)
    context = {
        'thisbook' : thisbook
    }
    return render (request, 'books_app/book_id_edit.html', context)
