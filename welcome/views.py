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
        # print(request.user) # this is user requesting to follow/unfollow
        current_user = request.POST['following']
        
        other_profile = request.POST['follower']
        
        # following_list is who I'm following essentially
        following_query_set = FollowersCount.objects.filter(follower=current_user)
        
        
        following_list = []
        for user in following_query_set.values():
            following_list.append(user['following'])
        # print(following_list)            
        # print(other_profile)
        # print(following_list)
        
        
        # This for loop below might not be necessary. 
        # user_following_set = {}
        # for user in following_list:
        #     user_following_set.add(get_object_or_404(User, username=user))

        # print(user_following_set)            

        # If user is not following, create FollowerCount Obj. Otherwise delete FollowerCount Obj
        if value == 'follow' and other_profile not in following_list:
            followers_cnt = FollowersCount.objects.create(following=other_profile, follower=current_user)
            followers_cnt.save()
            messages.success(request, f'Now following {other_profile}')
        else:
            followers_cnt = FollowersCount.objects.get(following=other_profile, follower=current_user)
            followers_cnt.delete()
            messages.warning(request, f'Unfollowed {other_profile}')

        return redirect('show-all-users')
