from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.conf import settings


GENDER_CHOICES = [
    ("male", "Male"),
    ("female", "Female"),
    ("non-binary", "Non-Binary"),
    ("prefer-not-to-say", "Prefer not to say"),
]

class NewUser(AbstractUser):
    # Personal info
    username= models.CharField( max_length=150, unique=True, null=True, blank=True,)
    user_type = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('user', 'User')], default='User')
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150)
    gotra = models.CharField(max_length=150, blank=True)
    DOB = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    email = models.EmailField(unique=True, default='example@mail.com', blank=True, null=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)  # Unique phone number
    is_phone_verified = models.BooleanField(default=False, null=True)  # ✅ New field
    otp = models.CharField(max_length=6, blank=True, null=True)  # ✅ Store OTP temporarily
    otp_created_at = models.DateTimeField(null=True, blank=True)  # ✅ OTP expiry tracking
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)  # Optional
    blood_group = models.CharField(max_length=10, blank=True)
    # Religious
    pant = models.CharField(max_length=20, blank=True)
    pantoption = models.CharField(max_length=20, blank=True, null=True)

    # Location
    marudar_place = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    residential_address = models.TextField(blank=True)

    # Business
    business_name = models.CharField(max_length=150, blank=True)
    business_type = models.CharField(max_length=150, blank=True)
    industry = models.CharField(max_length=150, blank=True)
    website = models.URLField(blank=True)
    business_address = models.TextField(blank=True)

    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete flag
    deleted_at = models.DateTimeField(null=True, blank=True)
    added_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='added_users')

    def __str__(self):
        return self.email




class FamilyMember(models.Model):
    main_user = models.ForeignKey('NewUser', on_delete=models.CASCADE, related_name='family_members')
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices= GENDER_CHOICES, default='male')
    phone = models.CharField(max_length=15, unique=True)  # Unique phone number for each family member
    whatsapp = models.CharField(max_length=15, blank=True, null=True)  # Optional WhatsApp number
    blood_group = models.CharField(max_length=10, blank=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    password = models.CharField(max_length=128)
    head_of_family = models.ForeignKey('NewUser', on_delete=models.CASCADE, related_name='head_of_family', null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return f"{self.name} ({self.relationship})"
    
class Event(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)  # Soft delete
    

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.title
    
class Invite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invites_sent')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_invites')
    members = models.ManyToManyField(NewUser, related_name='invited_events')
    invited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invite by {self.user} for {self.event}"
    



class AddressChangeRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    field_name = models.CharField(max_length=50, choices=[
        ('residential_address', 'Residential Address'),
        ('business_address', 'Business Address')
    ], default='residential_address')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    old_address = models.TextField()
    new_address = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"

class Entrepreneur(models.Model):
    name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=200, blank=True)
    designation = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='entrepreneurs/', null=True, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    added_by = models.ForeignKey(NewUser, on_delete=models.SET_NULL, null=True)  # assuming you use NewUser model
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete flag
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def __str__(self):
        return self.name



class CommitteeMember(models.Model):
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='committee_members/', null=True, blank=True)
    description = models.TextField(blank=True)
    added_by = models.ForeignKey(NewUser, on_delete=models.SET_NULL, null=True)  # assuming you use NewUser model
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Announcement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    image = models.ImageField(upload_to='announcements/', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class EventReadStatus(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    seen_at = models.DateTimeField(null=True, blank=True)

# models.py

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:20]}"
