from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=50)
    open_time = models.TimeField()
    close_time = models.TimeField()
    capacity = models.SmallIntegerField()

    def __str__(self):
        return self.name

# class User(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField()

class Booking(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField()
    status = models.BooleanField(default=False)
    status_remark = models.TextField()
    book_by = models.ForeignKey(User, on_delete=models.CASCADE)
    book_date = models.DateField()
    def __str__(self):
        return self.room_id,self.book_by
