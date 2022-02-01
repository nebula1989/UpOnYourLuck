from django.contrib.auth.models import User
from .models import Profile

from django.shortcuts import render, redirect
from .forms import NewUserForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    """if username:
        current_user = get_object_or_404(User, username=username)

    else:
        current_user = request.user"""

    args1 = {
        'current_user': request.user,
    }
    return render(request, 'dashboard.html', args1)


def profile(request):
    args1 = {
        'current_user': request.user,
    }
    return render(request, 'profile.html', args1)


@login_required()
def update_profile(request):
    if request.method == 'POST':
        p_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UpdateUserForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your Profile has been updated!')
            return redirect('profile')
    else:
        p_form = UpdateProfileForm(instance=request.user)
        u_form = UpdateUserForm(instance=request.user.profile)

    context = {'p_form': p_form, 'u_form': u_form}
    return render(request, 'update_profile.html', context)


def register_request(request):
    if request.method == "POST":
        user_form = NewUserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("welcome_index")

        messages.error(request, "Unsuccessful registration. Invalid information.")
    user_form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": user_form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("user_dashboard")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("welcome_index")
