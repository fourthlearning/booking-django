
from django.contrib import admin
from room.models import Room, Booking
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Room)


admin.site.register(Booking)

admin.site.register(Permission)