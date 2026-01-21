from django.db import models
from ownerapp.models import Property 
# Create your models here.

class BookingRequest(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='booking_requests')  
    seeker_name = models.CharField(max_length=100)  
    seeker_email = models.EmailField()  
    seeker_contact = models.CharField(max_length=15)  
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Accepted', 'Accepted'),
            ('Rejected', 'Rejected'),
            ('Already Booked', 'Already Booked')  # New status added
        ],
        default='Pending'
    )  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Booking by {self.seeker_name} for {self.property.title} ({self.status})"
    

class Seeker_Complaint(models.Model):
    seeker_name = models.CharField(max_length=100)
    seeker_email = models.EmailField()
    complaint_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint by {self.seeker_name} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"