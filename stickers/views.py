from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
def sticker_index(request):
    args1 = {
        'current_user': request.user,
    }
    return render(request, 'sticker_index.html', args1)


def sticker_index_for_visitor(request, username=None):
    if username:
        username_obj = get_object_or_404(User, username=username)
    else:
        messages.error(request, 'No User Found')
        return redirect('welcome_index')

    if username_obj.username == request.user.username:
        return redirect('visitor_to_profile')
    context = {
        'username': username_obj.username,
        'qr_code_img': username_obj.profile.qr_code_img,
    }

    return render(request, 'sticker_index_for_visitor.html', context)
