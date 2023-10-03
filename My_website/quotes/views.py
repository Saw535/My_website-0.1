from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth import views as auth_views
from .models import Author, Quote
from django.contrib.auth import authenticate
from .forms import PasswordResetForm

def home(request):
    authors = Author.objects.all()
    quotes = Quote.objects.all()
    return render(request, 'home.html', {'authors': authors, 'quotes': quotes})

def author_detail(request, author_id):
    author = Author.objects.get(pk=author_id)
    quotes = Quote.objects.filter(author=author)
    return render(request, 'author_detail.html', {'author': author, 'quotes': quotes})

@login_required
def add_author(request):
    if request.method == 'POST':
        name = request.POST['name']
        author = Author.objects.create(name=name)
        return redirect('home')
    return render(request, 'add_author.html')

@login_required
def add_quote(request):
    if request.method == 'POST':
        author_id = request.POST['author']
        text = request.POST['text']
        author = Author.objects.get(pk=author_id)
        quote = Quote.objects.create(author=author, text=text)
        return redirect('home')
    authors = Author.objects.all()
    return render(request, 'add_quote.html', {'authors': authors})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def profile(request):
    return render(request, 'profile.html')

class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            user = request.user

            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                return redirect('home')
            else:
                form.add_error('current_password', 'Incorrect current password.')
    else:
        form = PasswordResetForm()

    return render(request, 'change_password.html', {'form': form})