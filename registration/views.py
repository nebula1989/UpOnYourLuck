from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, 25, 'Person Created!')
        else:
            messages.add_message(request, 40, 'Error in Registration.  Try again.')
        return redirect('/')

    else:
        form = RegisterForm()

        return render(request, "registration/sign_up.html", {"form": form})
