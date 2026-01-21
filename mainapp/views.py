from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache
from adminapp.models import *
from ownerapp.models import *
from seekerapp.models import *
import random
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from openai import OpenAI

# Public views
@never_cache
def index(req):
    return render(req, 'index.html')

@never_cache
def about(req):
    return render(req, 'about.html')

@never_cache
def services(req):
    return render(req, 'services.html')

@never_cache
def contact(req):
    return render(req, 'contact.html')

@never_cache
def complaints(req):
    if req.method == 'POST':
        name = req.POST.get('name')
        email = req.POST.get('email')
        subject = req.POST.get('subject')
        message = req.POST.get('message')

        if name and email and subject and message:
            try:
                Complaint.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message
                )
                messages.success(req, 'Your complaint has been submitted successfully!')
                return redirect('complaints')
            except Exception as e:
                messages.error(req, 'An error occurred while submitting your complaint. Please try again.')
        else:
            messages.error(req, 'All fields are required.')
    
    return render(req, 'complaints.html')

@never_cache
def login(request):
    if request.method == 'POST':
        user_type = request.POST.get('usertype')
        username = request.POST.get('email')
        password = request.POST.get('password')

        if user_type == 'admin':
            try:
                admin = AdminLogin.objects.get(username=username, password=password)
                request.session['adminid'] = admin.id
                messages.success(request, 'Admin login successful!')
                return redirect('adminapp:adminhome')
            except AdminLogin.DoesNotExist:
                messages.error(request, 'Invalid Admin credentials')

        elif user_type == 'seeker':
            try:
                seeker = Seeker.objects.get(email=username, password=password, registration_status='Approved')
                request.session['seekerid'] = seeker.id
                messages.success(request, 'Seeker login successful!')
                return redirect('seekerapp:seekerhome')
            except Seeker.DoesNotExist:
                messages.error(request, 'Invalid Seeker credentials')

        elif user_type == 'owner':
            try:
                owner = Owner.objects.get(email=username, password=password, registration_status='Approved')
                request.session['ownerid'] = owner.id
                messages.success(request, 'Owner login successful!')
                return redirect('ownerapp:ownerhome')
            except Owner.DoesNotExist:
                messages.error(request, 'Invalid Owner credentials')

        else:
            messages.error(request, 'Invalid user type selected.')

    return render(request, 'login.html')

@never_cache
def register(request):
    return render(request, 'register.html')

@never_cache
def owner_registration(request):
    if request.method == 'POST':
        try:
            gov_id_proof = request.FILES.get('gov_id_proof')
            land_certificate = request.FILES.get('land_certificate')
            profile_photo = request.FILES.get('profile_photo')

            if not gov_id_proof or not land_certificate or not profile_photo:
                messages.error(request, "All files are required!")
                return redirect('register')

            name = request.POST.get('name')
            email = request.POST.get('email')

            Owner.objects.create(
                name=name,
                email=email,
                contact_no=request.POST.get('contact_no'),
                password=request.POST.get('password'),
                address=request.POST.get('address'),
                gov_id_proof=gov_id_proof,
                land_certificate=land_certificate,
                profile_photo=profile_photo,
                registration_status='Pending'
            )

            send_mail(
                subject="Landsphere: Registration Successful",
                message=f"Dear {name},\n\nThank you for registering on Landsphere. Your account is under review. You will be notified once approved.\n\nBest regards,\nLandsphere Team",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, "Your registration is successful! Please wait for admin approval. You will receive an email confirmation shortly.")
            return redirect('register')
        except Exception as e:
            messages.error(request, f"Error in registration: {str(e)}")
            return redirect('register')
    return render(request, 'register.html')

@never_cache
def seeker_registration(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            contact_no = request.POST.get('contact_no')
            password = request.POST.get('password')
            id_proof = request.FILES.get('id_proof')
            photo = request.FILES.get('photo')

            if not id_proof or not photo:
                messages.error(request, "ID proof and photo are required!")
                return redirect('register')

            Seeker.objects.create(
                name=name,
                email=email,
                contact_no=contact_no,
                password=password,
                id_proof=id_proof,
                photo=photo,
                registration_status='Pending',
                booking_status='No Booking'
            )

            send_mail(
                subject="Landsphere: Registration Successful",
                message=f"Dear {name},\n\nThank you for registering on Landsphere. Your account is under review. You will be notified once approved.\n\nBest regards,\nLandsphere Team",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, "Your registration is successful! Please wait for admin approval. You will receive an email confirmation shortly.")
            return redirect('register')

        except Exception as e:
            messages.error(request, f"Error in registration: {str(e)}")
            return redirect('register')

    return render(request, 'register.html')

def properties(request):
    properties = Property.objects.filter(status='Approved')
    return render(request, 'properties.html', {'properties': properties})

def submit_complaint(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            try:
                Complaint.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message
                )
                messages.success(request, 'Your complaint has been submitted successfully!')
                return redirect('submit_complaint')
            except Exception as e:
                messages.error(request, 'An error occurred while submitting your complaint. Please try again.')
        else:
            messages.error(request, 'All fields are required.')
    
    return render(request, 'complaints.html')

@csrf_exempt
def chatbot_send(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_msg = data.get("message", "").strip().lower()

        # Simple FAQ logic (extend as needed)
        faq_data = {
            "Hey": "Hello! How can I assist you today?",
            "hi": "Hello! How can I assist you today?",
            "hello": "Hello! How can I assist you today?",

            "how to register": "To register, click on the Register button and fill out the form.",
            "how to contact support": "You can reach out to support via the Contact Us page or email.",
            "what is landsphere": "Landsphere is a platform to buy, or sell properties easily.",
            "how to book property": "Once logged in as a seeker, go to the 'Properties' section and click 'Book Now'.",
            "how to list property": "Register as an Owner, then upload property details from your dashboard after approval.",
            "where is your office": "We are an online platform, but our head office is located in Lucknow, India.",
        }

        # Try matching exact or partial questions
        response = None
        for question, answer in faq_data.items():
            if question in user_msg:
                response = answer
                break

        if not response:
            response = "I'm sorry, I don't understand that yet. Please ask something else."

        return JsonResponse({"response": response})
