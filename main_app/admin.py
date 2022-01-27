from django.contrib import admin

# import your models here
from .models import Guitar, Restring, Accessory, Photo

# register your models here.
admin.site.register(Guitar)
admin.site.register(Restring)
admin.site.register(Accessory)
admin.site.register(Photo)