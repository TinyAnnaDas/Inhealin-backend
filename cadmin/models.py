from django.db import models




# Create your models here.


class SubscriptionPlans(models.Model):
    type = models.CharField(max_length=20)
    sessions_available=models.IntegerField(null=True, blank=True)
    chat_access_no_of_weeks  = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    details1 = models.TextField(null=True, blank=True)
    details2 = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type




class Chat(models.Model):
    content = models.CharField(max_length=1000)
    owner = models.ForeignKey(
        'client.User',  
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
        )
    timestamp = models.DateTimeField(auto_now=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)

    

class Group(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=200)
    room_name = models.CharField(max_length=200)

    def __str__(self):
        return self.name




    






