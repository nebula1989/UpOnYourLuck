from pyexpat.errors import messages
from django.http import QueryDict
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from user.models import FollowersCount
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'welcome/welcome_base.html')


def show_all_users(request):
    user_model = get_user_model()
    current_user = request.user.username
    list_of_active_nonstaff_users = user_model.objects.all().filter(is_active=True, is_staff=False)
    num_list = [1, 2, 3, 4, 5, 6]

    user_list = get_user_followers(list_of_active_nonstaff_users, request).items()

    context = {
        'current_user': current_user,
        'list_of_users': list_of_active_nonstaff_users,
        'num_list': num_list,
        'title': "People in your area",
        'user_list': user_list,
    }
    return render(request, 'welcome/show_all_users.html', context)

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


@login_required
def followers_count(request):
    if request.method == 'POST':
        
        # Get form values
        value = request.POST['value']
        following = request.POST['following']
        follower = request.POST['follower']

        # Debugging code
        following_list = FollowersCount.objects.filter(following=request.user.username)
        print(following_list[0].follower)

        # prints out each of profile's follower's after they press a follow button
        for ele in following_list:
            print(ele.follower)

        user_list = []
        for user in following_list:
            user_list.append(get_object_or_404(User, username=user.following))

        # If user is not following, create follower. Otherwise delete follower
        if value == 'follow':
            followers_cnt = FollowersCount.objects.create(following=follower, follower=following)
            followers_cnt.save()
            messages.success(request, f'Now following {follower}')
        else:
            followers_cnt = FollowersCount.objects.get(following=follower, follower=following)
            followers_cnt.delete()
            messages.warning(request, f'Unfollowed {follower}')

        return redirect('show-all-users')
