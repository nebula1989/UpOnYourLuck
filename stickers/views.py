from django.shortcuts import render


# Create your views here.
def sticker_index(request):
    return render(request, 'sticker_index.html')
