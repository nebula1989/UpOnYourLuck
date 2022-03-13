from multiprocessing import context
import os
from textwrap import fill
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ChangePassword, LoginForm, NewUserForm, UpdateProfileForm, UpdateUserForm  # UpdateUserForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import FollowersCount, Profile

import qrcode


@login_required
def dashboard(request):
    user_following = len(FollowersCount.objects.filter(follower=request.user.username))
    user_followers = len(FollowersCount.objects.filter(following=request.user.username))
    qr_scans = Profile.objects.get(user=request.user).qr_scan_count

    context = {
        'current_user': request.user,
        'user_followers': user_followers,
        'user_following': user_following,
        'qr_scans': qr_scans,
    }

    return render(request, 'dashboard.html', context)


@login_required()
def view_followers(request):
    followers_list = FollowersCount.objects.filter(following=request.user.username)
    num_list = [1, 2, 3, 4, 5, 6]
    user_list = []
    for user in followers_list:
        user_list.append(get_object_or_404(User, username=user.follower))

    context = {
        'current_user': request.user,
        'list_of_users': user_list,
        'num_list': num_list,
        'title': "Your followers"
    }
    return render(request, 'welcome/show_all_users.html', context)


@login_required()
def view_following(request):
    following_list = FollowersCount.objects.filter(follower=request.user.username)
    print(following_list)
    num_list = [1, 2, 3, 4, 5, 6]
    user_list = []
    for user in following_list:
        user_list.append(get_object_or_404(User, username=user.following))

    context = {
        'current_user': request.user,
        'list_of_users': user_list,
        'num_list': num_list,
        'title': "People you are following"
    }
    return render(request, 'welcome/show_all_users.html', context)


# for visitors going to a user's profile page
def visitor_to_profile(request, username=None):
    if username:
        username_obj = get_object_or_404(User, username=username)
    else:
        messages.error(request, 'No User Found')
        return redirect('welcome_index')

    # Check if user came from QR scan
    if "?source=qr" in request.build_absolute_uri():
        profile = Profile.objects.get(user=username_obj)
        profile.qr_scan_count += 1
        print(profile.qr_scan_count)
        profile.save()

    # Get number of followers and following
    current_user = username_obj.username
    logged_in_user = request.user.username
    user_followers = len(FollowersCount.objects.filter(following=current_user))
    user_following = len(FollowersCount.objects.filter(follower=current_user))
    follower_list = FollowersCount.objects.filter(following=current_user)

    # Loop through follower_list to check if requester is already following
    user_list = []
    for x in follower_list:
        follower_list = x.follower
        user_list.append(follower_list)
    if logged_in_user in user_list:
        follow_btn = 'unfollow'
    else:
        follow_btn = 'follow'

    if username_obj.username == request.user.username:
        return redirect('profile')
    context = {
        'current_user': current_user,
        'user_followers': user_followers,
        'user_following': user_following,
        'follow_btn': follow_btn,
        'profile_username': username_obj.username,
        'payment_link_url': username_obj.profile.payment_link_url,
        'life_story': username_obj.profile.life_story,
        'profile_img': username_obj.profile.profile_img,
        'city': username_obj.profile.city,
        'state': username_obj.profile.state,
    }

    return render(request, 'profile_for_visitor.html', context)


def followers_count(request):
    if request.method == 'POST':
        # Get form values
        value = request.POST['value']
        following = request.POST['following']
        follower = request.POST['follower']

        # If user is not following, create follower. Otherwise delete follower
        if value == 'follow':
            followers_cnt = FollowersCount.objects.create(follower=follower, following=following)
            followers_cnt.save()
        else:
            followers_cnt = FollowersCount.objects.get(follower=follower, following=following)
            followers_cnt.delete()

        return redirect('/' + following)


# For logged in users to see their own profile page
def profile(request):
    logged_in_user = request.user.username
    user_followers = len(FollowersCount.objects.filter(following=logged_in_user))
    user_following = len(FollowersCount.objects.filter(follower=logged_in_user))
    follower_list = FollowersCount.objects.filter(following=logged_in_user)

    context = {
        'current_user': request.user,
        'user_followers': user_followers,
        'user_following': user_following,
        'payment_link_url': request.user.profile.payment_link_url,
        'life_story': request.user.profile.life_story,
        'profile_img': request.user.profile.profile_img,
        'city': request.user.profile.city,
        'state': request.user.profile.state,
    }
    return render(request, 'profile.html', context)


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

    context = {
        'p_form': p_form,
        'u_form': u_form,
        'current_user': request.user,
        'profile_img': request.user.profile.profile_img,
    }
    return render(request, 'update_profile.html', context)


@login_required()
def update_security(request):
    if request.method == 'POST':
        # Get correct form
        form = ChangePassword(request.user, request.POST)

        # Check if form is valid, save and update if valid, display error if invalid
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, form.errors)
    else:
        form = ChangePassword(request.user)
    return render(request, 'security_update.html', {'p_form': form, 'current_user': request.user})


@login_required()
def delete_profile(request):
    if request.method == 'POST':
        # Get Profile object of user
        profile = Profile.objects.get(user=request.user)

        # Remove profile image and qr code
        os.remove(profile.profile_img.path)
        os.remove(f'media/qr_code/{request.user.username}.jpg')

        # Delete user data
        profile.user.delete()

        # Display success to user and return to homepage
        messages.success(request, 'Your account was successfully deleted!')
        return redirect('welcome_index')


def register_request(request):
    args = {}
    if request.method == "POST":
        user_form = NewUserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            generate_qr_code(request)
            messages.success(request, "Registration successful.")
            return redirect("user_dashboard")

        # messages.error(request, f"{user_form.errors}")
    else:
        user_form = NewUserForm()
    return render(request=request, template_name="register.html",
                  context={"register_form": user_form, "user": request.user, "errors": user_form.errors})


def login_request(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
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
    form = LoginForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("welcome_index")


def generate_qr_code(request):
    DOMAIN = 'bwalters89.pythonanywhere.com/'
    profile_url = request.user.profile.profile_url
    user_profile_full_url = DOMAIN + profile_url + '?source=qr'
    qr_img = qrcode.make(user_profile_full_url)
    qr_img.save('/home/bwalters89/UpOnYourLuck/media/qr_code/' + request.user.username + '.jpg')
    request.user.profile.qr_code_img = request.user.username + '.jpg'
