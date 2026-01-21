from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.cache import cache_control
from .models import *
from seekerapp.models import *
from django.core.mail import send_mail
from django.conf import settings


# Custom login required decorator for owner
def login_required_owner(view_func):
    def wrapper(request, *args, **kwargs):
        if 'ownerid' not in request.session:
            messages.error(request, 'Please log in first.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_owner
def ownerhome(request):
    return render(request, 'ownerhome.html')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_owner
def add_property(request):
    owner = Owner.objects.get(id=request.session['ownerid'])
    if request.method == 'POST':
        Property.objects.create(
            owner=owner,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            location=request.POST.get('location'),
            images=request.FILES.get('images'),
            status='Pending'
        )
        messages.success(request, 'Property added successfully and sent for admin approval!')
        return redirect('ownerapp:ownerhome')
    return render(request, 'add_property.html')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_owner
def listed_properties(request):
    owner = Owner.objects.get(id=request.session['ownerid'])
    properties = Property.objects.filter(owner=owner, status='Approved')
    return render(request, 'listed_properties.html', {'properties': properties})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_owner
def inlisted_properties(request):
    owner = Owner.objects.get(id=request.session['ownerid'])
    properties = Property.objects.filter(owner=owner, status='Inlisted')
    return render(request, 'inlisted_properties.html', {'properties': properties})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_owner
def inlist_property(request, property_id):
    prop = get_object_or_404(Property, property_id=property_id, owner_id=request.session['ownerid'])
    prop.status = 'Inlisted'
    prop.save()
    messages.info(request, f'Property "{prop.title}" has been temporarily inlisted.')
    return redirect('ownerapp:inlisted_properties')

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_owner
def relist_property(request, property_id):
    property = get_object_or_404(Property, property_id=property_id,  owner_id=request.session['ownerid'])

    if property.status == 'Inlisted':
        property.status = 'Approved'
        property.save()
        messages.success(request, "Property is re-listed.")
    else:
        messages.warning(request, "Property is not currently inlisted.")

    return redirect('ownerapp:listed_properties')  


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_owner
def property_applicants(request, property_id):
    prop = get_object_or_404(Property, property_id=property_id, owner_id=request.session['ownerid'])
    requests = BookingRequest.objects.filter(property=prop, status='Pending')
    return render(request, 'property_applicants.html', {'property': prop, 'requests': requests})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_owner
def accept_request(request, property_id, request_id):
    prop = get_object_or_404(Property, property_id=property_id, owner_id=request.session['ownerid'])
    booking = get_object_or_404(BookingRequest, id=request_id, property=prop, status='Pending')
    booking.status = 'Accepted'
    booking.save()

    BookingRequest.objects.filter(property=prop).exclude(id=request_id).update(status='Rejected')
    prop.status = 'Sold'
    prop.save()

    try:
        seeker = Seeker.objects.get(email=booking.seeker_email)
        seeker.booking_status = 'Already Booked'
        seeker.save()

        send_mail(
            subject="Booking Accepted - Landsphere",
            message=(
                f"Dear {seeker.name},\n\n"
                f"Your booking request for the property \"{prop.title}\" has been accepted!\n"
                f"The property is now marked as Sold.\n\n"
                "Thank you for using Landsphere.\n"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[seeker.email],
            fail_silently=False
        )

    except Seeker.DoesNotExist:
        pass

    messages.success(request, f'Booking accepted. Property "{prop.title}" marked as sold.')
    return redirect('ownerapp:property_applicants', property_id=property_id)


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_owner
def reject_request(request, property_id, request_id):
    prop = get_object_or_404(Property, property_id=property_id, owner_id=request.session['ownerid'])
    booking = get_object_or_404(BookingRequest, id=request_id, property=prop, status='Pending')
    booking.status = 'Rejected'
    booking.save()

    try:
        seeker = Seeker.objects.get(email=booking.seeker_email)
        seeker.booking_status = 'No Booking'
        seeker.save()

        send_mail(
            subject="Booking Request Rejected - Landsphere",
            message=(
                f"Dear {seeker.name},\n\n"
                f"We regret to inform you that your booking request for the property \"{prop.title}\" has been rejected by the owner.\n"
                f"You may explore and apply for other available properties on the platform.\n\n"
                "Thank you for using Landsphere.\n"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[seeker.email],
            fail_silently=False
        )

    except Seeker.DoesNotExist:
        pass

    messages.info(request, f'Booking request by {booking.seeker_name} rejected.')
    return redirect('ownerapp:property_applicants', property_id=property_id)


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_owner
def sold_properties(request):
    properties = Property.objects.filter(owner_id=request.session['ownerid'], status='Sold')
    return render(request, 'sold_properties.html', {'properties': properties})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_owner
def pending_properties(request):
    pending_props = Property.objects.filter(owner_id=request.session['ownerid'], status='Pending' and 'Rejected')
    return render(request, 'pending_properties.html', {'properties': pending_props})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_owner
def owner_profile(request):
    owner = Owner.objects.get(id=request.session['ownerid'])
    return render(request, 'owner_profile.html', {'owner': owner})



@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_owner
def edit_owner_profile(request):
    owner = Owner.objects.get(id=request.session['ownerid'])

    if request.method == 'POST':
        owner.name = request.POST.get('name')   
        owner.contact_no = request.POST.get('contact_no')
        owner.address = request.POST.get('address')

        if 'profile_photo' in request.FILES:
            owner.profile_photo = request.FILES['profile_photo']

        owner.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('ownerapp:owner_profile')

    return render(request, 'edit_owner_profile.html', {'owner': owner})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_owner
def change_password(request):
    owner = Owner.objects.get(id=request.session['ownerid'])
    if request.method == 'POST':
        current = request.POST['current_password']
        new = request.POST['new_password']
        confirm = request.POST['confirm_password']

        if current != owner.password:
            messages.error(request, "Current password is incorrect.")
        elif new != confirm:
            messages.error(request, "New passwords do not match.")
        elif new == current:
            messages.warning(request, "New password cannot be the same as the current password.")
        else:
            owner.password = new
            owner.save()
            messages.success(request, "Password changed successfully.")
            return redirect('ownerapp:ownerhome')

    return render(request, 'change_password.html')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def owner_logout(request):
    if 'ownerid' in request.session:
        del request.session['ownerid']
        messages.success(request, 'Owner logged out successfully!')
    else:
        messages.info(request, 'No active owner session found.')
    return redirect('login')



@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def owner_complaint(request):
    if request.method == 'POST':
        owner_name = request.POST.get('owner_name')
        owner_email = request.POST.get('owner_email')
        complaint_text = request.POST.get('complaint_text')

        Owner_Complaint.objects.create(
            owner_name=owner_name,
            owner_email=owner_email,
            complaint_text=complaint_text
        )

        messages.success(request, 'Complaint submitted successfully!')
        return redirect('ownerapp:ownerhome')

    return render(request, 'owner_complaint.html')





