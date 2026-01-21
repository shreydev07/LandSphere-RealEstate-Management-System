from django.urls import path
from . import views

app_name = 'adminapp'

urlpatterns = [
   path('adminhome/', views.adminhome, name='adminhome'),
   path('admin/pending-approvals/', views.pending_approvals, name="pending_approvals"),
   path('admin/update-approval/<str:user_type>/<int:pk>/<str:action>/', views.update_approval, name="update_approval"),
   path('admin/approved-seekers/', views.approved_seekers, name="approved_seekers"),
   path('admin/approved-owners/', views.approved_owners, name="approved_owners"),
   path('admin/logout/', views.admin_logout, name="admin_logout"),\
   path('admin/pending-approvals/', views.pending_approvals, name="pending_approvals"),  # existing
   path('admin/pending-properties/', views.pending_properties, name='pending_properties'),
   path('admin/approve-property/<int:property_id>/', views.approve_property, name='approve_property'),
   path('admin/reject-property/<int:property_id>/', views.reject_property, name='reject_property'),
   path('admin/sold-properties/', views.sold_properties_list, name='sold_properties_list'),
   path('admin/approved-properties/', views.admin_approved_properties, name='admin_approved_properties'),
   path('admin/delete-property/<int:property_id>/', views.delete_property, name='delete_property'),
   path('admin_change-password/', views.admin_change_password, name='admin_change_password'),
   path('view_complaints/',views.view_complaints, name='view_complaints'),
   path('delete/<int:complaint_id>/',views.delete_complaint, name='delete_complaint'),
   path('admin/view-seeker-complaints/', views.view_seeker_complaints, name='view_seeker_complaints'),
   path('delete-seeker-complaint/<int:complaint_id>/', views.delete_seeker_complaint, name='delete_seeker_complaint'),
   path('admin/view-owner-complaints/', views.view_owner_complaints, name='view_owner_complaints'),
   path('delete-owner-complaint/<int:complaint_id>/', views.delete_owner_complaint, name='delete_owner_complaint'),

]
