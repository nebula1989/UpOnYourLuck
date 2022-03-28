from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from stickers.models import StickerShipment
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from stickers.forms import ShipStickerForm

from uponyourluck import settings


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


@login_required
def ship_sticker_view(request):
    if request.method == 'POST':
        qr_request_model = StickerShipment()
        form = ShipStickerForm(request.POST)
        if form.is_valid():
            form.save()
            email_subject = f'QR Sticker Request for {request.user}'
            email_message = qr_request_model.__str__()
            send_mail(email_subject, email_message, settings.CONTACT_EMAIL, settings.ADMIN_EMAILS)
            return render(request, 'success.html')
    form = ShipStickerForm()
    context = {'form': form}
    return render(request, 'ship_sticker.html', context)
