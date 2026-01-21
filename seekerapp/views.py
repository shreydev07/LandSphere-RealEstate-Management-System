from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.cache import cache_control
from adminapp.models import *
from ownerapp.models import *
from seekerapp.models import *

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def seekerhome(request):
    if 'seekerid' not in request.session:
        return redirect('login')
    return render(request, 'seekerhome.html')

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def seeker_logout(request):
    if 'seekerid' in request.session:
        del request.session['seekerid']
        messages.success(request, 'Seeker logged out successfully!')
    else:
        messages.info(request, 'No active seeker session found.')
    return redirect('login')

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def seeker_profile(request):
    if 'seekerid' not in request.session:
        return redirect('login')
    seeker = get_object_or_404(Seeker, id=request.session['seekerid'])
    return render(request, 'seeker_profile.html', {'seeker': seeker})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def edit_seeker_profile(request):
    if 'seekerid' not in request.session:
        return redirect('login')

    seeker = get_object_or_404(Seeker, id=request.session['seekerid'])

    if request.method == 'POST':
        seeker.name = request.POST.get('name')
        seeker.contact_no = request.POST.get('contact_no')
        seeker.address = request.POST.get('address')

        if 'photo' in request.FILES:
            seeker.photo = request.FILES['photo']

        seeker.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('seekerapp:seeker_profile')

    return render(request, 'edit_seeker_profile.html', {'seeker': seeker})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def available_properties(request):
    if 'seekerid' not in request.session:
        return redirect('login')
    seeker = get_object_or_404(Seeker, id=request.session['seekerid'])
    all_properties = Property.objects.filter(status='Approved')
    booking_requests = BookingRequest.objects.filter(seeker_email=seeker.email)
    booked_property_ids = booking_requests.values_list('property_id', flat=True)

    context = {
        'properties': all_properties,
        'booked_property_ids': set(booked_property_ids)
    }
    return render(request, 'available_properties.html', context)

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def book_property(request, property_id):
    if 'seekerid' not in request.session:
        return redirect('login')
    seeker = get_object_or_404(Seeker, id=request.session['seekerid'])
    prop = get_object_or_404(Property, property_id=property_id, status='Approved')

    if BookingRequest.objects.filter(property=prop, seeker_email=seeker.email).exists():
        messages.info(request, 'You have already requested this property.')
        return redirect('seekerapp:available_properties')

    BookingRequest.objects.create(
        property=prop,
        seeker_name=seeker.name,
        seeker_email=seeker.email,
        seeker_contact=seeker.contact_no,
        status='Pending'
    )
    seeker.booking_status = 'Pending'
    seeker.save()

    messages.success(request, f'Booking request sent for "{prop.title}".')
    return redirect('seekerapp:my_bookings')

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def my_bookings(request):
    if 'seekerid' not in request.session:
        return redirect('login')
    seeker = get_object_or_404(Seeker, id=request.session['seekerid'])
    bookings = BookingRequest.objects.filter(seeker_email=seeker.email)
    return render(request, 'my_bookings.html', {'bookings': bookings})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def seeker_change_password(request):
    if 'seekerid' not in request.session:
        return redirect('login')
    seeker = get_object_or_404(Seeker, id=request.session['seekerid'])

    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if current_password != seeker.password:
            messages.error(request, "Current password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        elif new_password == current_password:
            messages.warning(request, "New password cannot be the same as the current one.")
        else:
            seeker.password = new_password
            seeker.save()
            messages.success(request, "Password changed successfully.")
            return redirect('seekerapp:seekerhome')

    return render(request, 'seeker_change_password.html')



@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def booking_receipt(request, booking_id):
    if 'seekerid' not in request.session:
        return redirect('login')

    booking = get_object_or_404(BookingRequest, id=booking_id, seeker_email=Seeker.objects.get(id=request.session['seekerid']).email)

    if booking.status != 'Accepted':
        messages.error(request, "Receipt is only available for accepted bookings.")
        return redirect('seekerapp:my_bookings')

    return render(request, 'booking_receipt.html', {'booking': booking})


def seeker_complaint(request):
    if 'seekerid' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        name = request.POST.get('seeker_name')
        email = request.POST.get('seeker_email')
        complaint_text = request.POST.get('complaint_text')
        created_at = request.POST.get('created_at')

        Seeker_Complaint.objects.create(seeker_name=name, seeker_email=email, complaint_text=complaint_text, created_at=created_at)
        messages.success(request, "Complaint submitted successfully.")
        return redirect('seekerapp:seekerhome')

    return render(request, 'seeker_complaint.html')

