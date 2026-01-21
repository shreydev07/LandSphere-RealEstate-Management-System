from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('about/',views.about, name='about'),
    path('services/',views.services, name='services'),
    path('contact/',views.contact, name='contact'),
    path('properties/',views.properties, name='properties'),
    path('complaints/',views.complaints, name='complaints'),
    path('login/',views.login, name='login'),
    path('register/',views.register, name='register'),
    path('register/seeker/', views.seeker_registration, name='seeker_registration'),
    path('register/owner/', views.owner_registration, name='owner_registration'), 
    path('complaints/', views.submit_complaint, name='submit_complaint'), 
    path('chatbot_send/', views.chatbot_send, name='chatbot_send'),
]