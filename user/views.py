import os
from os.path import exists
from PIL import Image
from django.contrib.auth.models import User
from django.http import QueryDict
from django.shortcuts import render, redirect, get_object_or_404

from uponyourluck.settings import DOMAIN, MEDIA_ROOT, account_sid, auth_token, client, service
from .forms import ChangePassword, LoginForm, NewUserForm, UpdateProfileForm, UpdateTwoFactor, UpdateUserForm  # UpdateUserForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash, get_user_model

from django.contrib import messages
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
    user_model = get_user_model()
    list_of_active_nonstaff_users = user_model.objects.all().filter(is_active=True, is_staff=False)
    user_list = get_user_followers(list_of_active_nonstaff_users, request)
    
    list_of_followers_usernames = []
    for name in followers_list:
        list_of_followers_usernames.append(name.follower)

    newDict = dict()
    for key, value in user_list.items():
        if str(key) in list_of_followers_usernames:
            newDict[key] = value

    num_list = [1, 2, 3, 4, 5, 6]
    user_list = []
    for user in followers_list:
        user_list.append(get_object_or_404(User, username=user.follower))

    context = {
        'current_user': request.user,
        'list_of_users': user_list,
        'num_list': num_list,
        'title': "Your followers",
        'user_followers_dict': newDict,
    }
    return render(request, 'welcome/show_all_users.html', context)


@login_required()
def view_following(request):
    
    # following_list is list of people I follow in QuerySet Object
    following_list = FollowersCount.objects.filter(follower=request.user.username)

    user_model = get_user_model()
    num_list = [1, 2, 3, 4, 5, 6]
    following_list_usernames = []
    list_of_active_nonstaff_users = user_model.objects.all().filter(is_active=True, is_staff=False)
    user_list = get_user_followers(list_of_active_nonstaff_users, request)
    newDict = dict()
    for key, value in user_list.items():
        if value == 'unfollow':
            newDict[key] = value

    for user in following_list:
        following_list_usernames.append(get_object_or_404(User, username=user.following))

    num_list = [1, 2, 3, 4, 5, 6]
    # user_list is a list of people I follow
    user_list = []
    for user in following_list:
        user_list.append(get_object_or_404(User, username=user.following))

    context = {
        'current_user': request.user,
        'list_of_users': user_list,
        'num_list': num_list,
        'title': "People you are following",
        'user_followers_dict': newDict,
    }
    return render(request, 'welcome/show_all_users.html', context)

def get_user_following(user_list: QueryDict, request):
    user_dict= {}
    for user in user_list:
        following = request.user.username
        obj = FollowersCount.objects.filter(follower=user.username, following=following)
        if obj.exists():
            user_dict.update({user: 'unfollow'})
        else:
            user_dict.update({user: 'follow'})
    return user_dict

def get_user_followers(user_list: QueryDict, request):
    user_dict= {}
    for user in user_list:
        follower = request.user.username
        obj = FollowersCount.objects.filter(follower=follower, following=user.username)
        if obj.exists():
            user_dict.update({user: 'unfollow'})
        else:
            user_dict.update({user: 'follow'})
    return user_dict


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


@login_required()
def follow_count(request):
    
    if request.method == 'POST':
        # Get form values
        value = request.POST['value']
        following = request.POST['following']
        follower = request.POST['follower']
        
        following_list = FollowersCount.objects.filter(following=request.user.username)
        user_list = []
        for user in following_list:
            user_list.append(get_object_or_404(User, username=user.following))
        

        
        # If user is not following, create follower. Otherwise delete follower
        if value == 'follow':
            followers_cnt = FollowersCount.objects.create(follower=follower, following=following)
            followers_cnt.save()
        else:
            followers_cnt = FollowersCount.objects.get(follower=follower, following=following)

            followers_cnt.delete()

        return redirect('/' + following)


@login_required()
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

        # Delete a Profile's associated FollowersCount objects
        FollowersCount.objects.filter(follower=request.user.username).delete()
        FollowersCount.objects.filter(following=request.user.username).delete()

        # remove qr code img upon account deletion
        os.remove(str(MEDIA_ROOT) + f'/qr_code/{request.user.username}.jpg')
        # remove profile image but not the default placeholder profile img
        if profile.profile_img.path == 'profile_img/default.jpg':
            pass
        else:
            os.remove(profile.profile_img.path)

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

            return redirect('user_dashboard')
        else:
            messages.error(request, f"{user_form.errors}")
            return redirect('register')
    else:
        user_form = NewUserForm()
    return render(request=request, template_name="register.html",
                  context={"register_form": user_form, "user": request.user, "errors": user_form.errors})


""" 
    Function: login_request()
    Params: None
    Purpose: View to allow users to login to existing accounts, and requests 2FA as needed.
"""
def login_request(request):
    # On post
    if request.method == "POST":
        # Get login form
        form = LoginForm(request, data=request.POST)
        # If form is valid
        if form.is_valid():
            # Get cleaned data from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Check if user can be authenticated
            user = authenticate(username=username, password=password)
            # If user can be authenticated
            if user is not None:
                # If fingerprint is recognized
                if user.profile.visitor_id == request.POST['visitor_id']:
                    # Login user
                    login(request, user)
                    # Display success
                    messages.info(request, f"You are now logged in as {username}.")
                    # Redirect to homepage
                    return redirect("welcome_index")
                # If fingerprint not recognized
                else:
                    # If user has two factor authentication enabled
                    if user.profile.two_factor_enabled:
                        # Generate and send verifcation code
                        verification = service.verifications \
                            .create(to=user.profile.phone_number, channel='sms')
                        # Render login verifcation page
                        return render(request, template_name='login_verify.html', context={'user_id': user.id, 'user': user})
                    # If user not using 2FA
                    else:
                        # Log user in
                        login(request, user)
                        # Display success
                        messages.info(request, f"You are now logged in as {username}.")
                        # Redirect to homepage
                        return redirect("welcome_index")
            else:
                # If user cannot be authenticated, display error
                messages.error(request, "Invalid username or password.")
        else:
            # If form isnt valid alert user
            messages.error(request, "Invalid username or password.")
    # Generate login form
    form = LoginForm()
    # Render login page
    return render(request=request, template_name="login.html", context={"login_form": form})

""" 
    Function: login_verification()
    Params: None
    Purpose: Verifies users with 2FA enabled
"""
def login_verification(request):
    # On post
    if request.method == "POST":
        # Get user ID from post data
        user_id = request.POST['user_id']
        # Get user object from user ID
        user = Profile.objects.get(user_id=user_id)
        
        # Get verification code entered by user
        code = ''
        for i in range(1, 7):
            code += request.POST[f'digit{i}']

        # Check if code entered by user matches generated one
        verification_check = service \
            .verification_checks \
            .create(to=user.phone_number, code=code)

        # If code approved
        if verification_check.status == "approved":
            # Get user object from user ID
            user = User.objects.get(id=user.user_id)
            # Set users fingerprint and save
            user.profile.visitor_id = request.POST['visitor_id']
            user.profile.save()
            # Log user in
            login(request, user)

            # Display success and redirect to homepage
            messages.info(request, f"You are now logged in as {user.username}.")
            return redirect("welcome_index")
        # If code wasn't approved
        else:
            # Display error to user and return to login page
            messages.error(request, "The code you entered was incorrect.")
            return redirect("login")

""" 
    Function: toggle_two_factor()
    Params: None
    Purpose: Allows users to toggle two factor authentication.
"""
def toggle_two_factor(request):
    form = UpdateTwoFactor(request.POST, request.user.profile)

    if form.is_valid():
        profile = Profile.objects.get(user_id=request.user.id)
        form_data = form.save(commit=False)
        profile.two_factor_enabled = form_data.two_factor_enabled
        profile.phone_number = form_data.phone_number
        profile.save()
        messages.success(request, "You have updated your Two Factor Authentication Information!")
        return redirect('update_security')
    else:
        messages.error(request, form.errors)
        return redirect('update_security')


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("welcome_index")

""" 
    Function: generate_qr_code()
    Params: Username - Username of user creating QR Code
    Purpose: Generates a QR code for a user. Includes UpOnYourLuck logo.
"""
def generate_qr_code(request, username=None):
    # Domain of the site
    domain = DOMAIN

    # Statement to check if our username value was passed
    # Sets profile_url accordingly
    if username == None:
        profile_url = request.user.profile.profile_url
    else:
        profile_url = username.profile.profile_url

    # Creates profile URL link to embed into QR Code
    user_profile_full_url = domain + '/' + profile_url + '/?source=qr'

    # Open and resize the UpOnYourLuck Logo
    logo = Image.open(str(MEDIA_ROOT) + '/home_page/UpOnYourLuck_Logo_transparent.jpg')
    logo.thumbnail((150,150), Image.ANTIALIAS)

    # Create a new QR code with maximum error correction
    qr_img = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

    # Add the profile url to the QR code, and generate image.
    qr_img.add_data(user_profile_full_url)
    qr_img.make()

    # Convert to RGB so Logo has color
    qr_code = qr_img.make_image().convert('RGB')
    
    # Set the logo position in the center of the QR Code
    logo_pos = ((qr_code.size[0] - logo.size[0]) // 2, (qr_code.size[1] - logo.size[1]) // 2)

    # Place the logo in the QR Code
    qr_code.paste(logo, logo_pos)

    # Save file and update database with path to qr code
    if username == None:
        qr_code.save(str(MEDIA_ROOT) + '/qr_code/' + request.user.username + '.jpg')
        request.user.profile.qr_code_img = request.user.username + '.jpg'
    else:
        qr_code.save(str(MEDIA_ROOT) + '/qr_code/' + username.username + '.jpg')
        username.profile.qr_code_img = username.username + '.jpg'

""" 
    Function: regenerate_qr_code()
    Params: None
    Purpose: Regenerates a QR code for a user. Includes UpOnYourLuck logo.
"""
def regenerate_qr_code(request):
    # Get expected path of the QR Code
    qr_path = str(MEDIA_ROOT) + '/qr_code/' + request.user.username + '.jpg'

    # If QR Code already exists, remove it and regenerate it.
    # Otherwise generate a new code
    if exists(qr_path):
        os.remove(qr_path)
        generate_qr_code(request=request)   
    else:
        generate_qr_code(request=request)

    # Display success and return to sticker page
    messages.success(request, "You have created a new QR Code!")
    return redirect('sticker_index')

""" 
    Function: regenerate_user_qr_code()
    Params: Username - Username of user creating QR Code
    Purpose: Admin function to regenerate a users QR Code.
"""
def regenerate_user_qr_code(request, username=None):
    # Get username object from user sticker page
    username_obj = get_object_or_404(User, username=username)

    # Get expected path of the QR Code
    qr_path = str(MEDIA_ROOT) + '/qr_code/' + username_obj.username + '.jpg'

    # If QR Code already exists, remove it and regenerate it.
    # Otherwise generate a new code
    if exists(qr_path):
        os.remove(qr_path)
        generate_qr_code(request=request, username=username_obj)
    else:
        generate_qr_code(request=request, username=username_obj)

    # Display success and return to users sticker page
    messages.success(request, "You have created a new QR Code for this user!")
    return redirect('sticker_index_for_visitor', username_obj)