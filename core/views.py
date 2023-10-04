# core/views.py

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, LeagueCreationForm
from .models import League


def home(request):
    return render(request, 'home.html')


@login_required
def account(request):
    return render(request, 'account.html', {'user': request.user})


@login_required
def leagues(request):
    user = request.user
    user_leagues = user.membership_set.all().select_related('league')
    other_leagues = League.objects.exclude(members=user)
    return render(request, 'leagues.html', {'user_leagues': user_leagues, 'other_leagues': other_leagues})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('account')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('leagues')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def create_league(request):
    if request.method == 'POST':
        form = LeagueCreationForm(request.POST)
        if form.is_valid():
            league = form.save(commit=False)
            league.creator = request.user
            league.save()
            league.members.add(request.user)
            return redirect('leagues')
    else:
        form = LeagueCreationForm()
    return render(request, 'create_league.html', {'form': form})