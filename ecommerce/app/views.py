from django.shortcuts import render, redirect
from .forms import RegistrationForm


def home(request):
    return render(request, 'app/home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:home')
    else:
        form = RegistrationForm()
    return render(request, 'app/register.html', {'form': form})


def about_view(request):
    return render(request, 'app/about.html')

