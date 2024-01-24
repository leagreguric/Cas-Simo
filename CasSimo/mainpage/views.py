from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import User, BetHistory
from .forms import CreateUserForm
from decimal import Decimal

# Create your views here.
def home(request):
    context = {}
    return render(request, 'mainpage/index.html', context)


def register_page(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            User.objects.create(
                user=user,
                username=user.username,
            )
            messages.success(request, f'User "{username.title()}" created')
            return redirect('login')
        else:
            messages.error(request, 'Something went wrong, please try again..')

    context = {
        'form': form,
    }

    return render(request, 'mainpage/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('mainpage_index')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,
                                username=username,
                                password=password,
                                )
            if user is not None:
                login(request, user)
                return redirect('mainpage_index')
            else:
                messages.error(request, 'Username of password is incorrect')

    context = {}

    return render(request, 'mainpage/login.html', context)


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    user = User.objects.get(user=request.user)

    labels = ['win', 'lose', 'draw']
    data = [user.win, user.lose, user.draw]

    context = {
        'labels': labels,
        'data': data
    }

    return render(request, 'mainpage/bet_history.html', context)


@login_required(login_url='login')
def add_funds(request):
    return render(request, 'mainpage/add_funds.html')



@login_required(login_url='login')
def deposit(request, amount):
    user = get_object_or_404(User, user=request.user)
    main_account = get_object_or_404(User, username='admin')
    user.money += Decimal(amount)
    main_account.money -= Decimal(amount)
    user.save()
    main_account.save()
    return render(request, 'mainpage/add_funds.html')


@login_required(login_url='login')
def bet_history(request):
    user_profile = User.objects.get(user=request.user)
    all_bet_history = BetHistory.objects.filter(user=user_profile).order_by('-timestamp')

    context = {
        'all_bet_history': all_bet_history,
    }

    return render(request, 'mainpage/bet_history.html', context)

   