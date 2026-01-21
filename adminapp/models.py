from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class AdminLogin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    


class Owner(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact_no = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    address = models.TextField()
    gov_id_proof = models.ImageField(upload_to='gov_id_proofs/')
    land_certificate = models.ImageField(upload_to='land_certificates/')
    profile_photo = models.ImageField(upload_to='profile_photos/')
    registration_status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.registration_status})"
    



class Seeker(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact_no = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=100)  
    id_proof = models.ImageField(upload_to='id_proofs/')
    photo = models.ImageField(upload_to='photos/')
    registration_status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )
    booking_status = models.CharField(
        max_length=20,
        choices=[
            ('No Booking', 'No Booking'),
            ('Pending', 'Pending'),  # New Status for Pending Requests
            ('Booked', 'Booked'),
            ('Already Booked', 'Already Booked')
        ],
        default='No Booking'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.registration_status}, {self.booking_status})"


class Complaint(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField() 
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} by {self.name}"
    