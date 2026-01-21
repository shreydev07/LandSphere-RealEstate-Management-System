from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from ownerapp.models import *
from seekerapp.models import *
from django.core.mail import send_mail
from django.conf import settings

def adminhome(request):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    return render(request, 'adminhome.html')

def pending_approvals(request):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    owners = Owner.objects.filter(registration_status="Pending")
    seekers = Seeker.objects.filter(registration_status="Pending")
    return render(request, 'pending_approvals.html', {'owners': owners, 'seekers': seekers})

def update_approval(request, user_type, pk, action):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    if request.method == "POST":
        obj = None
        if user_type == "owner":
            obj = get_object_or_404(Owner, pk=pk)
        elif user_type == "seeker":
            obj = get_object_or_404(Seeker, pk=pk)
        else:
            messages.error(request, "Invalid user type.")
            return redirect("adminapp:pending_approvals")

        if action == "approve":
            obj.registration_status = "Approved"
            subject = "Registration Approved"
            message = f"Dear {obj.name},\n\nYour registration as a {user_type} has been approved. You can now log in and use the platform.\n\nThank you,\nLandsphere Team"
        elif action == "reject":
            obj.registration_status = "Rejected"
            subject = "Registration Rejected"
            message = f"Dear {obj.name},\n\nWe regret to inform you that your registration as a {user_type} has been rejected.\n\nThank you,\nLandsphere Team"
        else:
            messages.error(request, "Invalid action.")
            return redirect("adminapp:pending_approvals")

        obj.save()

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [obj.email],
            fail_silently=False
        )

        messages.success(request, f"{user_type.capitalize()} '{obj.name}' has been {obj.registration_status}. Email sent.")
    return redirect("adminapp:pending_approvals")

def approved_seekers(request):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    seekers = Seeker.objects.filter(registration_status="Approved")
    return render(request, "approved_seekers.html", {"approved_seekers": seekers, "total_seekers": seekers.count()})

def approved_owners(request):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    owners = Owner.objects.filter(registration_status="Approved")
    return render(request, "approved_owners.html", {"approved_owners": owners, "total_owners": owners.count()})

def admin_logout(request):
    try:
        del request.session['adminid']
    except KeyError:
        pass
    messages.success(request, 'Admin logged out successfully!')
    return redirect('login')

def pending_properties(request):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    props = Property.objects.filter(status='Pending')
    return render(request, 'pending_property_requests.html', {'properties': props})

def approve_property(request, property_id):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    prop = get_object_or_404(Property, property_id=property_id, status='Pending')
    prop.status = 'Approved'
    prop.save()
    messages.success(request, f'Property "{prop.title}" has been approved.')
    return redirect('adminapp:pending_properties')

def reject_property(request, property_id):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    prop = get_object_or_404(Property, property_id=property_id, status='Pending')
    prop.status = 'Rejected'
    prop.save()
    messages.info(request, f'Property "{prop.title}" has been rejected.')
    return redirect('adminapp:pending_properties')

def sold_properties_list(request):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    props = Property.objects.filter(status='Sold')
    return render(request, 'sold_property_list.html', {'properties': props})

def admin_approved_properties(request):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    props = Property.objects.filter(status='Approved')
    return render(request, 'admin_approved_properties.html', {'properties': props})

def delete_property(request, property_id):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    prop = get_object_or_404(Property, property_id=property_id)
    prop.delete()
    messages.warning(request, f'Property "{prop.title}" has been deleted.')
    return redirect('adminapp:admin_approved_properties')

def admin_change_password(request):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    adminid = request.session.get('adminid')
    admin = get_object_or_404(AdminLogin, id=adminid)
    if request.method == 'POST':
        current = request.POST['current_password']
        new = request.POST['new_password']
        confirm = request.POST['confirm_password']

        if current != admin.password:
            messages.error(request, "Current password is incorrect.")
        elif new != confirm:
            messages.error(request, "New passwords do not match.")
        elif new == current:
            messages.warning(request, "New password cannot be the same as the current password.")
        else:
            admin.password = new
            admin.save()
            messages.success(request, "Password changed successfully. Please log in again.")
            try:
                del request.session['adminid']
            except KeyError:
                pass
            return redirect('login')

    return render(request, 'admin_change_password.html')

def view_complaints(request):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'view_complaints.html', {'complaints': complaints})

def delete_complaint(request, complaint_id):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        complaint.delete()
        messages.success(request, 'Complaint deleted successfully!')
    else:
        messages.error(request, 'Invalid request.')
    return redirect('adminapp:view_complaints')

def view_seeker_complaints(request):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    seeker_complaints = Seeker_Complaint.objects.all().order_by('-created_at')
    return render(request, 'view_seeker_complaints.html', {'seeker_complaints': seeker_complaints})

def delete_seeker_complaint(request, complaint_id):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    complaint = get_object_or_404(Seeker_Complaint, id=complaint_id)
    if request.method == 'POST':
        complaint.delete()
        messages.success(request, 'Complaint deleted successfully.')
    else:
        messages.error(request, 'Invalid request.')
    return redirect('adminapp:view_seeker_complaints')

def view_owner_complaints(request):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    owner_complaints = Owner_Complaint.objects.all().order_by('-created_at')
    return render(request, 'view_owner_complaints.html', {'owner_complaints': owner_complaints})

def delete_owner_complaint(request, complaint_id):
    if not request.session.get('adminid'):
        messages.error(request, "You must be logged in as admin to access this page.")
        return redirect('login')
    complaint = get_object_or_404(Owner_Complaint, id=complaint_id)
    if request.method == 'POST':
        complaint.delete()
        messages.success(request, 'Complaint deleted successfully.')
    else:
        messages.error(request, 'Invalid request.')
    return redirect('adminapp:view_owner_complaints')