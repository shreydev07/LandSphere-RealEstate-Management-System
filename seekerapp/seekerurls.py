from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'seekerapp'

urlpatterns = [
    path('seekerhome/', views.seekerhome, name='seekerhome'),
    path('seeker/logout/', views.seeker_logout, name="seeker_logout"),
    path('properties/', views.available_properties, name='available_properties'),
    path('book/<int:property_id>/', views.book_property, name='book_property'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('seeker_profile/', views.seeker_profile, name='seeker_profile'),
    path('seeker_change_password/', views.seeker_change_password, name='seeker_change_password'),
    path('profile/edit/', views.edit_seeker_profile, name='edit_seeker_profile'),
    path('receipt/<int:booking_id>/', views.booking_receipt, name='booking_receipt'),
    path('seeker_complaint/', views.seeker_complaint, name='seeker_complaint'),



    
]
