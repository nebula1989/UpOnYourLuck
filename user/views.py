from django.contrib.auth.models import User
from .models import Profile

from django.shortcuts import render, redirect, get_object_or_404
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


def profile(request, username=None):
    if username:
        current_user = get_object_or_404(User, username=username)
    else:
        messages.error(request, 'No User Found')
        return redirect('welcome_index')
    args1 = {
        'current_user': current_user,
    }
    return render(request, 'profile.html', args1)


@login_required()
def update_profile(request):
    logged_in_user = request.user
    profile_obj = Profile.objects.get(user=logged_in_user)
    # when a user submits a form
    if request.method == 'POST':
        profile_form = UpdateProfileForm(request.POST)
        if profile_form.is_valid():
            profile_obj.form.save()
            messages.success(request, "Profile Updated Successfully.")
    profile_form = UpdateProfileForm()
    return render(request, template_name='profile.html', context={"update_profile_form": profile_form})


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
