from django.contrib import admin
from .models import Stickers
from .forms import SendStickerForm


# Register your models here
class StickerAdmin(admin.ModelAdmin):
    form = SendStickerForm


admin.site.register(Stickers, StickerAdmin)
