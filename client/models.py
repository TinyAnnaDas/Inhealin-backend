from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from cadmin.models import SubscriptionPlans

class UserAccountManager(BaseUserManager):

    def create_user(self, name, email, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        email = email.lower()
        
        user = self.model(
            name = name,
            email= email,
            phone = phone,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, name, email, phone, password=None):

        user = self.create_user(
            name,
            email,
            phone,
            password=password,
            
        )
        # user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
            
        user.save(using=self._db)
        return user






class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    phone = PhoneNumberField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(upload_to="images", default="avatar.svg")
    objects = UserAccountManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    # therapy_session = models.ForeignKey('TherapySessions', on_delete=models.SET_NULL, null=True, blank=True)
 


    class Types(models.TextChoices):
        CLIENT = "CLIENT", "Client"
        THERAPIST = "THERAPIST", "Therapist"


    status = models.CharField(max_length=255, default="pending")

    type = models.CharField(_('Type'), max_length=255, choices=Types.choices)
    


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone"]

    def __str__(self):
        return self.name





class ClientManager(UserAccountManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CLIENT)

class Client(User):
    objects = ClientManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.CLIENT
        return super().save(*args, **kwargs)

class ClientAdditionalDetails(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    subscription = models.ForeignKey(SubscriptionPlans, on_delete=models.SET_NULL, null=True, blank=True)
    sessions_available=models.IntegerField(null=True, blank=True)




class Subscriptions(models.Model):
    subscription_plan = models.ForeignKey(SubscriptionPlans, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.subscription_plan


        

class MoodJournal(models.Model):
    journal = models.TextField(null=True, blank=True)
    client = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        limit_choices_to={'type': User.Types.CLIENT})

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   


class TherapySessions(models.Model):
   

    client = models.ForeignKey(
        'client.Client',
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='therapy_sessions_as_client'
    )

    therapist = models.ForeignKey(
        'therapist.Therapist',
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='therapy_sessions_as_therapist'
    )

    scheduled_time = models.DateTimeField(null=True, blank=True)
    cancelled_by_therapist = models.BooleanField(default=False)
    cancelled_by_client = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



