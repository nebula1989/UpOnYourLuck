from django.shortcuts import render


# Create your views here.
def sticker_index(request):
    args1 = {
        'current_user': request.user,
    }
    return render(request, 'sticker_index.html', args1)
