from django.db import models
from adminapp.models import *

# Create your models here.
class Property(models.Model):
    property_id = models.AutoField(primary_key=True)  
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='properties')  # Property Owner
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=255)
    images = models.ImageField(upload_to='property_images/')  
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),  
            ('Approved', 'Approved'),  
            ('Inlisted', 'Inlisted'),
            ('Rejected', 'Rejected'),
            ('Sold', 'Sold'),  
             
        ],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"
    


class Owner_Complaint(models.Model):
    owner_name = models.CharField(max_length=100)
    owner_email = models.EmailField()
    complaint_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint by {self.owner_name} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"