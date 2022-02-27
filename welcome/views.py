from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

from user.models import FollowersCount


# Create your views here.
def index(request):
    return render(request, 'welcome/welcome_base.html')


def show_all_users(request):
    user_model = get_user_model()
    current_user = request.user.username
    list_of_active_nonstaff_users = user_model.objects.all().filter(is_active=True, is_staff=False)
    num_list = [1, 2, 3, 4, 5, 6]

    context = {
        'current_user': current_user,
        'list_of_users': list_of_active_nonstaff_users,
        'num_list': num_list,
    }
    return render(request, 'welcome/show_all_users.html', context)

def followers_count(request):
    if request.method == 'POST':
        value = request.POST['value']
        following = request.POST['following']
        follower = request.POST['follower']
        print(following)

        if value == 'follow':
            followers_cnt = FollowersCount.objects.create(follower=follower, following=following)
            followers_cnt.save()
        else:
            followers_cnt = FollowersCount.objects.get(follower=follower, following=following)
            followers_cnt.delete()
            
        return redirect('/'+following)
