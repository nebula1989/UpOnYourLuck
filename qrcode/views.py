from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.

def index(request, username=None):
    if username:
        current_user = get_object_or_404(User, username=username)
    else:
        messages.error(request, 'No QR codes for this User')
        return redirect('welcome_index')
    args1 = {
        'current_user': current_user,
    }
    return render(request, 'qrcode/qrcode_base.html', args1)
